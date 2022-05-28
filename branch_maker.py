import re

import git

from custom_logging import logger
from pivotal_tracker.story import Story

BRANCH_NAME_FORMAT = "disco/{story_type}/{story_id}-{story_title}"


def _sanitize_branch_name(string: str) -> str:
    """Make a valid branch name

    Args:
        string (str): _description_

    Returns:
        str: Valid branch name
    """
    string = string.lower()
    string = re.sub(r"[\[\]]", "", string)
    string = re.sub(r"\s|:+", "-", string)

    return string


def make_branch(repo: git.Repo, story: Story):
    """Make branch from story

    Args:
        repo (git.Repo): _description_
        story (Story): _description_

    Returns:
        str: Branch name
    """
    branch_name = BRANCH_NAME_FORMAT.format(
        story_type=story.type,
        story_id=story.id,
        story_title=_sanitize_branch_name(story.title),
    )

    repo.git.checkout("-b", branch_name)
    logger.info("Branch made with name: %s", branch_name)

    return branch_name
