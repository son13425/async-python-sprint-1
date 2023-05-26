from typing import Any, List
from prettytable import PrettyTable
import logging

from .outputs import file_output


def creating_field_table(data_item: dict) -> List[Any]:
    """Формирование шапки итоговой таблицы"""
    logging.info("Формирую шапку итоговой таблицы")
    datas_field = []
    for date in data_item['forecasts']:
        datas_field.append(date['date'])
    table_row_field = ["Город/День", "", *datas_field, "Среднее", "Рейтинг"]
    logging.info("Сформирована шапка итоговой таблицы")
    return table_row_field


def creating_body_table(list_table_body: List[dict]) -> tuple[List[Any]]:
    """Формирование тела итоговой таблицы для одного города"""
    city = list_table_body['city']
    logging.info("Формирую тело итоговой таблицы для города: %s", city)
    first_row = [city, "Температура, среднее"]
    second_row = ["", "Без осадков, часов"]
    data_by_day = list_table_body['days']
    for data in data_by_day:
        first_row.append(data['temp_avg'])
        second_row.append(data['relevant_cond_hours'])
    return (first_row, second_row)


def creating_table(field: List[Any], body: List[List[Any]]) -> None:
    """Формирование итоговой таблицы"""
    table = PrettyTable()
    table.field_names = field
    for index in range(len(body)):
        if index % 2 == 0:
            table.add_row(body[index])
        else:
            table.add_row(body[index], divider=True)
    file_output(table)
    logging.info('Итоговая таблица выведена в файл')
    print('Итоговая таблица выведена в файл в папку external/results')
