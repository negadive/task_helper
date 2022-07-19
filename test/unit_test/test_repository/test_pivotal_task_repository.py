import re

import pytest
from model.task.pivotal_task import PivotalTask
from repository.task_repository.errors import TaskNotFound
from repository.task_repository.pivotal_task_repository import (
    PivotalTaskRepository,
)


@pytest.fixture
def task_repo() -> PivotalTaskRepository:
    return PivotalTaskRepository("123", "123")


@pytest.mark.parametrize(
    "story_id,expected_id,expected_title,expected_type,expected_project_id",
    (
        [1, 1, "Story name", "feature", "34"],
        [1, 1, "Story name 3", "bug", "65"],
    ),
)
def test_get_story(
    requests_mock,
    task_repo: PivotalTaskRepository,
    story_id: int,
    expected_id: int,
    expected_title: str,
    expected_type: str,
    expected_project_id: str,
):
    requests_mock.get(
        re.compile(
            rf"https:\/\/www.pivotaltracker.com/(.*)/stories/{story_id}"
        ),
        json={
            "id": expected_id,
            "name": expected_title,
            "story_type": expected_type,
            "project_id": expected_project_id,
        },
    )

    story = task_repo.get(story_id)

    assert isinstance(story, PivotalTask)
    assert story.id == expected_id
    assert story.title == expected_title
    assert story.type == expected_type


def test_not_found_story(requests_mock, task_repo: PivotalTaskRepository):
    requests_mock.get(
        re.compile(r"https:\/\/www.pivotaltracker.com/(.*)/stories/11"),
        status_code=404,
        text="Story not found",
    )

    with pytest.raises(TaskNotFound):
        task_repo.get(11)
