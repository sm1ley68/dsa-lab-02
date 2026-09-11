"""
Динамический массив — оппонент связного списка в экспериментах золотого уровня.

Смысл структуры: элементы лежат в одном непрерывном блоке памяти фиксированной
ёмкости. Отсюда и сильные, и слабые стороны:
  * доступ по индексу — O(1) (адрес считается арифметикой);
  * вставка/удаление в начале — O(n) (нужно сдвинуть весь «хвост»);
  * append — O(1) амортизированно (изредка происходит перевыделение с ростом x2).
"""


class DynamicArray:
    """Динамический массив с удвоением ёмкости."""

    INITIAL_CAPACITY = 4
    GROWTH_FACTOR = 2

    def __init__(self, iterable=None):
        self._capacity = self.INITIAL_CAPACITY
        self._size = 0
        # Список фиксированной длины играет роль сырого блока памяти:
        # обращаться к нему разрешено только по индексам < self._capacity.
        self._data = [None] * self._capacity
        self._resize_count = 0
        if iterable is not None:
            for item in iterable:
                self.append(item)

    def _resize(self, new_capacity):
        """Выделяет новый блок и копирует в него элементы. O(n)."""
        new_data = [None] * new_capacity
        new_data[: self._size] = self._data[: self._size]
        self._data = new_data
        self._capacity = new_capacity
        self._resize_count += 1

    def _ensure_capacity(self):
        if self._size == self._capacity:
            self._resize(self._capacity * self.GROWTH_FACTOR)

    def append(self, value):
        """Добавляет элемент в конец. O(1) амортизированно."""
        self._ensure_capacity()
        self._data[self._size] = value
        self._size += 1

    def insert(self, index, value):
        """Вставляет элемент по индексу. O(n) — сдвиг хвоста вправо."""
        if not (0 <= index <= self._size):
            raise IndexError("Index out of bounds")
        self._ensure_capacity()
        # Сдвиг «хвоста» на одну позицию вправо. Присваивание срезом — это ровно
        # тот же memmove непрерывного блока, который делает настоящий
        # динамический массив в C: объём работы линеен по числу сдвигаемых
        # элементов, просто выполняется без интерпретаторных накладных расходов.
        self._data[index + 1 : self._size + 1] = self._data[index : self._size]
        self._data[index] = value
        self._size += 1

    def pop(self, index=None):
        """Удаляет элемент по индексу (по умолчанию последний). O(n), с конца O(1)."""
        if self._size == 0:
            raise IndexError("pop from empty array")
        if index is None:
            index = self._size - 1
        if not (0 <= index < self._size):
            raise IndexError("Index out of bounds")
        value = self._data[index]
        self._data[index : self._size - 1] = self._data[index + 1 : self._size]
        self._data[self._size - 1] = None
        self._size -= 1
        return value

    def get(self, index):
        """Возвращает элемент по индексу. O(1)."""
        if not (0 <= index < self._size):
            raise IndexError("Index out of bounds")
        return self._data[index]

    def set(self, index, value):
        """Записывает элемент по индексу. O(1)."""
        if not (0 <= index < self._size):
            raise IndexError("Index out of bounds")
        self._data[index] = value

    def find(self, value):
        """Ищет индекс первого совпадения. O(n). Возвращает индекс или None."""
        for i in range(self._size):
            if self._data[i] == value:
                return i
        return None

    def delete(self, value):
        """Удаляет первое вхождение значения. O(n)."""
        index = self.find(value)
        if index is not None:
            self.pop(index)

    @property
    def capacity(self):
        """Текущая ёмкость выделенного блока."""
        return self._capacity

    @property
    def resize_count(self):
        """Сколько раз массив перевыделял память."""
        return self._resize_count

    def __getitem__(self, index):
        return self.get(index)

    def __setitem__(self, index, value):
        self.set(index, value)

    def __len__(self):
        return self._size

    def __iter__(self):
        for i in range(self._size):
            yield self._data[i]

    def __str__(self):
        return "[" + ", ".join(str(x) for x in self) + "]"

    def __repr__(self):
        return f"DynamicArray([{', '.join(repr(x) for x in self)}])"
