from datetime import datetime
from pathlib import Path
from pytest import fixture
from src.weekly_curation.newsletter import Issue, Link
from src.weekly_curation.presenters import MarkdownPresenter


def test_link_presented_in_markdown(a_link: Link):
    markdown_link = MarkdownPresenter().present_link(a_link)
    assert (
        markdown_link
        == "- 📝 [AI Could Change How Blind People See the World](https://www.wired.com/story/ai-gpt4-could-change-how-blind-people-see-the-world/) | #R&D #GPT-4"
    )


def test_link_from_a_contributor_presented_in_markdown(a_link_from_a_contributor: Link):
    markdown_link = MarkdownPresenter().present_link(a_link_from_a_contributor)
    assert (
        markdown_link
        == """- 🧰 [Understanding SVG Paths](https://www.nan.fyi/svg-paths) | #SVG #Cursor #Line #Bezier #Animation #Demo
    - Contributed by [@rfrenoy](https://github.com/rfrenoy)"""
    )


def test_an_issue_with_two_links_from_two_distinct_categories(
    a_link: Link, a_link_from_a_contributor: Link, expected_issue: str
):
    newsleter_issue = Issue(
        date=datetime(day=10, month=7, year=2023),
        links=[a_link, a_link_from_a_contributor],
    )
    markdown_issue = MarkdownPresenter().present_issue(newsleter_issue)
    assert markdown_issue == expected_issue


@fixture
def a_link() -> Link:
    return Link(
        content_type="📝",
        name="AI Could Change How Blind People See the World",
        url="https://www.wired.com/story/ai-gpt4-could-change-how-blind-people-see-the-world/",
        category="AI",
        subcategories=["R&D", "GPT-4"],
        date_of_publication=datetime(day=9, month=7, year=2023),
        contributor=None,
    )


@fixture
def a_link_from_a_contributor() -> Link:
    return Link(
        content_type="🧰",
        name="Understanding SVG Paths",
        url="https://www.nan.fyi/svg-paths",
        category="WebDevelopment",
        subcategories=["SVG", "Cursor", "Line", "Bezier", "Animation", "Demo"],
        date_of_publication=datetime(day=3, month=7, year=2023),
        contributor="[@rfrenoy](https://github.com/rfrenoy)",
    )


@fixture
def expected_issue() -> str:
    script_location = Path(__file__).absolute().parent
    with open(script_location / "sample_issue.md", "r") as issue_of_july_10:
        return issue_of_july_10.read()
