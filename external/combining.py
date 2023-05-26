import logging
from typing import Any, List
from .table import creating_body_table


def combining_data(data: dict) -> tuple[dict, List[Any]]:
    """Расчет средних значений за период"""
    if not data:
        logging.warning("Input data is empty...")
        return {}
    rows_table = creating_body_table(data)
    data_list = data["days"]
    city = data["city"]
    list_item = []
    for index in range(len(data_list)):
        if data_list[index]['hours_count'] != 0:
            list_item.append(data_list[index])
    count_day = len(list_item)
    if count_day > 0:
        temp_sum = 0
        cond_sum = 0
        for data in list_item:
            temp_sum += data["temp_avg"]
            cond_sum += data["relevant_cond_hours"]
        temp_avg = round(temp_sum / count_day, 1)
        cond_avg = round(cond_sum / count_day, 1)
        data = {
            "city": city,
            "temp_avg": temp_avg,
            "cond_avg": cond_avg
        }
        rows_table[0].append(temp_avg)
        rows_table[1].append(cond_avg)
        rows_table[1].append('')
        logging.info(
            "Сформировано тело итоговой таблицы для города: %s", city
        )
        return (data, rows_table)
