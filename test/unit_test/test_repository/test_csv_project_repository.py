import pandas as pd
import pytest
from model.project import Project
from repository.project_repository.csv_project_repository import (
    CSVProjectRepository,
)

PROJECT_PATH = "./test_projects.csv"


def tear_down():
    open(PROJECT_PATH, "w").close()


def test_initialize():
    with pytest.raises(Exception):
        CSVProjectRepository(None)


@pytest.mark.parametrize(
    ("project_id", "project_name"),
    (
        (1, "project 1"),
        (2, "project 3"),
        pytest.param(3, "project 3", marks=pytest.mark.xfail),
    ),
)
def test_find(project_id: int, project_name: str):
    pd.DataFrame(
        [{"id": 1, "name": "project 1"}, {"id": 2, "name": "project 3"}]
    ).to_csv(PROJECT_PATH)

    repo = CSVProjectRepository(PROJECT_PATH)

    project: Project = repo.find(project_id)

    assert project.id == project_id
    assert project.name == project_name

    tear_down()


@pytest.mark.xfail
@pytest.mark.parametrize(("project_id", "project_name"), ((1, "project 1"),))
def test_find_empty_data(project_id: int, project_name: str):
    repo = CSVProjectRepository(PROJECT_PATH)

    project: Project = repo.find(project_id)

    assert project.id == project_id
    assert project.name == project_name

    tear_down()


@pytest.mark.parametrize(
    ("project_id", "project_name"),
    (
        (1, "project 1"),
        (2, "project 2"),
    ),
)
def test_store(project_id: int, project_name: str):
    repo = CSVProjectRepository(PROJECT_PATH)

    repo.store(Project(project_id, project_name))

    datas = pd.read_csv(PROJECT_PATH)
    datas = datas[datas["id"] == project_id].to_dict("records")

    assert len(datas) > 0

    data = datas[0]
    assert data["name"] == project_name

    tear_down()


@pytest.mark.xfail
@pytest.mark.parametrize(("project_id", "project_name"), ((3, "project 3"),))
def test_store_data_exist(project_id: int, project_name: str):
    pd.DataFrame([{"id": 3, "name": "project 3"}]).to_csv(PROJECT_PATH)

    repo = CSVProjectRepository(PROJECT_PATH)

    repo.store(Project(project_id, project_name))

    tear_down()
