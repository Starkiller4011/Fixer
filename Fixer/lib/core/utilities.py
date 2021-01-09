import json
import random
from pathlib import Path
from discord.colour import Colour

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
