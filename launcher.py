#!/usr/bin/env python3
# This is the Discord Cyberpunk RED RPG App
# Author: Derek Blue
# Copyright (C) 2021 See LICENSE file

# Import required libraries
from sys import argv
from glob import glob
from pathlib import Path
from getopt import gnu_getopt
from getopt import GetoptError

from discord.utils import get

import Fixer
from Fixer import Logger
from Fixer import FixerBot
from Fixer import DataBase
from Fixer import Configurator

configurator = Configurator(verbose=False)
configurator.load()
fixer_bot = FixerBot(configurator)
database = DataBase(configurator)

database.build()
database.autosave(fixer_bot.scheduler)

cog_path = str(Path.joinpath(configurator.cwd, "cogs/*.py"))
cogs = [path.split("\\")[-1][:-3] for path in glob(cog_path)]

fixer_bot.run(cogs)

# def main(argv):
#     args = Fixer.parse_args(argv)
#     if args is not None:
#         print(args)
#         if "verbose" in args:
#             config = Configurator(args["verbose"])
#     else:
#         config = Configurator()
#     print(Fixer.parse_expression("4*(3d10+8)+23*(1d6*(3d4+2))"))
#     number = "10"
#     third = int(number)/3
#     print(third)

# if __name__ == '__main__':
#     main(argv[1:])
