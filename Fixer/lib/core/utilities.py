#!/usr/bin/env python3
# This is the Discord Cyberpunk RED RPG App
# Author: Derek Blue
# Copyright (C) 2021 See LICENSE file

import re
import json
import random
from pathlib import Path
from collections import deque
from apscheduler.util import repr_escape

from discord.colour import Colour

def sanitize_input(input_string):
    output_string = ""
    for char in input_string:
        if char == '>':
            outchar = '&gt;'
        elif char == '<':
            outchar = '&lt;'
        else:
            outchar = char
        output_string += outchar
    return output_string

def generate_id(type):
    str_id = ""
    if type == "game":
        print(f"[Utility] >> Generating game ID:")
        str_id += str(71135)
    elif type == "character":
        print(f"[Utility] >> Generating character ID:")
        str_id += str(38118)
    elif type == "npc":
        print(f"[Utility] >> Generating NPC character ID:")
        str_id += str(14163)
    for digit in [random.randint(0,9) for i in range(0,13)]:
        str_id += str(digit)
    int_id = int(str_id)
    return int_id

def get_colour(colour, variant):
    colours = {}
    with open(Path.joinpath(Path(__file__).parents[2], "config/colours.json"), "r") as colour_file:
        colours = json.load(colour_file)
    return Colour(int(f'0x{colours[colour][variant]}', 16))

def parse_expression(expression):
    tokens = re.split(r' *([\(\+\_\*\^/\)d]) *', expression)
    tokens = [t for t in tokens if t != '']
    def to_rpn(tokens):
        precedence = {'(': 0, '+': 1, '-': 1, '/': 2, '*': 2, '^': 3, 'd': 4}
        operators = ('+', '-', '*', '/', '^', '(', ')', 'd')
        rpn = []
        op_stack = Stack()
        for token in tokens:
            if not token in operators:
                rpn.append(token)
            elif token == '(':
                op_stack.push(token)
            elif token == ')':
                top_token = op_stack.pop()
                while top_token != '(':
                    rpn.append(top_token)
                    top_token = op_stack.pop()
            else:
                while (not op_stack.isEmpty()) and (precedence[op_stack.peek()] >= precedence[token]):
                    rpn.append(op_stack.pop())
                op_stack.push(token)
        while not op_stack.isEmpty():
            rpn.append(op_stack.pop())
        return rpn
    return to_rpn(tokens)

def parse_args(argv):
    args = None
    # Parse command line args if they were passed
    for i in range(len(argv)):
        if argv[i] in ("-v", "--verbose"):
            if args is None:
                args = {}
            args["verbose"] = True
        if argv[i] in ("-c", "--case_insensitive"):
            if args is None:
                args = {}
            args["case_insensitive"] = True
        if argv[i] in ("-p", "--command_prefix"):
            if args is None:
                args = {}
            i += 1
            args["command_prefix"] = argv[i]
        if argv[i] in ("-t", "--token"):
            if args is None:
                args = {}
            i += 1
            args["token"] = argv[i]
        if '=' in argv[i]:
            opt = argv[i].split('=')
            if opt[0] in ("-p", "--command_prefix"):
                if args is None:
                    args = {}
                args["command_prefix"] = opt[1]
            if opt[0] in ("-t", "--token"):
                if args is None:
                    args = {}
                args["token"] = opt[1]
    return args
