"""
Серебряный уровень. Реализация двусвязного списка.
"""


class DNode:
    """Узел двусвязного списка."""

    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next

    def __repr__(self):
        return f"DNode({self.data!r})"


class DoublyLinkedList:
    """Двусвязный список с head и tail."""

    def __init__(self, iterable=None):
        self.head = None
        self.tail = None
        self._size = 0
        if iterable is not None:
            for item in iterable:
                self.append(item)

    def prepend(self, data):
        """Добавляет элемент в начало. O(1)."""
        new_node = DNode(data, None, self.head)
        if self.head is None:
            self.tail = new_node
        else:
            self.head.prev = new_node
        self.head = new_node
        self._size += 1

    def append(self, data):
        """Добавляет элемент в конец. O(1) с tail."""
        new_node = DNode(data, self.tail, None)
        if self.tail is None:
            self.head = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node
        self._size += 1

    def find(self, data):
        """Ищет узел по значению. O(n). Возвращает DNode или None."""
        current = self.head
        while current is not None:
            if current.data == data:
                return current
            current = current.next
        return None

    def delete(self, data):
        """Удаляет первый узел с заданным значением. O(n)."""
        node = self.find(data)
        if node is None:
            return
        self.delete_node(node)

    def delete_node(self, node):
        """Удаляет узел по ссылке. O(1) — главное преимущество двусвязного списка."""
        if node.prev is not None:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next is not None:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = node.next = None
        self._size -= 1

    def get(self, index):
        """Возвращает элемент по индексу. O(n).

        Идём с того конца, который ближе: наличие tail позволяет
        сократить обход вдвое (асимптотика та же — O(n)).
        """
        if not (0 <= index < self._size):
            raise IndexError("Index out of bounds")
        if index <= self._size // 2:
            current = self.head
            for _ in range(index):
                current = current.next
        else:
            current = self.tail
            for _ in range(self._size - 1 - index):
                current = current.prev
        return current.data

    def reverse(self):
        """Разворачивает список. O(n)."""
        current = self.head
        while current is not None:
            current.prev, current.next = current.next, current.prev
            current = current.prev
        self.head, self.tail = self.tail, self.head

    def __len__(self):
        return self._size

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.data
            current = current.next

    def __reversed__(self):
        current = self.tail
        while current is not None:
            yield current.data
            current = current.prev

    def __str__(self):
        if self.head is None:
            return "None"
        result = []
        current = self.head
        while current is not None:
            result.append(str(current.data))
            current = current.next
        return " <-> ".join(result) + " <-> None"

    def __repr__(self):
        return f"DoublyLinkedList([{', '.join(repr(x) for x in self)}])"
