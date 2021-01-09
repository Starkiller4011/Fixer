#!/usr/bin/env python3
# This is the Discord Cyberpunk RED RPG App
# Author: Derek Blue
# Copyright (C) 2021 See LICENSE file

# Import required libraries
from pathlib import Path
from Fixer import Configurator
from Fixer import MrHands
from Fixer import DataBase
from glob import glob

configurator = Configurator()
mr_hands = MrHands(configurator)
database = DataBase(configurator)

database.build()
database.autosave(mr_hands.scheduler)
cog_path = str(Path.joinpath(configurator.cwd, "cogs/*.py"))
cogs = [path.split("\\")[-1][:-3] for path in glob(cog_path)]
mr_hands.run(cogs)
