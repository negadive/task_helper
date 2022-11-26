import click

from config import Config
from custom_logging import logger
from repository.project_repository.csv_project_repository import (
    CSVProjectRepository,
)
from repository.project_repository.errors import ProjectExist, ProjectNotFound
from repository.task_repository.errors import TaskNotFound
from repository.task_repository.pivotal_task_repository import (
    PivotalTaskRepository,
)
from repository.vcs_repository.git_vcs_repository import GitVCSRepository
from service.pivotal_vcs_service import PivotalVCSService
from service.project_service import ProjectService


def main():
    @click.group()
    @click.pass_context
    def main_command(ctx: click.Context):
        """Task helper, helps you with your tasks
        \f

        Args:
            ctx (click.Context): Context for sub command
        """
        ctx.ensure_object(dict)

        config = Config()
        logger.debug(f"{config.__dict__=}")
        ctx.obj["config"] = config

        ctx.obj["project_service"] = ProjectService(
            repo=CSVProjectRepository(config.CSV_PROJECT_REPO_DIR)
        )

        return

    @main_command.command()
    @click.argument("story_id", required=True)
    @click.option("--project", default="")
    @click.pass_context
    def mkb(ctx: click.Context, story_id: str, project: str):
        """Make branch
        \f

        Args:
            ctx (click.Context): Command context
            story_id (str): Story id
        """
        config: Config = ctx.obj["config"]
        project_id = project or config.PIVOTAL_TRACKER_PROJECT_ID

        pivotal_vcs_service = PivotalVCSService(
            vcs_repo=GitVCSRepository(config.REPO_DIR),
            task_repo=PivotalTaskRepository(
                project_id, config.PIVOTAL_TRACKER_TOKEN
            ),
            project_repo=ctx.obj["project_service"],
        )
        try:
            return pivotal_vcs_service.make_branch(story_id)
        except TaskNotFound as e:
            logger.error(f"Task Not Found: {e}")
        except ProjectNotFound:
            logger.error("Project havent registered")

    @main_command.command()
    @click.argument("project_id", required=True)
    @click.argument("name", required=True)
    @click.pass_context
    def register_project(ctx: click.Context, project_id: str, name: str) -> None:
        """Register project for other commands
        \f

        Args:
            ctx (click.Context): Command context
            project_id (str): Project id
            name (str): Project name
        """
        project_service: ProjectService = ctx.obj["project_service"]

        try:
            return project_service.register(int(project_id), name)
        except ProjectExist:
            logger.error("Project already registered")

    main_command(obj={})


if __name__ == "__main__":
    main()
