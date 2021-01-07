#!/usr/bin/env python3
# This is the Discord Cyberpunk RED RPG Bot Mr Hands
# Author: Derek Blue
# Copyright (C) 2021 See LICENSE file

# Import required libraries
from discord.ext.commands import Bot
from .config import Configurator

# Mr Hands Class
class MrHands(Bot):
    """
    Class: Mr Hands (single use)
    """
    def __init__(self, configuration: Configurator):
        """
        Initializer

        Args:
            version (str): The bot version
        """
        self.configuration = configuration
