import unittest
from multiprocessing import Manager

from external.client import YandexWeatherAPI
from external.combining import combining_data
from external.ratinger import partition, quicksort, rating
from external.table import creating_body_table, creating_field_table
from external.tests_data import (analiz_data, avg_data, avg_data_list,
                                 data_sort, list_sort, list_sort_for_sort,
                                 start_data, table_body, table_body_first,
                                 table_body_itog, table_body_rating,
                                 table_field)
from tasks import (DataAggregationTask, DataAnalyzingTask, DataCalculationTask,
                   DataFetchingTask)
from utils import get_key, get_url_by_city_name


class MyTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print('Тесты запущены')

    @classmethod
    def tearDownClass(cls) -> None:
        print('Тесты успешно пройдены')

    def setUp(self) -> None:
        print('Тестирую...')

    def tearDown(self) -> None:
        print('Успешно!')

    def test_class_datafetchingtask(self):
        self.assertEqual(
            DataFetchingTask().parse('TORONTO'),
            None,
        )

    def test_with_error_datafetchingtask(self):
        self.assertEqual(
            DataFetchingTask().parse('PARIS'),
            None,
            msg='Данные не соответствуют ожиданию'
        )

    def test_class_for_queue(self):
        queue = Manager().Queue()
        self.assertEqual(
            DataCalculationTask(queue).run(start_data),
            analiz_data
        )
        self.assertEqual(
            DataAggregationTask(queue).run(1),
            avg_data
        )

    def test_with_error_for_queue_put(self):
        queue = Manager().Queue()
        self.assertEqual(
            DataCalculationTask(queue).run(start_data),
            avg_data,
            msg='Данные не соответствуют ожиданию'
        )

    def test_with_error_for_queue_get(self):
        queue = Manager().Queue()
        self.assertEqual(
            DataCalculationTask(queue).run(start_data),
            analiz_data
        )
        self.assertEqual(
            DataAggregationTask(queue).run(analiz_data),
            table_body,
            msg='Данные не соответствуют ожиданию'
        )

    def test_class_dataanalyzingtask(self):
        self.assertEqual(
            DataAnalyzingTask().run(avg_data_list),
            table_body_rating
        )

    def test_with_error_dataanalyzingtask(self):
        self.assertEqual(
            DataAnalyzingTask().run(avg_data_list),
            analiz_data,
            msg='Данные не соответствуют ожиданию'
        )

    def test_func_dict_get_url(self):
        self.assertEqual(
            get_url_by_city_name('TORONTO'),
            'https://code.s3.yandex.net/async-module/toronto-response.json'
        )

    def test_with_error_dict_get_url(self):
        self.assertEqual(
            get_url_by_city_name('TORONTO'),
            'https://code.s3.yandex.net/async-module/giza-response.json',
            msg='Данные не соответствуют ожиданию'
        )

    def test_func_dict_get_key(self):
        self.assertEqual(
            get_key(
                'https://code.s3.yandex.net/async-module/giza-response.json'
            ),
            'GIZA'
        )

    def test_with_error_dict_get_key(self):
        self.assertEqual(
            get_key(
                'https://code.s3.yandex.net/async-module/giza-response.json'
            ),
            'TORONTO',
            msg='Данные не соответствуют ожиданию'
        )

    def test_creating_field_table(self):
        self.assertEqual(
            creating_field_table(start_data),
            table_field
        )

    def test_with_error_creating_field_table(self):
        self.assertEqual(
            creating_field_table(start_data),
            ['Город/День', '', 'Среднее', 'Рейтинг'],
            msg='Данные не соответствуют ожиданию'
        )

    def test_creating_body_table(self):
        self.assertEqual(
            creating_body_table(analiz_data),
            table_body_first
        )

    def test_with_error_creating_body_table(self):
        self.assertEqual(
            creating_body_table(analiz_data),
            table_body,
            msg='Данные не соответствуют ожиданию'
        )

    def test_quicksort(self):
        self.assertEqual(
            quicksort(list_sort_for_sort, 0, 3),
            list_sort
        )

    def test_with_error_quicksort(self):
        self.assertEqual(
            quicksort(list_sort_for_sort, 0, 3),
            [(1, ), (2, ), (3, )],
            msg='Данные не соответствуют ожиданию'
        )

    def test_partition(self):
        self.assertEqual(
            partition(list_sort_for_sort, 0, 3),
            0
        )

    def test_with_error_partition(self):
        self.assertEqual(
            partition(list_sort_for_sort, 0, 3),
            2,
            msg='Данные не соответствуют ожиданию'
        )

    def test_rating(self):
        self.assertEqual(
            rating(data_sort),
            table_body_itog
        )

    def test_with_error_rating(self):
        self.assertEqual(
            rating(data_sort),
            [],
            msg='Данные не соответствуют ожиданию'
        )

    def test_combining_data(self):
        self.assertEqual(
            combining_data(analiz_data),
            avg_data
        )

    def test_with_error_combining_data(self):
        self.assertEqual(
            combining_data(analiz_data),
            avg_data_list,
            msg='Данные не соответствуют ожиданию'
        )

    def test_get_forecasting(self):
        self.assertEqual(
            YandexWeatherAPI().get_forecasting(
                'https://code.s3.yandex.net/async-module/moscow-response.json'
            ),
            start_data
        )

    def test_with_error_get_forecasting(self):
        self.assertEqual(
            YandexWeatherAPI().get_forecasting(
                'https://code.s3.yandex.net/async-module/moscow-response.json'
            ),
            {},
            msg='Данные не соответствуют ожиданию'
        )


if __name__ == '__main__':
    unittest.main()
