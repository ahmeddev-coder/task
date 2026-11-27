"""Stack — last in, first out.

Deliberately a thin structure: the interesting part is what you *do* with it
(balanced brackets, infix to postfix, undo history, DFS without recursion).

Built on your own `DynamicArray` (Week 4): the top of the stack is the END of
the array, where append and pop are O(1). Put the top at index 0 instead and
every push shifts the whole stack — try it, and measure it.
"""

from __future__ import annotations

from dsa.dynamic_array import DynamicArray


class Stack:
    """LIFO. Every operation should be O(1)."""

    def __init__(self, values=()):
        self._items = DynamicArray()
        for value in values:
            self.push(value)

    def push(self, value):
        """Add to the top. Target: O(1) amortised."""
        self._items.append(value)

    def pop(self):
        """Remove and return the top. Target: O(1). Raises IndexError when empty."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        """Return the top without removing it. Raises IndexError when empty."""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[len(self._items) - 1]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        if not len(self._items):
            return "Stack([])"
        return f"Stack({list(self._items)!r})  # top = {self._items[len(self._items) - 1]!r}"


# -- challenges -----------------------------------------------------------


def is_balanced(text):
    """True when every bracket in `text` is closed in the right order.

    "(a[b]{c})" -> True ;  "(a[b)]" -> False ;  "(" -> False

    The canonical first use of a stack. Target: O(n).
    """
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = Stack()
    for ch in text:
        if ch in "([{":
            stack.push(ch)
        elif ch in pairs:
            if stack.is_empty() or stack.pop() != pairs[ch]:
                return False
    return stack.is_empty()


def infix_to_postfix(tokens):
    """Shunting-yard: ["3","+","4","*","2"] -> ["3","4","2","*","+"].

    Target: O(n). Handles + - * / and parentheses.
    """
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}
    output = []
    ops = Stack()

    for token in tokens:
        if token in precedence:
            # pop operators with higher or equal precedence (left-associative)
            while (not ops.is_empty()
                   and ops.peek() != "("
                   and precedence[ops.peek()] >= precedence[token]):
                output.append(ops.pop())
            ops.push(token)
        elif token == "(":
            ops.push(token)
        elif token == ")":
            while not ops.is_empty() and ops.peek() != "(":
                output.append(ops.pop())
            if ops.is_empty():
                raise ValueError("mismatched parentheses")
            ops.pop()  # discard the "("
        else:
            output.append(token)  # operand

    while not ops.is_empty():
        op = ops.pop()
        if op == "(":
            raise ValueError("mismatched parentheses")
        output.append(op)

    return output
