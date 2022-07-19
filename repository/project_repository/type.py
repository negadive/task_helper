from typing import Protocol

from model.project import Project


class ProjectRepositoryP(Protocol):
    def find(self, project_id: int) -> Project:
        ...

    def store(self, project: Project) -> None:
        ...
