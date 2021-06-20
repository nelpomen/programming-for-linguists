"""
Programming for linguists

Implementation of the Reverse Polish Notation Converter
"""
from algorithms.calculator.reverse_polish_notation import (ReversePolishNotation, Op, Digit)

from data_structures.stack.stack import Stack


class ReversePolishNotationCalculator:
    """
    Calculator of expression in Reverse Polish Notation
    """
    def __init__(self):
        self.stack = Stack()

    def calculate(self, rpn_expression: ReversePolishNotation) -> float:
        for element in rpn_expression:
            if isinstance(element, Op):
                res = self.calculate_value(element)
                self.stack.push(res)
            else:
                self.stack.push(element)
        return self.stack.top()

    def _calculate_value(self, operator: Op) -> Digit:
        first = self.stack.top()
        self.stack.pop()
        second = self.stack.top()
        self.stack.pop()
        return operator.function(first, second)

