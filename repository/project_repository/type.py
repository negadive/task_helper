from typing import Protocol

from pivotal_tracker.project import Project


class ProjectRepositoryP(Protocol):
    def find(self, project_id: int) -> Project:
        ...

    def store(self, project: Project) -> None:
        ...
