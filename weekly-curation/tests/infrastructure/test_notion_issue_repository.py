from datetime import datetime
from typing import Any

from pytest import fixture
from src.weekly_curation.newsletter import Issue, Link
from src.weekly_curation.infrastructure.notion_issue_repository import (
    NotionIssueRepository,
    notion_result_to_link,
)


def test_notion_repository_get_by_issue_name():
    assert Issue(
        date=datetime(day=10, month=7, year=2023), links=[]
    ) == NotionIssueRepository().get_by_issue_name("10th of Jul. 2023")


def test_notion_result_to_link(a_result):
    assert notion_result_to_link(a_result) == Link(
        name="AWS SQS, SNS, Kinesis, EventBridge : How to choose ?",
        category="Architecture 📐",
        content_type="📝",
        contributor=None,
        date_of_publication=None,
        subcategories=[
            "AWS",
            "SQS",
            "SNS",
            "Kinesis",
            "EventBridge",
            "Queue",
            "Messaging",
        ],
        url="https://dev.to/onepoint/aws-sqs-sns-kinesis-eventbridge-how-to-choose--32l7",
    )


@fixture
def a_result() -> dict[str, Any]:
    return {
        "archived": False,
        "cover": None,
        "created_by": {
            "id": "fde248d8-d1e5-44ab-abf1-9b051891dd87",
            "object": "user",
        },
        "created_time": "2023-07-08T13:14:00.000Z",
        "icon": None,
        "id": "d980c14f-0dd6-4deb-a151-9f9e89f34311",
        "last_edited_by": {
            "id": "fde248d8-d1e5-44ab-abf1-9b051891dd87",
            "object": "user",
        },
        "last_edited_time": "2023-07-10T18:03:00.000Z",
        "object": "page",
        "parent": {
            "database_id": "3c7b35b5-2256-4a0a-b646-525ef8613d91",
            "type": "database_id",
        },
        "properties": {
            "Article": {
                "id": "title",
                "title": [
                    {
                        "annotations": {
                            "bold": True,
                            "code": False,
                            "color": "default",
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                        },
                        "href": None,
                        "plain_text": "AWS SQS, "
                        "SNS, "
                        "Kinesis, "
                        "EventBridge "
                        ": How to "
                        "choose ?",
                        "text": {
                            "content": "AWS "
                            "SQS, "
                            "SNS, "
                            "Kinesis, "
                            "EventBridge "
                            ": How "
                            "to "
                            "choose "
                            "?",
                            "link": None,
                        },
                        "type": "text",
                    }
                ],
                "type": "title",
            },
            "Category": {
                "id": "TiaJ",
                "select": {
                    "color": "red",
                    "id": "5918936c-3dfb-4598-9d6f-0b690d8117c6",
                    "name": "Architecture 📐",
                },
                "type": "select",
            },
            "Contributor": {"id": "Pytl", "rich_text": [], "type": "rich_text"},
            "DateOfOriginalPublication": {
                "date": None,
                "id": "svEa",
                "type": "date",
            },
            "Freshness": {
                "formula": {"string": "🆕", "type": "string"},
                "id": "VyCK",
                "type": "formula",
            },
            "NewsletterIssue": {
                "date": {"end": None, "start": "2023-07-10", "time_zone": None},
                "id": "fmO%3A",
                "type": "date",
            },
            "NewsletterIssueDateFormat": {
                "formula": {
                    "string": "10th " "of " "July " "2023",
                    "type": "string",
                },
                "id": "YopO",
                "type": "formula",
            },
            "Subcategories": {
                "id": "GThr",
                "multi_select": [
                    {
                        "color": "orange",
                        "id": "d912f07c-3d60-4fa0-97b1-b29295fe5122",
                        "name": "AWS",
                    },
                    {
                        "color": "red",
                        "id": "6f504475-f75a-439d-8ed9-960f390ba46a",
                        "name": "SQS",
                    },
                    {
                        "color": "green",
                        "id": "247aa0e8-e231-4700-be51-179f93417cfb",
                        "name": "SNS",
                    },
                    {
                        "color": "default",
                        "id": "06e533c6-7bed-489f-8701-2e46295399ab",
                        "name": "Kinesis",
                    },
                    {
                        "color": "default",
                        "id": "0598ee79-8bad-48a8-a5be-b13f3c25cac3",
                        "name": "EventBridge",
                    },
                    {
                        "color": "red",
                        "id": "0d03b9bb-f35c-4b56-b209-4345cbd8035e",
                        "name": "Queue",
                    },
                    {
                        "color": "yellow",
                        "id": "90148fd2-84ff-44f1-b414-425a802c976c",
                        "name": "Messaging",
                    },
                ],
                "type": "multi_select",
            },
            "Type": {
                "id": "%60Cbk",
                "select": {
                    "color": "brown",
                    "id": "2ca5a053-7eb0-4753-bec5-9259bd1ccb6d",
                    "name": "📝",
                },
                "type": "select",
            },
            "URL": {
                "id": "z_H%3C",
                "type": "url",
                "url": "https://dev.to/onepoint/aws-sqs-sns-kinesis-eventbridge-how-to-choose--32l7",
            },
        },
        "public_url": None,
        "url": "https://www.notion.so/AWS-SQS-SNS-Kinesis-EventBridge-How-to-choose-d980c14f0dd64deba1519f9e89f34311",
    }
