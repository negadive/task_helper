import click
import git

from branch_maker import make_branch
from config import Config
from custom_logging import logger
from pivotal_tracker import PivotalTracker
from repository.project_repository.csv_project_repository import (
    CSVProjectRepository,
)
from repository.project_repository.errors import ProjectExist
from service.project_service import ProjectService


def main():
    @click.group()
    @click.pass_context
    def main_command(ctx: click.Context):
        """Main cli

        Args:
            ctx (click.Context): _description_
        """
        ctx.ensure_object(dict)

        config = Config()
        logger.debug(f"{config.__dict__=}")
        ctx.obj["config"] = config

        project_service = ProjectService(repo=CSVProjectRepository())
        ctx.obj["project_service"] = project_service

        return

    @main_command.command()
    @click.argument("story_id", required=True)
    @click.option("--project", default="")
    @click.pass_context
    def mkb(ctx: click.Context, story_id: str, project: str):
        """Make branch cli

        Args:
            ctx (click.Context): _description_
            story_id (str): _description_
        """
        config: Config = ctx.obj["config"]
        project_id = project or config.PIVOTAL_TRACKER_PROJECT_ID

        pt = PivotalTracker(project_id, config.PIVOTAL_TRACKER_TOKEN)
        repo = git.Repo(config.REPO_DIR)

        return make_branch(repo, pt.get_story(story_id))

    @main_command.command()
    @click.argument("project_id", required=True)
    @click.argument("name", required=True)
    @click.pass_context
    def register_project(ctx: click.Context, project_id: str, name: str):
        project_service: ProjectService = ctx.obj["project_service"]

        try:
            return project_service.register(int(project_id), name)
        except ProjectExist:
            logger.error("Project already registered")

    main_command(obj={})


if __name__ == "__main__":
    main()
