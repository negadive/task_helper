import json
import os


class Project:
    id: str
    name: str

    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name

    @classmethod
    def register(cls, project_id: str, name: str) -> None:
        projects: dict = json.loads(os.getenv('PROJECTS', '{}'))

        projects.update({project_id: name})

        os.environ['PROJECTS'] = json.dumps(projects)

    @classmethod
    def get(cls, project_id: str) -> "Project":
        projects: dict = json.loads(os.getenv('PROJECTS', '{}'))

        return cls(project_id, projects.get(project_id))