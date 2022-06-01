from unittest import mock

import git
import pytest
from branch_maker import make_branch
from pivotal_tracker.story import Story


@pytest.fixture
def story() -> Story:
    story = mock.Mock(Story)
    story.type = "feature"
    story.id = 1
    story.title = "branch-name"

    return story


@pytest.fixture
def repo() -> git.Repo:
    return mock.Mock(git.Repo)


def test_make_branch(repo: git.Repo, story: Story):
    actual_branch_name = make_branch(repo, story)

    expected_branch_name = f"disco/{story.type}/{story.id}-branch-name"
    repo.git.checkout.assert_called_with("-b", expected_branch_name)
    assert actual_branch_name == expected_branch_name


def test_make_branch_sanitize_branch_name(repo: git.Repo, story: Story):
    story.title = (
        "branch-name with [[brackets]]  space  and::colons__underline's"
    )

    actual_branch_name = make_branch(repo, story)

    expected_branch_name = f"disco/{story.type}/{story.id}-branch-name-with-brackets-space-and-colons-underlines"
    repo.git.checkout.assert_called_with("-b", expected_branch_name)
    assert actual_branch_name == expected_branch_name
