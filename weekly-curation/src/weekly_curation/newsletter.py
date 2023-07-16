from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Self
from itertools import groupby

Category = str


@dataclass
class Link:
    content_type: str
    name: str
    url: str
    category: Category
    subcategories: list[str]
    date_of_publication: datetime
    contributor: Optional[str] = None


@dataclass
class Issue:
    date: datetime
    links: list[Link]

    def group_links_by_categories(self) -> dict[Category, list[Link]]:
        return {
            key: list(result)
            for key, result in groupby(self.links, key=lambda l: l.category)
        }


class LinkBuilder:
    def __init__(self) -> None:
        self.link = Link(
            content_type="🧰",
            name="Understanding SVG Paths",
            url="https://...",
            category="WebDevelopment",
            subcategories=["SVG", "Cursor", "Line", "Bezier", "Animation", "Demo"],
            date_of_publication=datetime(day=3, month=7, year=2023),
            contributor="[@rfrenoy](https://github.com/rfrenoy)",
        )

    def build(self) -> Link:
        return self.link

    def set_content_type(self, content_type: str) -> Self:
        self.link.content_type = content_type
        return self

    def set_name(self, name: str) -> Self:
        self.link.name = name
        return self

    def set_url(self, url: str) -> Self:
        self.link.url = url
        return self

    def set_category(self, category: Category) -> Self:
        self.link.category = category
        return self

    def set_subcategories(self, subcategories: list[str]) -> Self:
        self.link.subcategories = subcategories
        return self

    def set_date_of_publication(self, date_of_publication: datetime) -> Self:
        self.link.date_of_publication = date_of_publication
        return self

    def set_contributor(self, contributor: Optional[str]) -> Self:
        self.link.contributor = contributor
        return self
