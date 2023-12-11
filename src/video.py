from src.channel import YouTubeObject


class Video(YouTubeObject):
    def __init__(self, video_id: str) -> None:
        self.__video_id = video_id

        video = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                 id=video_id
                                                 ).execute()
        self.__title = video['items'][0]['snippet']['title']
        self.__description = video['items'][0]['snippet']['description']
        self.__url = f'https://www.youtube.com/watch?v={video_id}'
        self.__video_title: str = video['items'][0]['snippet']['title']
        self.__view_count: int = video['items'][0]['statistics']['viewCount']
        self.__like_count: int = video['items'][0]['statistics']['likeCount']
        self.__comment_count: int = video['items'][0]['statistics']['commentCount']

    @property
    def title(self):
        return self.__title

    def __str__(self) -> str:
        return self.title


class PLVideo(Video):
    def __init__(self, video_id: str, pl_id: str) -> None:
        super().__init__(video_id)
        self.__pl_id = pl_id
