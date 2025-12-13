from datetime import datetime
import os
from functools import wraps


def logger_1(old_function):
    """Декоратор без аргументов для логирования вызовов функций"""

    @wraps(old_function)
    def new_function(*args, **kwargs):
        datetime_ = datetime.now()
        name = old_function.__name__
        if args:
            args_str = ', '.join(str(arg) for arg in args)
        else:
            args_str = 'Нет'
        if kwargs:
            kwargs_str = ', '.join(f'{key}={value}' for key, value in kwargs.items())
        else:
            kwargs_str = 'Нет'

        result = old_function(*args, **kwargs)

        with open('main.log', 'a', encoding='utf-8') as log_file:
            log_file.write(f"Дата и время: '{datetime_}'\n"
                           f"Имя функции: '{name}'\n"
                           f"Позиционные аргументы: '{args_str}'\n"
                           f"Именованные аргументы: '{kwargs_str}'\n"
                           f"Результат: '{result}'\n\n")
        return result

    return new_function


def logger_2(path):
    """Декоратор с аргументом для логирования вызовов функций"""

    @wraps(path)
    def logger_1(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            datetime_ = datetime.now()
            name = old_function.__name__
            if args:
                args_str = ', '.join(str(arg) for arg in args)
            else:
                args_str = 'Нет'
            if kwargs:
                kwargs_str = ', '.join(f'{key}={value}' for key, value in kwargs.items())
            else:
                kwargs_str = 'Нет'

            result = old_function(*args, **kwargs)

            with open(path, 'a', encoding='utf-8') as log_file:
                log_file.write(f"Дата и время: '{datetime_}'\n"
                               f"Имя функции: '{name}'\n"
                               f"Позиционные аргументы: '{args_str}'\n"
                               f"Именованные аргументы: '{kwargs_str}'\n"
                               f"Результат: '{result}'\n\n")
            return result

        return new_function

    return logger_1


# Tests:
def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger_1
    def hello_world():
        return 'Hello World'

    @logger_1
    def summator(a, b=0):
        return a + b

    @logger_1
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'
    assert os.path.exists(path), 'файл main.log должен существовать'
    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path, encoding='utf-8') as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'

    print("Test 1 OK")


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger_2(path)
        def hello_world():
            return 'Hello World'

        @logger_2(path)
        def summator(a, b=0):
            return a + b

        @logger_2(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path, encoding='utf-8') as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'

    print("Test 2 OK")


if __name__ == '__main__':
    test_1()
    test_2()
