import json
import logging
from http import HTTPStatus
from urllib.request import urlopen

from utils import get_key

ERR_MESSAGE_TEMPLATE = 'Unexpected error: {error}'


logger = logging.getLogger()


class YandexWeatherAPI:
    """
    Base class for requests
    """
    def __init__(self):
        super().__init__()

    def __do_req(self, url: str) -> str:
        """Base request method"""
        city = get_key(url)
        try:
            with urlopen(url) as response:
                if response.status == HTTPStatus.OK:
                    resp_body = response.read().decode('utf-8')
                    if resp_body:
                        try:
                            data = json.loads(resp_body)
                            return data
                        except Exception:
                            logging.error(
                                'Некорректные данные для города: %s',
                                city
                            )
        except Exception:
            logging.error(
                'Некорректный url для города: %s',
                city
            )

    @staticmethod
    def get_forecasting(url: str):
        """
        :param url: url_to_json_data as str
        :return: response data as json
        """
        return YandexWeatherAPI().__do_req(url)
