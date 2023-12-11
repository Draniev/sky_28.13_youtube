from datetime import timedelta

from isodate import parse_duration

from src.channel import YouTubeObject
from src.utils import printj


class Video(YouTubeObject):
    def __init__(self, video_id: str) -> None:
        self.__video_id = video_id

        video = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                 id=video_id
                                                 ).execute()
        try:
            video_item = video['items'][0]
            self.__url = f'https://youtu.be/{video_id}'
            self.__title = video_item['snippet']['title']
            self.__description = video_item['snippet']['description']
            self.__video_title: str = video_item['snippet']['title']
            self.__view_count: int = video_item['statistics']['viewCount']
            self.__like_count: int = video_item['statistics']['likeCount']
            self.__comment_count: int = video_item['statistics']['commentCount']
            self.__duration_iso8601 = video_item['contentDetails']['duration']
        except IndexError:
            self.__url = None
            self.__title = None
            self.__description = None
            self.__video_title = None
            self.__view_count = None
            self.__like_count = None
            self.__comment_count = None
            self.__duration_iso8601 = None

    @property
    def title(self):
        return self.__title

    @property
    def like_count(self):
        return self.__like_count

    @property
    def duration(self) -> timedelta:
        return parse_duration(self.__duration_iso8601)

    @property
    def url(self):
        return self.__url

    def __str__(self) -> str:
        return self.title


class PLVideo(Video):
    def __init__(self, video_id: str, pl_id: str) -> None:
        super().__init__(video_id)
        self.__pl_id = pl_id
