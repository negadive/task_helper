from unittest.mock import Mock

import pytest
from model.project import Project
from model.task.type import Task
from repository.project_repository.type import ProjectRepositoryP
from repository.task_repository.type import TaskRepository
from repository.vcs_repository.type import VCSRepository
from service.pivotal_vcs_service import PivotalVCSService


@pytest.fixture
def mocked_vcs_repo() -> VCSRepository:
    return Mock(VCSRepository)


@pytest.fixture
def mocked_task_repo() -> TaskRepository:
    return Mock(TaskRepository)


@pytest.fixture
def mocked_project_repo() -> ProjectRepositoryP:
    return Mock(ProjectRepositoryP)


@pytest.mark.parametrize(
    ("task_id", "task_type", "task_title", "project", "expected_branch_name"),
    (
        (
            1,
            "feature",
            "title",
            Project(id="1", name="project-name"),
            "project-name/feature/1-title",
        ),
        (
            2,
            "bug",
            "title-2",
            Project(id="2", name="also-project-name"),
            "also-project-name/bug/2-title-2",
        ),
        (
            1,
            "feature",
            "branch-name with [[brackets]]  space  and::colons__underline's",
            Project(id="1", name="project-name"),
            "project-name/feature/1-branch-name-with-brackets-space-and-colons-underlines",
        ),
    ),
)
def test_make_branch(
    mocked_vcs_repo: VCSRepository,
    mocked_task_repo: TaskRepository,
    mocked_project_repo: ProjectRepositoryP,
    task_id: int,
    task_type: str,
    task_title: str,
    project: Project,
    expected_branch_name: str,
):
    mocked_task: Task = Mock()
    mocked_task.id = task_id
    mocked_task.type = task_type
    mocked_task.title = task_title

    mocked_task_repo.get = Mock(return_value=mocked_task)
    mocked_project_repo.find = Mock(return_value=project)

    service = PivotalVCSService(
        vcs_repo=mocked_vcs_repo,
        task_repo=mocked_task_repo,
        project_repo=mocked_project_repo,
    )

    service.make_branch(task_id)

    mocked_vcs_repo.create_branch.assert_called_with(expected_branch_name)
