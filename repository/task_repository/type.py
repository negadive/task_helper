from typing import Protocol

from model.task.type import Task


class TaskRepository(Protocol):
    def get(self, task_id: str) -> Task:
        ...
