"""Queue — first in, first out.

Two implementations worth writing side by side, because the naive one hides an
O(n) cost that only shows up when you measure it:

  * `SlowQueue` dequeues with `DynamicArray.pop(0)` — O(n) per operation
  * `CircularQueue` keeps a head index and a size in a fixed `Array` — O(1) per operation

Run both through `viz.complexity.measure` and plot. The gap is the lesson.
"""

from __future__ import annotations

from dsa.array import Array
from dsa.dynamic_array import DynamicArray


class SlowQueue:
    """FIFO on a DynamicArray. Correct, but dequeue is O(n) — prove it."""

    def __init__(self, values=()):
        self._items = DynamicArray(values)

    def enqueue(self, value):
        """Add to the back. O(1)."""
        self._items.append(value)

    def dequeue(self):
        """Remove from the front. O(n) here — every element shifts left.

        Raises IndexError when empty.
        """
        if len(self._items) == 0:
            raise IndexError("dequeue from empty queue")
        return self._items.pop(0)

    def __len__(self):
        return len(self._items)


class CircularQueue:
    """FIFO in a fixed-capacity ring buffer. Every operation O(1).

    `head` is where the next dequeue reads; the next enqueue writes at the
    tail, `(head + size) % capacity`, computed rather than stored. Keeping `_size` is
    what lets you tell "full" from "empty" when head == tail.
    """

    def __init__(self, capacity=8):
        self._block = Array(capacity)
        self._capacity = capacity
        self._head = 0
        self._size = 0

    def enqueue(self, value):
        """Add to the back. Target: O(1).

        Challenge: grow the ring when it fills, rather than raising. Careful —
        a naive copy scrambles the order once the data has wrapped around.
        """
        if self.is_full():
            self._grow()
        tail = (self._head + self._size) % self._capacity
        self._block[tail] = value
        self._size += 1

    def _grow(self):
        """Double the capacity, unrolling the ring so head goes back to 0."""
        new_capacity = max(1, self._capacity * 2)
        new_block = Array(new_capacity)
        for offset in range(self._size):
            new_block[offset] = self._block[(self._head + offset) % self._capacity]
        self._block = new_block
        self._capacity = new_capacity
        self._head = 0

    def dequeue(self):
        """Remove from the front. Target: O(1). Raises IndexError when empty."""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        value = self._block[self._head]
        self._block[self._head] = None  # drop the reference
        self._head = (self._head + 1) % self._capacity
        self._size -= 1
        return value

    def is_empty(self):
        return self._size == 0

    def is_full(self):
        return self._size == self._capacity

    def __len__(self):
        return self._size

    def __iter__(self):
        for offset in range(self._size):
            yield self._block[(self._head + offset) % self._capacity]

    def __repr__(self):
        return "CircularQueue([" + ", ".join(repr(v) for v in self) + "])"
