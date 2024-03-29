import logging
from typing import Any, List, Dict, Tuple


def quicksort(
    list_cities: List[Tuple[Any, ...]],
    start: int,
    end: int
) -> List[Tuple[Any, ...]]:
    """Быстрая сортировка списка городов"""
    if end - start > 1:
        pivot = partition(list_cities, start, end)
        quicksort(list_cities, start, pivot)
        quicksort(list_cities, pivot + 1, end)
    return list_cities


def partition(
    list_cities: List[Tuple[Any, ...]],
    start: int,
    end: int
) -> int:
    """Расчет значения pivot для быстрой сортировки городов"""
    pivot = list_cities[start]
    left = start + 1
    right = end - 1
    while True:
        while left <= right and list_cities[left] <= pivot:
            left = left + 1
        while left <= right and list_cities[right] >= pivot:
            right = right - 1
        if left <= right:
            list_cities[left], list_cities[right] = (
                list_cities[right],
                list_cities[left]
            )
        else:
            list_cities[start], list_cities[right] = (
                list_cities[right],
                list_cities[start]
            )
            return right


def rating(
    cities: List[Tuple[Dict[Any, Any], Tuple[List[Any], List[Any]]]]
) -> List[List[Any]]:
    """Формирование рейтинга «благоприятности поездки»"""
    cities_list = []
    table_body = []
    for city in cities:
        cities_list.append(city[0])
        table_body.append(city[1][0])
        table_body.append(city[1][1])
    start = 0
    end = len(cities_list)
    list_cities: List[Tuple[Any, ...]] = []
    for data in cities_list:
        temp_avg = data['temp_avg']
        cond_avg = data['cond_avg']
        city_name = data['city']
        city_tuple = ((-temp_avg), -cond_avg, city_name)
        list_cities.append(city_tuple)
    logging.info('Выполняю сортировку списка городов')
    list_sort = quicksort(list_cities, start, end)
    logging.info('Закончил сортировку списка городов')
    logging.info('Составляю рейтинг «благоприятности поездки»')
    rating = [[list_sort[0][2]]]
    for index in range(1, len(list_sort)):
        if (
            list_sort[index][0] == list_sort[0][0]
            and list_sort[index][1] == list_sort[0][1]
        ):
            rating[0].append(list_sort[index][2])
        else:
            rating.append(list_sort[index][2])
    logging.info('Составлен рейтинг «благоприятности поездки»')
    logging.info(
        ('Наиболее благоприятный для поездки город: ' + '{}, ' * len(
            rating[0]
        )).format(*rating[0])
    )
    print(
        ('Наиболее благоприятный для поездки город: ' + '{}, ' * len(
            rating[0]
        )).format(*rating[0]))
    for item in table_body:
        if item[0] in rating[0]:
            item.append(1)
        if item[0] in rating[1::]:
            item.append(rating.index(item[0]) + 1)
    return table_body
