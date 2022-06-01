import re

import pytest
from exception import StoryNotFound
from pivotal_tracker import PivotalTracker
from pivotal_tracker.story import Story


@pytest.fixture
def pt() -> PivotalTracker:
    return PivotalTracker(str(123), str(123))


@pytest.mark.parametrize(
    "story_id,expected_id,expected_title,expected_type",
    ([1, 1, "Story name", "feature"], [1, 1, "Story name 3", "bug"]),
)
def test_get_story(
    requests_mock,
    pt: PivotalTracker,
    story_id: int,
    expected_id: int,
    expected_title: str,
    expected_type: str,
):
    requests_mock.get(
        re.compile(
            rf"https:\/\/www.pivotaltracker.com/(.*)/stories/{story_id}"
        ),
        json={
            "id": expected_id,
            "name": expected_title,
            "story_type": expected_type,
        },
    )

    story = pt.get_story(story_id)

    assert isinstance(story, Story)
    assert story.id == expected_id
    assert story.title == expected_title
    assert story.type == expected_type


def test_not_found_story(requests_mock, pt: PivotalTracker):
    requests_mock.get(
        re.compile(r"https:\/\/www.pivotaltracker.com/(.*)/stories/11"),
        status_code=404,
        text="Story not found",
    )

    with pytest.raises(StoryNotFound):
        pt.get_story(11)
