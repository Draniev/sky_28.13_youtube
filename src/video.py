from datetime import timedelta
from src.channel import YouTubeObject
from isodate import parse_duration


class Video(YouTubeObject):
    def __init__(self, video_id: str) -> None:
        self.__video_id = video_id
        self.__url = f'https://youtu.be/{video_id}'

        video = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                 id=video_id
                                                 ).execute()
        self.__title = video['items'][0]['snippet']['title']
        self.__description = video['items'][0]['snippet']['description']
        self.__video_title: str = video['items'][0]['snippet']['title']
        self.__view_count: int = video['items'][0]['statistics']['viewCount']
        self.__like_count: int = video['items'][0]['statistics']['likeCount']
        self.__comment_count: int = video['items'][0]['statistics']['commentCount']
        self.__duration_iso8601 = video['items'][0]['contentDetails']['duration']

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
