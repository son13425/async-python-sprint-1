CITIES = {
    'MOSCOW': 'https://code.s3.yandex.net/async-module/moscow-response.json',
    'PARIS': 'https://code.s3.yandex.net/async-module/paris-response.json',
    'LONDON': 'https://code.s3.yandex.net/async-module/london-response.json',
    'BERLIN': 'https://code.s3.yandex.net/async-module/berlin-response.json',
    'BEIJING': 'https://code.s3.yandex.net/async-module/beijing-response.json',
    'KAZAN': 'https://code.s3.yandex.net/async-module/kazan-response.json',
    'SPETERSBURG': (
        'https://code.s3.yandex.net/async-module/spetersburg-response.json'
    ),
    'VOLGOGRAD': (
        'https://code.s3.yandex.net/async-module/volgograd-response.json'
    ),
    'NOVOSIBIRSK': (
        'https://code.s3.yandex.net/async-module/novosibirsk-response.json'
    ),
    'KALININGRAD': (
        'https://code.s3.yandex.net/async-module/kaliningrad-response.json'
    ),
    'ABUDHABI': (
        'https://code.s3.yandex.net/async-module/abudhabi-response.json'
    ),
    'ABUDHABI-2': (
        'https://code.s3.yandex.net/async-module/abudhabi-response.json'
    ),
    'WARSZAWA': (
        'https://code.s3.yandex.net/async-module/warszawa-response.json'
    ),
    'BUCHAREST': (
        'https://code.s3.yandex.net/async-module/bucharest-response.json'
    ),
    'ROMA': 'https://code.s3.yandex.net/async-module/roma-response.json',
    'CAIRO': 'https://code.s3.yandex.net/async-module/cairo-response.json',
    'GIZA': 'https://code.s3.yandex.net/async-module/giza-response.json',
    'MADRID': 'https://code.s3.yandex.net/async-module/madrid-response.json',
    'TORONTO': 'https://code.s3.yandex.net/async-module/toronto-response.json'
}

MIN_MAJOR_PYTHON_VER = 3
MIN_MINOR_PYTHON_VER = 9


def check_python_version():
    """Проверяет используемую версию пайтона"""
    import sys
    major = sys.version_info.major
    minor = sys.version_info.minor
    if (major < MIN_MAJOR_PYTHON_VER or minor < MIN_MINOR_PYTHON_VER):
        raise Exception(
            'Please use python version >= {}.{}'.format(
                MIN_MAJOR_PYTHON_VER, MIN_MINOR_PYTHON_VER
            )
        )


def get_url_by_city_name(city_name: str) -> str:
    """Возвращает значение словаря CITIES по ключу"""
    if city_name in CITIES:
        return CITIES[city_name]


def get_key(value_res: str) -> str:
    """Возвращает ключ словаря CITIES по значению"""
    if value_res in CITIES.values():
        for key, value in CITIES.items():
            if value_res == value:
                return key


def gluing_two_numbers_hex_format(junior, senior):
    """Склеивание двух чисел в формате hex в python"""
    result = int(junior, 16)
    result += int(senior, 16) << 16
    number_hex = int(hex(result), 0)
    return number_hex

# def main():
#     shift=16
#     result=0x614E
#     print(type(result))
#     result += 0x00BC << shift
#     print(hex(result))
#     print(int.from_bytes(b'\x00\xbc\x61\x4e', 'big'))
#     print(int(hex(result), 0))
