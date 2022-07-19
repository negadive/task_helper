import pandas as pd
from model.project import Project
from pandas.errors import EmptyDataError

from .errors import ProjectEmpty, ProjectExist, ProjectNotFound


class CSVProjectRepository:
    def __init__(self, csv_path: str = "./projects.csv") -> None:
        self._csv_path = csv_path

    def find(self, project_id: int) -> Project:
        try:
            datas = self._get_datas()
        except EmptyDataError as e:
            raise ProjectEmpty from e

        datas = datas[datas["id"] == project_id].to_dict("records")
        if not len(datas) > 0:
            raise ProjectNotFound
        data = datas[0]

        return Project(project_id, data["name"])

    def store(self, project: Project) -> None:
        set_header = False
        try:
            self._get_datas()
        except EmptyDataError:
            set_header = True

        try:
            self.find(project.id)
        except (ProjectEmpty, ProjectNotFound):
            ...
        else:
            raise ProjectExist

        pd.DataFrame([{"id": int(project.id), "name": project.name}]).to_csv(
            self._csv_path, mode="a", header=set_header
        )

    def _get_datas(self):
        return pd.read_csv(self._csv_path)
