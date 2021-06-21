"""
Programming for linguists

Implementation of the Reverse Polish Notation Converter
"""
from algorithms.calculator.reverse_polish_notation import (Digit, Op, ReversePolishNotation, BinaryOp, OpenBracket, CloseBracket, OpFactory)
from data_structures.queue_ import Queue_
from data_structures.stack import Stack


class ReversePolishNotationConverterState:
    """
    Class to store the state of RPN convert process
    """
    def __init__(self, expression_in_infix_notation: str):
        self.expression_in_infix_notation = Queue_(expression_in_infix_notation)
        self.expression_in_postfix_notation = ReversePolishNotation()
        self.stack = Stack()

        while not ReversePolishNotationConverter.is_open_bracket(self.stack.top()):
            self.expression_in_postfix_notation.put(self.stack.top())
            self.stack.pop()
        self.stack.pop()


class ReversePolishNotationConverter:
    def __init__(self, infix_string: str):
        self._infix_notation = Queue_(infix_string)
        self._postfix_notation = ReversePolishNotation()
        self.stack = Stack()
    point = '.'

    def convert(self, expression_in_infix_notation: str) -> ReversePolishNotation:
        while not self._infix_notation.empty():
            character = self._infix_notation.get()
            if self.is_part_of_digit(character):
                digit = self.read_digit(character)
                self._postfix_notation.put(digit)
                continue
            elif self.is_opening_bracket(character):
                self.stack.push(character)
                continue
            elif self.is_closing_bracket(character):
                self.pop_from_stack_until_opening_bracket()
                continue

            operator = OpFactory.get_op_by_symbol(character)
            if self.is_binary_operation(operator):
                self.pop_from_stack_until_prioritizing(operator)
            else:
                raise Exception(character)
        while not self.stack.empty():
            self._postfix_notation.put(self.stack.top())
            self.stack.pop()
        return self._postfix_notation

    def pop_from_stack_until_opening_bracket(self):
        while not self.is_opening_bracket(self.stack.top()):
            self._postfix_notation.put_operator(self.stack.top())
            self.stack.pop()
        self.stack.pop()

    def pop_from_stack_until_prioritizing(self, operator: Op, state: ReversePolishNotationConverterState):
        current_priority = operator.priority
        while not self.stack.empty() and self.stack.top().priority > current_priority:
            self._postfix_notation.put(self.stack.top())
            self.stack.pop()
        self.stack.push(operator)

    def read_digit(self, character: str) -> Digit:
        digit = character
        while not self._infix_notation.empty() and self.is_part_of_digit(self._infix_notation.top()):
            digit += self._infix_notation.get()
        return Digit(digit)

    @staticmethod
    def is_part_of_digit(character: str) -> bool:
        return character.isdigit() or character == ReversePolishNotationConverter.point

    @staticmethod
    def is_open_bracket(character: str, operator: Op) -> bool:
        if character == '(':
            return True
        return False

    @staticmethod
    def is_close_bracket(character: str, operator: Op) -> bool:
        if character == ')':
            return True
        return False

    @staticmethod
    def is_binary_operation(operator: Op) -> bool:
        return isinstance(operator, BinaryOp)
