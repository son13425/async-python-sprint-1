import unittest
from multiprocessing import Manager

from tasks import (
    DataFetchingTask,
    DataCalculationTask,
    DataAggregationTask,
    DataAnalyzingTask)
from external.tests_data import start_data, analiz_data, avg_data, table_body


class MyTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("Тесты запущены")

    @classmethod
    def tearDownClass(cls) -> None:
        print("Тесты успешно пройдены")

    def setUp(self) -> None:
        print("Тестирую...")

    def tearDown(self) -> None:
        print("Успешно!")

    def test_simple(self):
        self.assertEqual(DataFetchingTask().parse("TORONTO"), None)
        queue = Manager().Queue()
        self.assertEqual(
            DataCalculationTask(queue).run(start_data),
            analiz_data
        )
        self.assertEqual(DataAggregationTask(queue).run(1), avg_data)
        self.assertEqual(DataAnalyzingTask().run(avg_data), table_body)

    def test_with_error(self):
        self.assertEqual(
            DataFetchingTask().parse("PARIS"),
            None,
            msg="Данные не соответствуют ожиданию"
        )
        self.assertEqual(
            DataCalculationTask().run(start_data),
            avg_data,
            msg="Данные не соответствуют ожиданию"
        )
        self.assertEqual(
            DataAggregationTask().run(analiz_data),
            table_body,
            msg="Данные не соответствуют ожиданию"
        )
        self.assertEqual(
            DataAnalyzingTask().run(avg_data),
            analiz_data,
            msg="Данные не соответствуют ожиданию"
        )


if __name__ == "__main__":
    unittest.main()
