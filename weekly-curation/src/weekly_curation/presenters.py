from abc import ABC, abstractmethod

from src.weekly_curation.newsletter import Issue

from src.weekly_curation.newsletter import Issue, Link


class NewsletterPresenter(ABC):
    @abstractmethod
    def present_link(link: Link) -> str:
        raise NotImplementedError

    @abstractmethod
    def present_issue(issue: Issue) -> str:
        raise NotImplementedError


class MarkdownPresenter(NewsletterPresenter):
    @staticmethod
    def present_link(link: Link) -> str:
        subcategories_prepended_with_hashtag = [
            "#" + subcat for subcat in link.subcategories
        ]
        presented_link = f"- {link.content_type} [{link.name}]({link.url}) | {' '.join(subcategories_prepended_with_hashtag)}"

        if not link.contributor:
            return presented_link
        else:
            return f"{presented_link}\n    - Contributed by {link.contributor}"

    @staticmethod
    def present_issue(issue: Issue) -> str:
        grouped_by_categories: dict[str, list[Link]] = issue.group_links_by_categories()

        grouping_with_markdown_links: dict[str, str] = {}
        for category, links in grouped_by_categories.items():
            grouping_with_markdown_links[category] = "\n".join(
                list(map(MarkdownPresenter().present_link, links))
            )

        md_categories: list[str] = []
        for k, v in grouping_with_markdown_links.items():
            md_categories.append(f"### {k}\n\n{v}\n\n")

        issue_header = f"## {issue.date.strftime('%dth %b. %Y')}\n\n"
        return issue_header + "".join(md_categories)
