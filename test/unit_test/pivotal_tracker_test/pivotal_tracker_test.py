import unittest
from unittest import mock

import pytest
from exception import StoryNotFound
from pivotal_tracker import PivotalTracker
from pivotal_tracker.story import Story
from requests import Response


# This method will be used by the mock to replace requests.get
def mocked_requests_get(status: int, json: dict = {}, text: str = ""):
    response = mock.Mock(Response)
    response.status_code = status
    response.json = mock.Mock(return_value=json)
    response.text = text

    return response


class PivotalTrackerGetStoryTestCase(unittest.TestCase):
    @mock.patch(
        "requests.get",
        return_value=mocked_requests_get(
            200, {"id": 1, "name": "Story name", "story_type": "feature"}
        ),
    )
    def test_get_story(self, mock_get):
        pt = PivotalTracker(123, 123)
        story = pt.get_story(11)

        assert isinstance(story, Story)
        assert story.id == 1
        assert story.title == "Story name"
        assert story.type == "feature"

    @mock.patch(
        "requests.get",
        return_value=mocked_requests_get(
            200, {"id": 2, "name": "Story name 3", "story_type": "bug"}
        ),
    )
    def test_get_story2(self, mock_get):
        pt = PivotalTracker(123, 123)
        story = pt.get_story(11)

        assert isinstance(story, Story)
        assert story.id == 2
        assert story.title == "Story name 3"
        assert story.type == "bug"

    @mock.patch(
        "requests.get",
        return_value=mocked_requests_get(404, text="Story not found"),
    )
    def test_not_found_story(self, mock_get):
        pt = PivotalTracker(123, 123)

        with pytest.raises(StoryNotFound):
            pt.get_story(11)
