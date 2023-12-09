import json

from googleapiclient.discovery import build

from src.utils import printj


class Channel:
    """Класс для ютуб-канала"""
    __youtube = None

    def __new__(cls, *args, **kwargs):
        if cls.__youtube is None:
            raise Exception('Объект не инициализирован! Нужен Апи ключ.')
        return super().__new__(cls)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.__channel_id = channel_id
        channel = self.get_service().channels().list(
            id=self.__channel_id, part='snippet,statistics').execute()
        self.__title = channel['items'][0]['snippet']['title']
        self.__description = channel['items'][0]['snippet']['description']
        self.__url = f'https://www.youtube.com/channel/{channel_id}'
        self.__video_count = channel['items'][0]['statistics']['videoCount']
        self.__view_count = channel['items'][0]['statistics']['viewCount']
        self.__subscriber_count = channel['items'][0]['statistics']['subscriberCount']

    @classmethod
    def init_api(cls, youtube_api: str):
        print('Инициализирую ютуб')
        cls.__youtube = build('youtube', 'v3',
                              developerKey=youtube_api)
        print(f'Объект ютуба: {cls.__youtube}')

    @classmethod
    def get_service(cls):
        return cls.__youtube

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        return self.__title

    @property
    def description(self):
        return self.__description

    @property
    def url(self):
        return self.__url

    @property
    def video_count(self):
        return self.__video_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.get_service().channels().list(
            id=self.__channel_id, part='snippet,statistics').execute()
        printj(channel)

    def to_json(self, filename: str):
        data = {
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'video_count': self.video_count,
        }

        with open(filename, 'w') as file:
            json.dump(data, file)
