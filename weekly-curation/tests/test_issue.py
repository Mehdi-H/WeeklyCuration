from datetime import datetime
from src.weekly_curation.newsletter import Issue, Link, LinkBuilder


def test_link_builder():
    assert LinkBuilder().set_name("Article#1").set_category("AI").build() == Link(
        content_type="🧰",
        name="Article#1",
        url="https://...",
        category="AI",
        subcategories=["SVG", "Cursor", "Line", "Bezier", "Animation", "Demo"],
        date_of_publication=datetime(day=3, month=7, year=2023),
        contributor="[@rfrenoy](https://github.com/rfrenoy)",
    )


def test_group_links_by_categories():
    article1, article2, article3 = (
        LinkBuilder().set_name("Article#1").set_category("AI").build(),
        LinkBuilder().set_name("Article#2").set_category("AI").build(),
        LinkBuilder().set_name("Article#3").set_category("AI").build(),
    )
    article4, article5 = (
        LinkBuilder().set_name("Article#4").set_category("Cloud").build(),
        LinkBuilder().set_name("Article#5").set_category("Cloud").build(),
    )
    an_issue = Issue(
        date=datetime.now(),
        links=[article1, article2, article3, article4, article5],
    )

    assert an_issue.group_links_by_categories() == {
        "AI": [article1, article2, article3],
        "Cloud": [article4, article5],
    }
