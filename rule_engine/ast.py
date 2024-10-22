from enum import Enum
from typing import Optional, Union

class NodeType(Enum):
    OPERATOR = 1
    COMPARISON = 2
    LITERAL = 3
    VARIABLE = 4

class Operator(Enum):
    AND = 1
    OR = 2
    NOT = 3

class Node:
    def __init__(self, type, value, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right
