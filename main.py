import click
import git

from branch_maker import make_branch
from config import Config
from custom_logging import logger
from pivotal_tracker import PivotalTracker
from pivotal_tracker.project import Project


def main():
    @click.group()
    @click.pass_context
    def main_command(ctx: click.Context):
        """Main cli

        Args:
            ctx (click.Context): _description_
        """
        config = Config()
        logger.debug(f"{config.__dict__=}")

        ctx.ensure_object(dict)
        ctx.obj["config"] = config

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

        pt = PivotalTracker(
            project_id, config.PIVOTAL_TRACKER_TOKEN
        )
        repo = git.Repo(config.REPO_DIR)

        make_branch(repo, pt.get_story(story_id))

    @main_command.command()
    @click.argument("project_id", required=True)
    @click.argument("name", required=True)
    def register_project(project_id: str, name: str):
        Project.register(project_id, name)


    main_command(obj={})


if __name__ == "__main__":
    main()
