import json
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build
from uritemplate import api

from src.utils import printj


class YouTubeObject:
    __youtube = None

    def __new__(cls, *args, **kwargs):
        if cls.__youtube is None:
            is_load = load_dotenv()
            if not is_load:
                print('Загрузить переменные среды не вышло!')
                raise FileNotFoundError

            api_key = os.getenv('YT_API_KEY')
            if api_key is None:
                print('Загрузить АПИ ключ не вышло!')
                raise ValueError('Загрузить АПИ ключ не вышло!')
            cls.init_api(api_key)
            # raise Exception('Объект не инициализирован! Нужен Апи ключ.')
        return super().__new__(cls)

    @classmethod
    def init_api(cls, youtube_api: str):
        print('Инициализирую ютуб')
        cls.__youtube = build('youtube', 'v3',
                              developerKey=youtube_api)
        print(f'Объект ютуба: {cls.__youtube}')

    @classmethod
    def get_service(cls):
        return cls.__youtube


class Channel(YouTubeObject):
    """Класс для ютуб-канала"""
    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.__channel_id = channel_id
        channel = self.get_service().channels().list(
            id=self.__channel_id, part='snippet,statistics').execute()
        self.__title = channel['items'][0]['snippet']['title']
        self.__description = channel['items'][0]['snippet']['description']
        self.__url = f'https://www.youtube.com/channel/{channel_id}'
        self.__video_count = int(
            channel['items'][0]['statistics']['videoCount'])
        self.__view_count = int(channel['items'][0]['statistics']['viewCount'])
        self.__subscriber_count = int(
            channel['items'][0]['statistics']['subscriberCount'])

    def __str__(self):
        return f"{self.__title} ({self.__url})"

    def __lt__(self, other):
        """ Меньше """
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        """ Меньше или Равно """
        return self.subscriber_count <= other.subscriber_count

    def __add__(self, other):
        """ ПЛЮС """
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        """ МИНУС """
        return self.subscriber_count - other.subscriber_count

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

    @property
    def view_count(self):
        return self.__view_count

    @property
    def subscriber_count(self):
        return self.__subscriber_count

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
