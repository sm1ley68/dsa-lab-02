"""
Бронзовый уровень. Реализация односвязного списка.
"""


class Node:
    """Узел односвязного списка."""

    def __init__(self, data, next_node=None):
        self.data = data
        self.next = next_node

    def __repr__(self):
        return f"Node({self.data!r})"


class SinglyLinkedList:
    """Односвязный список."""

    def __init__(self, iterable=None):
        self.head = None
        self._size = 0
        if iterable is not None:
            for item in iterable:
                self.append(item)

    def prepend(self, data):
        """Добавляет элемент в начало. O(1)."""
        self.head = Node(data, self.head)
        self._size += 1

    def append(self, data):
        """Добавляет элемент в конец. O(n) (без tail)."""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._size += 1

    def find(self, data):
        """Ищет узел по значению. O(n). Возвращает Node или None."""
        current = self.head
        while current is not None:
            if current.data == data:
                return current
            current = current.next
        return None

    def delete(self, data):
        """Удаляет первый узел с заданным значением. O(n)."""
        if self.head is None:
            return
        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return
        current = self.head
        while current.next is not None and current.next.data != data:
            current = current.next
        if current.next is None:
            return
        current.next = current.next.next
        self._size -= 1

    def get(self, index):
        """Возвращает элемент по индексу. O(n).

        Нужен для золотого уровня: именно здесь видно, чем связный список
        проигрывает массиву — до нужного узла приходится дойти по ссылкам.
        """
        if not (0 <= index < self._size):
            raise IndexError("Index out of bounds")
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data

    def __len__(self):
        return self._size

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.data
            current = current.next

    def __str__(self):
        if self.head is None:
            return "None"
        result = []
        current = self.head
        while current is not None:
            result.append(str(current.data))
            current = current.next
        return " -> ".join(result) + " -> None"

    def __repr__(self):
        return f"SinglyLinkedList([{', '.join(repr(x) for x in self)}])"
