"""
Тесты для проверки корректности реализации списков.
Запустите этот файл, чтобы убедиться, что всё работает:

    python3 test_lists.py
"""

from singly_linked_list import SinglyLinkedList
from doubly_linked_list import DoublyLinkedList
from dynamic_array import DynamicArray


def test_singly():
    """Тесты для односвязного списка."""
    print("Проверка SinglyLinkedList...")
    sll = SinglyLinkedList()

    # Проверка prepend, append и __str__
    sll.prepend(10)
    sll.prepend(20)
    sll.append(30)
    assert str(sll) == "20 -> 10 -> 30 -> None", "Ошибка в prepend/append или __str__"
    assert len(sll) == 3, "Неправильный размер"

    # Проверка find
    assert sll.find(10) is not None, "find не находит существующий элемент"
    assert sll.find(99) is None, "find находит отсутствующий элемент"

    # Проверка delete
    sll.delete(10)
    assert str(sll) == "20 -> 30 -> None", "Ошибка в delete (удаление из середины)"
    sll.delete(20)
    assert str(sll) == "30 -> None", "Ошибка в delete (удаление головы)"
    sll.delete(30)
    assert str(sll) == "None", "Ошибка в delete (удаление последнего элемента)"
    assert len(sll) == 0, "Размер не обновился после удаления"

    print("✅ SinglyLinkedList: все тесты пройдены!")


def test_doubly():
    """Тесты для двусвязного списка."""
    print("\nПроверка DoublyLinkedList...")
    dll = DoublyLinkedList()

    # Проверка prepend, append и __str__
    dll.prepend(10)
    dll.prepend(20)
    dll.append(30)
    assert str(dll) == "20 <-> 10 <-> 30 <-> None", "Ошибка в prepend/append или __str__"
    assert len(dll) == 3, "Неправильный размер"

    # Проверка find
    assert dll.find(10) is not None, "find не находит существующий элемент"
    assert dll.find(99) is None, "find находит отсутствующий элемент"

    # Проверка delete
    dll.delete(10)
    assert str(dll) == "20 <-> 30 <-> None", "Ошибка в delete (удаление из середины)"
    dll.delete(20)
    assert str(dll) == "30 <-> None", "Ошибка в delete (удаление головы)"
    dll.delete(30)
    assert str(dll) == "None", "Ошибка в delete (удаление последнего элемента)"
    assert len(dll) == 0, "Размер не обновился после удаления"

    # Проверка reverse
    dll.prepend(10)
    dll.prepend(20)
    dll.append(30)
    dll.reverse()
    assert str(dll) == "30 <-> 10 <-> 20 <-> None", "Ошибка в reverse"

    # Проверка get
    assert dll.get(0) == 30, "get(0) вернул неправильное значение"
    assert dll.get(1) == 10, "get(1) вернул неправильное значение"
    assert dll.get(2) == 20, "get(2) вернул неправильное значение"
    try:
        dll.get(3)
        assert False, "get(3) должен был выбросить IndexError"
    except IndexError:
        pass

    print("✅ DoublyLinkedList: все тесты пройдены!")


def test_singly_edge_cases():
    """Крайние случаи односвязного списка."""
    print("\nПроверка SinglyLinkedList (крайние случаи)...")
    sll = SinglyLinkedList()

    # Пустой список
    assert str(sll) == "None", "Пустой список должен печататься как 'None'"
    assert len(sll) == 0
    assert sll.find(1) is None, "find в пустом списке должен вернуть None"
    sll.delete(1)  # не должно падать
    assert len(sll) == 0, "delete в пустом списке изменил размер"

    # Единственный элемент
    sll.append(1)
    assert str(sll) == "1 -> None", "Ошибка в append в пустой список"
    assert sll.head.next is None, "У единственного узла next должен быть None"

    # Удаление отсутствующего значения не меняет список
    sll.append(2)
    sll.delete(99)
    assert str(sll) == "1 -> 2 -> None" and len(sll) == 2, "delete удалил лишнее"

    # Удаляется только ПЕРВОЕ вхождение
    sll = SinglyLinkedList([5, 7, 5])
    sll.delete(5)
    assert str(sll) == "7 -> 5 -> None", "delete должен удалять только первое вхождение"
    assert len(sll) == 2

    # find возвращает именно узел с данными
    node = sll.find(5)
    assert node is not None and node.data == 5, "find вернул не тот узел"

    # get и выход за границы
    sll = SinglyLinkedList([10, 20, 30])
    assert [sll.get(i) for i in range(3)] == [10, 20, 30], "get вернул не те значения"
    for bad in (-1, 3):
        try:
            sll.get(bad)
            assert False, f"get({bad}) должен был выбросить IndexError"
        except IndexError:
            pass

    # Итерирование
    assert list(sll) == [10, 20, 30], "Ошибка в __iter__"

    print("✅ SinglyLinkedList: крайние случаи пройдены!")


def test_doubly_edge_cases():
    """Крайние случаи двусвязного списка: главное — целостность prev/next, head/tail."""
    print("\nПроверка DoublyLinkedList (крайние случаи)...")

    def check_links(dll):
        """Проверяет, что список связен в обе стороны и head/tail на месте."""
        if dll.head is None:
            assert dll.tail is None, "head=None, но tail не None"
            assert len(dll) == 0, "Пустой список с ненулевым размером"
            return
        assert dll.head.prev is None, "У head должен быть prev=None"
        assert dll.tail.next is None, "У tail должен быть next=None"
        forward, current = [], dll.head
        while current is not None:
            forward.append(current.data)
            if current.next is not None:
                assert current.next.prev is current, "Нарушена связь next/prev"
            current = current.next
        backward, current = [], dll.tail
        while current is not None:
            backward.append(current.data)
            current = current.prev
        assert forward == backward[::-1], "Обход вперёд и назад дают разный результат"
        assert len(dll) == len(forward), "Размер не совпадает с числом узлов"

    # Пустой список
    dll = DoublyLinkedList()
    assert str(dll) == "None"
    dll.delete(1)  # не должно падать
    check_links(dll)

    # Единственный элемент: он одновременно head и tail
    dll.append(1)
    assert dll.head is dll.tail, "Единственный узел должен быть и head, и tail"
    check_links(dll)
    dll.delete(1)
    assert dll.head is None and dll.tail is None, "После удаления head/tail не сброшены"
    check_links(dll)

    # Удаление головы и хвоста обновляет head/tail
    dll = DoublyLinkedList([1, 2, 3])
    dll.delete(1)
    assert dll.head.data == 2, "head не обновился после удаления первого элемента"
    dll.delete(3)
    assert dll.tail.data == 2, "tail не обновился после удаления последнего элемента"
    check_links(dll)

    # Удаление по ссылке — O(1)
    dll = DoublyLinkedList([1, 2, 3])
    dll.delete_node(dll.find(2))
    assert str(dll) == "1 <-> 3 <-> None", "Ошибка в delete_node"
    check_links(dll)

    # После prepend/append tail и head корректны, продолжать можно с обеих сторон
    dll = DoublyLinkedList()
    dll.prepend(2)
    dll.append(3)
    dll.prepend(1)
    assert str(dll) == "1 <-> 2 <-> 3 <-> None"
    check_links(dll)

    # reverse на пустом и одноэлементном списке
    empty = DoublyLinkedList()
    empty.reverse()
    check_links(empty)
    one = DoublyLinkedList([42])
    one.reverse()
    assert str(one) == "42 <-> None" and one.head is one.tail
    check_links(one)

    # reverse дважды возвращает исходный список, связи остаются целыми
    dll = DoublyLinkedList([1, 2, 3, 4])
    dll.reverse()
    assert str(dll) == "4 <-> 3 <-> 2 <-> 1 <-> None", "Ошибка в reverse"
    assert dll.head.data == 4 and dll.tail.data == 1, "reverse не поменял head/tail"
    check_links(dll)
    dll.reverse()
    assert str(dll) == "1 <-> 2 <-> 3 <-> 4 <-> None", "Двойной reverse не вернул исходный порядок"
    check_links(dll)

    # После reverse список остаётся рабочим
    dll.reverse()
    dll.append(0)
    dll.prepend(9)
    assert str(dll) == "9 <-> 4 <-> 3 <-> 2 <-> 1 <-> 0 <-> None", "Список сломался после reverse"
    check_links(dll)

    # get с обоих концов (внутри реализации выбирается более близкий конец)
    dll = DoublyLinkedList(range(10))
    assert [dll.get(i) for i in range(10)] == list(range(10)), "get вернул не те значения"
    assert list(reversed(dll)) == list(range(9, -1, -1)), "Ошибка в __reversed__"
    try:
        dll.get(-1)
        assert False, "get(-1) должен был выбросить IndexError"
    except IndexError:
        pass

    print("✅ DoublyLinkedList: крайние случаи пройдены!")


def test_dynamic_array():
    """Тесты для динамического массива (нужен для золотого уровня)."""
    print("\nПроверка DynamicArray...")
    arr = DynamicArray()
    assert len(arr) == 0 and str(arr) == "[]", "Ошибка в пустом массиве"

    # append и рост ёмкости
    for i in range(10):
        arr.append(i)
    assert len(arr) == 10, "Неправильный размер после append"
    assert str(arr) == "[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]", "Ошибка в append или __str__"
    assert arr.capacity >= len(arr), "Ёмкость меньше размера"
    assert arr.resize_count > 0, "Массив должен был перевыделить память"

    # доступ по индексу O(1)
    assert arr.get(0) == 0 and arr.get(9) == 9 and arr[5] == 5, "Ошибка в get"
    arr[5] = 55
    assert arr.get(5) == 55, "Ошибка в set"
    for bad in (-1, 10):
        try:
            arr.get(bad)
            assert False, f"get({bad}) должен был выбросить IndexError"
        except IndexError:
            pass

    # вставка в начало и середину
    arr = DynamicArray([1, 2, 3])
    arr.insert(0, 0)
    assert str(arr) == "[0, 1, 2, 3]", "Ошибка во вставке в начало"
    arr.insert(2, 99)
    assert str(arr) == "[0, 1, 99, 2, 3]", "Ошибка во вставке в середину"
    arr.insert(len(arr), 4)
    assert str(arr) == "[0, 1, 99, 2, 3, 4]", "Ошибка во вставке в конец"
    try:
        arr.insert(100, 1)
        assert False, "insert(100) должен был выбросить IndexError"
    except IndexError:
        pass

    # удаление
    assert arr.pop() == 4, "pop вернул не тот элемент"
    assert arr.pop(0) == 0, "pop(0) вернул не тот элемент"
    assert str(arr) == "[1, 99, 2, 3]", "Ошибка в pop"
    arr.delete(99)
    assert str(arr) == "[1, 2, 3]", "Ошибка в delete"
    arr.delete(12345)
    assert str(arr) == "[1, 2, 3]", "delete удалил лишнее"
    assert arr.find(2) == 1 and arr.find(12345) is None, "Ошибка в find"

    empty = DynamicArray()
    try:
        empty.pop()
        assert False, "pop из пустого массива должен был выбросить IndexError"
    except IndexError:
        pass

    print("✅ DynamicArray: все тесты пройдены!")


def test_structures_agree():
    """Все три структуры должны вести себя одинаково на одной последовательности операций."""
    print("\nПроверка согласованности структур...")
    reference = []
    sll, dll, arr = SinglyLinkedList(), DoublyLinkedList(), DynamicArray()

    for i in range(50):
        if i % 3 == 0:
            reference.insert(0, i)
            sll.prepend(i)
            dll.prepend(i)
            arr.insert(0, i)
        else:
            reference.append(i)
            sll.append(i)
            dll.append(i)
            arr.append(i)

    assert list(sll) == reference, "SinglyLinkedList разошёлся с эталоном"
    assert list(dll) == reference, "DoublyLinkedList разошёлся с эталоном"
    assert list(arr) == reference, "DynamicArray разошёлся с эталоном"

    for value in (0, 7, 49, 1000):
        if value in reference:
            reference.remove(value)
        sll.delete(value)
        dll.delete(value)
        arr.delete(value)

    assert list(sll) == reference, "SinglyLinkedList разошёлся после удалений"
    assert list(dll) == reference, "DoublyLinkedList разошёлся после удалений"
    assert list(arr) == reference, "DynamicArray разошёлся после удалений"
    assert len(sll) == len(dll) == len(arr) == len(reference), "Размеры разошлись"

    mid = len(reference) // 2
    assert sll.get(mid) == dll.get(mid) == arr.get(mid) == reference[mid], "get разошёлся"

    print("✅ Все три структуры дают одинаковый результат!")


if __name__ == "__main__":
    test_singly()
    test_doubly()
    test_singly_edge_cases()
    test_doubly_edge_cases()
    test_dynamic_array()
    test_structures_agree()
    print("\n🎉 Все тесты успешно завершены!")
