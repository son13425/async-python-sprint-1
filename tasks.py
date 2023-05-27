import logging
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from multiprocessing import Manager, Process
from multiprocessing.process import AuthenticationString
from time import perf_counter
from typing import Any, List

from external.analyzer import analyze_json
from external.client import YandexWeatherAPI
from external.combining import combining_data
from external.ratinger import rating
from external.table import creating_field_table, creating_table
from utils import CITIES, get_url_by_city_name

CITIES_LIST = list(CITIES.keys())


class DataFetchingTask:
    """получение данных через API"""
    def __init__(self):
        super().__init__()

    def parse(self, city: str) -> dict:
        logging.info('Начинаю читать данные из url для города: %s', city)
        url_with_data = get_url_by_city_name(city)
        if url_with_data:
            response = YandexWeatherAPI.get_forecasting(url_with_data)
            if response:
                response['city'] = city
                logging.info('Закончил работу с url для города: %s', city)
                return response
            else:
                logging.error(
                    'ERROR 404 Not Found для города: %s', city)
        else:
            logging.error(
                'Пожалуйста, проверьте существование города: %s',
                city
            )


class DataCalculationTask(Process):
    """Вычисление погодных параметров для одного города"""
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self, data: dict) -> dict:
        city = data['city']
        logging.info('Анализирую данные для города: %s', city)
        data_calc = analyze_json(data)
        data_calc['city'] = city
        logging.info('Закончил анализ данных для города: %s', city)
        self.queue.put(data_calc)
        logging.info('Отправлены в очередь данные для города: %s', city)
        return data_calc

    def __getstate__(self):
        """
        позволяет запускать подпроцессы без того,
        чтобы строка аутентификации вызывала ошибку
        """
        state = self.__dict__.copy()
        conf = state['_config']
        if 'authkey' in conf:
            conf['authkey'] = bytes(conf['authkey'])
        return state

    def __setstate__(self, state):
        """для распаковки"""
        state['_config']['authkey'] = AuthenticationString(
            state['_config']['authkey']
        )
        self.__dict__.update(state)


class DataAggregationTask(DataCalculationTask):
    """
    Объединение вычисленных данных и расчет
    средних параметров для одного города
    """
    def run(self, int: int) -> dict:
        while True:
            if self.queue.empty():
                logging.error(
                    'Нет данных для расчета средних значений параметров'
                )
                break
            else:
                item = self.queue.get()
                city = item['city']
                logging.info(
                    'Из очереди получены данные для расчета средних значений '
                    'параметров для города: %s', city
                )
                logging.info(
                    'Вычисляю средние значения параметров для города: %s',
                    city
                )
                data = combining_data(item)
                logging.info(
                    'Закончил расчет средних значений параметров для города: '
                    '%s', city
                )
                return data


class DataAnalyzingTask:
    """Финальный анализ и получение результата"""
    def __init__(self):
        super().__init__()

    def run(self, data: List[tuple[dict, List[Any]]]) -> None:
        table_body = rating(data)
        return table_body


if __name__ == '__main__':
    format = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    datefmt = '%H:%M:%S'
    logging.basicConfig(
        format=format,
        level=logging.INFO,
        datefmt=datefmt,
        filename='application-log.log',
        filemode='w'
    )
    start = perf_counter()
    logging.info('Создаю пул для парсинга данных для списка городов')
    with ThreadPoolExecutor() as pool:
        func = DataFetchingTask()
        list_data = list(pool.map(func.parse, CITIES_LIST))
    list_data = list(filter(lambda city: city is not None, list_data))
    table_field = creating_field_table(list_data[0])
    logging.info('Завершен парсинг данных для списка городов')
    logging.info(
        'Запускаю мультипроцесс расчета средних значений параметров за период'
    )
    logging.info('Создаю очередь данных')
    queue = Manager().Queue()
    with ProcessPoolExecutor() as executor:
        process_producer = DataCalculationTask(queue)
        data_by_day = list(executor.map(process_producer.run, list_data))
        n = queue.qsize()
        process_consumer = DataAggregationTask(queue)
        results_list = list(executor.map(process_consumer.run, range(n)))
    logging.info(
        'Завершен расчет итоговых средних параметров для списка городов'
    )
    table_body = DataAnalyzingTask().run(results_list)
    logging.info('Формирую итоговую таблицу')
    creating_table(table_field, table_body)
    finish = perf_counter()
    logging.info(f'Выполнение заняло {finish-start} секунд.')
