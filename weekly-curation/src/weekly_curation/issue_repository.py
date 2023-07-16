from abc import ABC, abstractmethod

from src.weekly_curation.newsletter import Issue


class IssueRepository(ABC):
    @abstractmethod
    def get_by_issue_name(self, issue_name: str) -> Issue:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Issue]:
        raise NotImplementedError
