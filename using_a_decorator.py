import os
import types

from log_decorators import logger_1


@logger_1
def flat_generator(list_of_lists):
    """Генератор для прохода по списку списков (уровень вложенности 2)."""
    for sublist in list_of_lists:
        if isinstance(sublist, list):
            for item in sublist:
                yield item


@logger_1
def flat_recursive_generator(list_of_list):
    """Рекурсивный генератор, обрабатывающий списки любой вложенности."""
    for item in list_of_list:
        if isinstance(item, list):
            yield from flat_recursive_generator(item)
        else:
            yield item


def test_3():
    """Тест для flat_generator: проверка работы генератора и типа."""
    list_of_lists_1 = [["a", "b", "c"], ["d", "e", "f", "h", False], [1, 2, None]]

    for flat_iterator_item, check_item in zip(
        flat_generator(list_of_lists_1),
        ["a", "b", "c", "d", "e", "f", "h", False, 1, 2, None],
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "h",
        False,
        1,
        2,
        None,
    ]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)
    print("Test 3 OK!")


def test_4():
    """Тест для flat_recursive_generator: проверка рекурсивного генератора."""
    list_of_lists_2 = [
        [["a"], ["b", "c"]],
        ["d", "e", [["f"], "h"], False],
        [1, 2, None, [[[[["!"]]]]], []],
    ]

    for flat_iterator_item, check_item in zip(
        flat_recursive_generator(list_of_lists_2),
        ["a", "b", "c", "d", "e", "f", "h", False, 1, 2, None, "!"],
    ):
        assert flat_iterator_item == check_item

    assert list(flat_recursive_generator(list_of_lists_2)) == [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "h",
        False,
        1,
        2,
        None,
        "!",
    ]
    assert isinstance(flat_recursive_generator(list_of_lists_2), types.GeneratorType)
    print("Test 4 OK!")


if __name__ == "__main__":
    # Очистка старых логов
    log_file = "main.log"
    if os.path.exists(log_file):
        os.remove(log_file)
    # Тесты:
    test_3()
    test_4()
