import re
from enum import Enum

class NodeType(Enum):
    OPERATOR = 1
    COMPARISON = 2
    LITERAL = 3
    VARIABLE = 4

class Operator(Enum):
    AND = 1
    OR = 2

class Node:
    def __init__(self, type, value, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

def tokenize(rule_string):
    tokens = re.findall(r'\(|\)|AND|OR|[<>=!]+|\'[^\']*\'|\S+', rule_string)

# Correcting the output to ensure closing brackets are separate
    corrected_tokens = []
    for token in tokens:
        if token == ')':
            corrected_tokens.append(')')
        elif token.endswith(')'):
            # Split token if it ends with a closing bracket
            corrected_tokens.append(token[:-1])
            corrected_tokens.append(')')
        else:
            corrected_tokens.append(token)
    print(f"Tokenized rule: {corrected_tokens}")
    return corrected_tokens

def check_parentheses(tokens):
    stack = []
    for i, token in enumerate(tokens):
        print(f"Checking token {i}: '{token}'")
        if token == '(':
            stack.append(i)
            print(f"  Opening parenthesis found. Stack: {stack}")
        elif token == ')':
            if not stack:
                raise ValueError(f"Unmatched closing parenthesis at position {i}")
            last_open = stack.pop()
            print(f"  Closing parenthesis found. Matched with opening at position {last_open}. Stack: {stack}")
    
    if stack:
        unmatched_positions = ', '.join(str(pos) for pos in stack)
        raise ValueError(f"Unmatched opening parentheses at positions: {unmatched_positions}")

    print("Parentheses check passed successfully")

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        return self.expression()

    def expression(self):
        print(f"Parsing expression starting at token {self.current}: '{self.tokens[self.current]}'")
        expr = self.term()
        while self.current < len(self.tokens) and self.tokens[self.current] == 'OR':
            self.current += 1
            right = self.term()
            expr = Node(NodeType.OPERATOR, Operator.OR, expr, right)
        return expr

    def term(self):
        print(f"Parsing term starting at token {self.current}: '{self.tokens[self.current]}'")
        expr = self.factor()
        while self.current < len(self.tokens) and self.tokens[self.current] == 'AND':
            self.current += 1
            right = self.factor()
            expr = Node(NodeType.OPERATOR, Operator.AND, expr, right)
        return expr

    def factor(self):
        print(f"Parsing factor starting at token {self.current}: '{self.tokens[self.current]}'")
        if self.current < len(self.tokens) and self.tokens[self.current] == '(':
            self.current += 1
            expr = self.expression()
            if self.current < len(self.tokens) and self.tokens[self.current] == ')':
                self.current += 1
            else:
                raise ValueError(f"Expected closing parenthesis at position {self.current}")
            return expr
        else:
            return self.comparison()

    def comparison(self):
        print(f"Parsing comparison starting at token {self.current}: '{self.tokens[self.current]}'")
        if self.current + 2 >= len(self.tokens):
            raise ValueError(f"Incomplete comparison at position {self.current}")
        
        left = Node(NodeType.VARIABLE, self.tokens[self.current])
        self.current += 1
        op = self.tokens[self.current]
        self.current += 1
        right = Node(NodeType.LITERAL, self.tokens[self.current].strip("'"))
        self.current += 1
        return Node(NodeType.COMPARISON, op, left, right)

def create_rule(rule_string):
    print(f"Creating rule for: {rule_string}")
    tokens = tokenize(rule_string)
    check_parentheses(tokens)
    parser = Parser(tokens)
    rule = parser.parse()
    if parser.current < len(tokens):
        raise ValueError(f"Unexpected tokens after parsing: {' '.join(tokens[parser.current:])}")
    return rule

def evaluate_rule(rule, data):
    if rule is None:
        return False
    if rule.type == NodeType.OPERATOR:
        if rule.value == Operator.AND:
            return evaluate_rule(rule.left, data) and evaluate_rule(rule.right, data)
        elif rule.value == Operator.OR:
            return evaluate_rule(rule.left, data) or evaluate_rule(rule.right, data)
    elif rule.type == NodeType.COMPARISON:
        left_value = data.get(rule.left.value)
        right_value = rule.right.value
        
        if left_value is None:
            return False
        
        if rule.value == '>':
            return float(left_value) > float(right_value)
        elif rule.value == '<':
            return float(left_value) < float(right_value)
        elif rule.value == '=':
            return str(left_value) == str(right_value)
        elif rule.value == '>=':
            return float(left_value) >= float(right_value)
        elif rule.value == '<=':
            return float(left_value) <= float(right_value)
        elif rule.value == '!=':
            return str(left_value) != str(right_value)
    return False

def rule_to_string(node):
    if node is None:
        return "None"
    if node.type == NodeType.OPERATOR:
        return f"({rule_to_string(node.left)} {node.value.name} {rule_to_string(node.right)})"
    elif node.type == NodeType.COMPARISON:
        return f"({node.left.value} {node.value} {node.right.value})"
    elif node.type in (NodeType.LITERAL, NodeType.VARIABLE):
        return str(node.value)
    else:
        return "Unknown node type"
