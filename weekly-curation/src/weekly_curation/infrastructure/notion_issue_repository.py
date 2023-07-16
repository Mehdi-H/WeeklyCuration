from datetime import datetime
import os
from typing import Any
from notion_client import Client as NotionClient
from src.weekly_curation.newsletter import Issue, Link
from src.weekly_curation.issue_repository import IssueRepository


class NotionIssueRepository(IssueRepository):
    def __init__(self) -> None:
        self.notion_client = NotionClient(auth=os.environ["NOTION_API_KEY"])
        self.notion_db_id: str = os.environ["NOTION_DB"]

    def get_by_issue_name(self, issue_name: str) -> Issue:
        results: dict[str, Any] = self.notion_client.databases.query(
            **{
                "database_id": self.notion_db_id,
                "filter": {
                    "and": [
                        {
                            "property": "NewsletterIssueDateFormat",
                            "formula": {"string": {"equals": issue_name}},
                        }
                    ]
                },
                "sorts": [
                    {"property": "NewsletterIssue", "direction": "ascending"},
                    {"property": "Category", "direction": "ascending"},
                ],
            }
        ).get("results")
        links = [notion_result_to_link(result) for result in results]
        return Issue(datetime.strptime(issue_name, "%dth of %b. %Y"), links)

    def get_all(
        self,
    ) -> list[Issue]:
        raise NotImplementedError


def notion_result_to_link(result: dict[str, Any]) -> Link:
    properties = result.get("properties", {})
    return Link(
        name=properties.get("Article").get("title")[0].get("plain_text"),
        category=properties.get("Category", {}).get("select", {}).get("name"),
        content_type=properties.get("Type").get("select").get("name"),
        date_of_publication=None,
        subcategories=[
            select.get("name")
            for select in properties.get("Subcategories").get("multi_select")
        ],
        url=properties.get("URL").get("url"),
    )


