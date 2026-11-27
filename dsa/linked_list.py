"""Singly linked list.

The first structure where a picture beats an explanation. Use
`viz.draw.draw_linked_list(list(ll), highlight=i)` while you walk a pointer
along it.
"""

from __future__ import annotations
from operator import index



class Node:
    """One cell: a value, and a reference to the next cell (or None)."""

    __slots__ = ("value", "next")

    def __init__(self, value, next=None):
        self.value = value
        self.next = next

    def __repr__(self):
        return f"Node({self.value!r})"


class LinkedList:
    """A singly linked list holding a head reference and a length.

    Keeping `_size` updated as you go is what makes `__len__` O(1) instead of
    O(n) — a small decision worth discussing in class.
    """

    def __init__(self, values=()):
        self.head = None
        self._tail = None
        self._size = 0

        for value in values:
            self.append(value)

    # -- building -------------------------------------------------------

    def push_front(self, value):
        new_node = Node(value, self.head)
        self.head = new_node

        if self._tail is None:
            self._tail = new_node

        self._size += 1

    def append(self, value):
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node

        self._size += 1
        """Insert at the tail. Target: O(n) without a tail pointer.

        Challenge: add a `_tail` reference and get this to O(1). What does
        that cost you in `pop_front` and in `remove`?
        """
    

    def insert_at(self, index, value):
        if index < 0 or index > self._size:
            raise IndexError("Index out of range")

        if index == 0:
            self.push_front(value)
            return

        if index == self._size:
            self.append(value)
            return

        current = self.head

        for _ in range(index - 1):
            current = current.next

        new_node = Node(value, current.next)
        current.next = new_node

        self._size += 1
        """Insert so that the new node ends up at `index`. Target: O(n).

        Raises IndexError unless 0 <= index <= len(self).
        """
    

    # -- removing -------------------------------------------------------

    def pop_front(self):
        if self.head is None:
            raise IndexError("List is empty")

        value = self.head.value
        self.head = self.head.next

        self._size -= 1

        if self.head is None:
            self._tail = None

        return value
        """Remove and return the head value. Target: O(1).

        Raises IndexError when empty.
        """
    def remove(self, value):
        if self.head is None:
            return False

        if self.head.value == value:
            self.pop_front()
            return True

        previous = self.head
        current = self.head.next

        while current is not None:
            if current.value == value:
                previous.next = current.next

                if current is self._tail:
                    self._tail = previous

                self._size -= 1
                return True

            previous = current
            current = current.next

        return False
        """Remove the first node holding `value`. Target: O(n).

        Returns True when something was removed, False otherwise.
        """


    # -- reading --------------------------------------------------------

    def find(self, value):
        current = self.head
        index = 0

        while current is not None:
            if current.value == value:
                return index
            current = current.next
            index += 1

        return -1
        """Return the index of the first node holding `value`, else -1."""

    def reverse(self):
        previous = None
        current = self.head

        self._tail = self.head

        while current is not None:
            next_node = current.next
            current.next = previous

            previous = current
            current = next_node

        self.head = previous
        """Reverse the list in place. Target: O(n) time, O(1) extra space.

        The classic three-pointer problem. Draw it before you code it.
        """

    # -- Python protocol ------------------------------------------------

    def __len__(self):
        return self._size

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node.value
            node = node.next

    def __getitem__(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")

        current = self.head
        for _ in range(index):
            current = current.next

        return current.value
        """Positional access. Target: O(n) — and that is the whole lesson.

        Raises IndexError unless 0 <= index < len(self).

        Contrast with `dsa.dynamic_array.DynamicArray.__getitem__`, which is
        O(1). Same interface, completely different cost.
        """
       

    def __repr__(self):
        return "LinkedList([" + ", ".join(repr(v) for v in self) + "])"
