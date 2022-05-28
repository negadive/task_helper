from custom_logging import logger
import requests
from exception import StoryNotFound

from pivotal_tracker.story import Story

class PivotalTracker:
    def __init__(self, project_id: str, token: str) -> None:
        self._project_id = project_id
        self._token = token

    def get_story(self, story_id: str) -> Story:
        logger.info(f"Getting story with id {story_id} from project {self._project_id}")
        url = f"https://www.pivotaltracker.com/services/v5/projects/{self._project_id}/stories/{story_id}"
        story_res = requests.get(url, headers={"X-TrackerToken": self._token})

        if story_res.status_code != 200:
            raise StoryNotFound(story_res.text)

        story_json = story_res.json()

        return Story(
            id=story_json['id'],
            title=story_json['name'],
            type=story_json['story_type']
        )
