from datetime import timedelta

from src.channel import YouTubeObject
from src.video import Video


class PlayList(YouTubeObject):
    def __init__(self, pl_id: str):
        self.__pl_id = pl_id
        self.__url = f'https://www.youtube.com/playlist?list={pl_id}'

        pl = self.get_service().playlists().list(id=pl_id,
                                                 part='snippet',
                                                 maxResults=50,
                                                 ).execute()

        self.__title = pl['items'][0]['snippet']['title']
        self.__description = pl['items'][0]['snippet']['description']

    @property
    def pl_id(self):
        return self.__pl_id

    @property
    def title(self):
        return self.__title

    @property
    def url(self):
        return self.__url

    @property
    def total_duration(self) -> timedelta:
        videos = self.videos_list()
        pl_duration: timedelta = timedelta()
        for video in videos:
            pl_duration += video.duration
        return pl_duration

    def show_best_video(self) -> str:
        videos = self.videos_list()
        best_video = max(videos, key=lambda video: video.like_count)
        return best_video.url

    def videos_list(self) -> list[Video]:
        # ['items'][0]['contentDetails']['video_id']
        pl_videos = self.get_service().playlistItems().list(playlistId=self.pl_id,
                                                            part='contentDetails',
                                                            maxResults=100,
                                                            ).execute()
        videos = []
        for item in pl_videos['items']:
            video_id = item['contentDetails']['videoId']
            videos.append(Video(video_id))
        return videos
