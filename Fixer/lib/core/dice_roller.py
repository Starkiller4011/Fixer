import re
from random import randint

class Stack:
    def __str__(self):
        return str([item for item in self.items])
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
    def peek(self):
        return self.items[len(self.items)-1]
    def size(self):
        return len(self.items)
    def length(self):
        return len(self.items)

class DiceExpressionError(Exception):
    def __init__(self, expression: str):
        self.expression = expression
        self.message = f"Dice expression contained invalid characters: {self.expression}"
        super().__init__(self.message)

class DiceTypeError(Exception):
    def __init__(self, dice_type: int) -> None:
        self.dice_type = dice_type
        self.message = f"Wrong dice type given. D{self.dice_type} provided but only D4, D6, D8, D10, D12, D20, D100 are accepted"
        super().__init__(self.message)

class DiceRoll:

    def __str__(self) -> str: return "Dice Roll"

    def __init__(self, expression: str) -> None:
        self.expression = expression.lower()
        self.precedence = {'(': 0, '+': 1, '-': 1, '/': 2, '*': 2, '^': 3, 'd': 4}
        self.operators = ('+', '-', '*', '/', '^', '(', ')', 'd')
        self.dice_types = (4, 6, 8, 10, 12, 20, 100)
    
    def to_tokens(self) -> None:
        tokens = re.split(r' *([\(\+\-\*\^/\)d]) *', self.expression)
        self.tokens = [t for t in tokens if t != '']
    
    def roll_dice(self, count: int, dice_type: int) -> dict:
        if not dice_type in self.dice_types: raise DiceTypeError(dice_type)
        rolls = []
        total = 0
        for i in range(count):
            rolls.append(randint(1, dice_type))
        total = sum(rolls)
        return {'type':f"d{dice_type}", 'total': total, 'rolls': rolls}
    
    def to_rpn(self) -> None:
        rpn = []
        op_stack = Stack()
        for token in self.tokens:
            if not token in self.operators:
                rpn.append(token)
            elif token == '(':
                op_stack.push(token)
            elif token == ')':
                top_token = op_stack.pop()
                while top_token != '(':
                    rpn.append(top_token)
                    top_token = op_stack.pop()
            else:
                while (not op_stack.isEmpty()) and (self.precedence[op_stack.peek()] >= self.precedence[token]):
                    rpn.append(op_stack.pop())
                op_stack.push(token)
        while not op_stack.isEmpty():
            rpn.append(op_stack.pop())
        self.rpn = rpn
    
    def evaluate_term(self, operator, operand1, operand2):
        if operator == 'd':
            return self.roll_dice(operand1, operand2)
        elif operator == '^':
            return operand1**operand2
        elif operator == '/':
            return round(operand1/operand2)
        elif operator == '*':
            return operand1*operand2
        elif operator == '+':
            return operand1+operand2
        elif operator == '-':
            return operand1-operand2
        else:
            return None
    
    def to_string(self):
        result_string = ""
        for roll in self.rolls:
            result_string += f"{roll['type']}: ["
            for i , result in enumerate(roll['rolls']):
                if i > 0:
                    result_string += f", "
                result_string += f"{result}"
            result_string += f"] "
        self.result_string = f"{result_string} = {self.result}"
    
    def evaluate(self):
        rolls = []
        op_stack = Stack()
        for token in self.rpn:
            if not token in self.operators:
                op_stack.push(token)
            else:
                try:
                    operand2 = int(op_stack.pop())
                    operand1 = int(op_stack.pop())
                except:
                    raise DiceExpressionError(self.expression)
                result = self.evaluate_term(token, operand1, operand2)
                if result is not None:
                    if isinstance(result, dict):
                        rolls.append(result)
                        result = result['total']
                    op_stack.push(result)
        self.rolls = rolls
        if op_stack.isEmpty():
            raise DiceExpressionError(self.expression)
        self.result = op_stack.pop()
