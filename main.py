import click
import git

from branch_maker import make_branch
from config import Config
from custom_logging import logger
from pivotal_tracker import PivotalTracker


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
    @click.pass_context
    def mkb(ctx: click.Context, story_id: str):
        """Make branch cli

        Args:
            ctx (click.Context): _description_
            story_id (str): _description_
        """
        config: Config = ctx.obj["config"]

        pt = PivotalTracker(
            config.PIVOTAL_TRACKER_PROJECT_ID, config.PIVOTAL_TRACKER_TOKEN
        )
        repo = git.Repo(config.REPO_DIR)

        make_branch(repo, pt.get_story(story_id))

    main_command(obj={})


if __name__ == "__main__":
    main()
