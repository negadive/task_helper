import json
import os
from typing import Dict

import pytest
from pivotal_tracker.project import Project


def get_projects() -> Dict[str, str]:
    return json.loads(os.environ.get("PROJECTS", "{}"))


def clear_projects() -> None:
    os.environ["PROJECTS"] = json.dumps({})


@pytest.mark.parametrize(
    "project_id,name",
    (["1", "disco"], ["2", "web"], ["1", "web"]),
)
def test_register_project(project_id: str, name: str):
    Project.register(project_id, name)

    projects = get_projects()

    assert project_id in projects
    assert projects[project_id] == name

    clear_projects()


@pytest.mark.parametrize(
    "project_id,expected_name",
    (
        ["1", "disco"],
        ["2", "web"],
        pytest.param("1", "web", marks=pytest.mark.xfail),
    ),
)
def test_get_project(project_id, expected_name):
    Project.register("1", "disco")
    Project.register("2", "web")

    project = Project.get(project_id)

    assert isinstance(project, Project)
    assert project.id == project_id
    assert project.name == expected_name

    clear_projects()
