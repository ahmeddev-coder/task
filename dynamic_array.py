"""Dynamic array — what Python's `list` actually is underneath.

Built on the course `Array` (`dsa/array.py`): a fixed-size block that is
reallocated when it fills. The payoff is
`amortised` O(1) append: most appends are cheap, a few are expensive, and the
average stays constant. Doubling the capacity is what makes that true —
growing by a constant instead gives O(n) amortised, which is worth measuring
with `viz.complexity.measure` rather than just asserting.
"""

from __future__ import annotations

from dsa.array import Array


def make_block(capacity):
    
    """Allocate a fixed-size block of `capacity` slots, every one None.

    This is the one piece we hand you: an `Array` is a genuinely fixed-size,
    C-style array, so the reallocation you write is real rather than simulated
    on top of another list. Growing means: make a bigger block, copy, switch.
    """
    return Array(capacity)


class DynamicArray:
    """A growable array with O(1) indexing and amortised O(1) append."""

    def __init__(self, values=(), growth=2):
        self._size = 0
        self._capacity = 1
        self._block = make_block(self._capacity)
        self.growth = growth
        #: number of reallocations so far — plot this against n
        self.resize_count = 0
        for value in values:
            self.append(value)

    def append(self, value):
      if self._size == self._capacity:
        self._resize(self._capacity * self.growth)

      self._block[self._size] = value
      self._size += 1
      """Add to the end. Target: amortised O(1).

        Call `_resize(self._capacity * self.growth)` when full.
        """
        

    def insert_at(self, index, value):
      if not 0 <= index <= self._size:
        raise IndexError(index)

      if self._size == self._capacity:
        self._resize(self._capacity * self.growth)

      for i in range(self._size, index, -1):
        self._block[i] = self._block[i - 1]

      self._block[index] = value
      self._size += 1
      """Insert at `index`, shifting the rest right. Target: O(n).

        Raises IndexError unless 0 <= index <= len(self), as `insert_at` does
        in Week 2 and in the linked list. Inserting at len(self) appends.
        """


    def pop(self, index=-1):
       if self._size == 0:
          raise IndexError("Array is empty")

       if index < 0:
        index += self._size

       if not 0 <= index < self._size:
        raise IndexError(index)

       value = self._block[index]

       for i in range(index, self._size - 1):
        self._block[i] = self._block[i + 1]

       self._size -= 1
       self._block[self._size] = None

       return value
       """Remove and return the value at `index`. Target: O(n), O(1) at the end.

        Raises IndexError when empty.
        """
    def _resize(self, capacity):
        new_block = make_block(capacity)

        for i in range(self._size):
            new_block[i] = self._block[i]

        self._block = new_block
        self._capacity = capacity
        self.resize_count += 1
        """Move every element into a fresh block of `capacity` slots.

        Remember to increment `self.resize_count` — the notebook plots it.
        """
       

    def __len__(self):
        return self._size
        
    def __getitem__(self, index):
        if index < 0:
            index += self._size

        if not 0 <= index < self._size:
            raise IndexError(index)

        return self._block[index]
        """Target: O(1). Support negative indices; raise IndexError otherwise."""
    

    def __setitem__(self, index, value):
        if index < 0:
            index += self._size

        if not 0 <= index < self._size:
            raise IndexError(index)

        self._block[index] = value
    """a[index] = value. Target: O(1). Same indices, and errors, as __getitem__."""
    
    def __iter__(self):
        for i in range(self._size):
            yield self._block[i]
    def __repr__(self):
     return "DynamicArray([" + ", ".join(repr(v) for v in self) + "])"
