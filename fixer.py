#!/usr/bin/env python3
# This is the Discord Cyberpunk RED RPG Bot Mr. Hands
# Author: Derek Blue
# Copyright (C) 2021 See LICENSE file

# Import required libraries
import pathlib
import discord                          # discord API
from discord.ext import commands        # discord bot API
from pathlib import Path                # For file paths
import logging                          # For logging
import random                           # For dice rolls
import json                             # For configuration

import Fixer
from Fixer import Configurator

configurator = Configurator()



# # First startup configuration
# def configure():
#     # Load configuration
#     with open("Fixer/config/config.json", "r") as config_file:
#         configuration = json.load(config_file)
#     # Load or set the bot token
#     if("fixer_bot_token" in configuration):
#         print("Configuration contains bot token")
#     else:
#         bot_token = input("Enter your bot token: ")
#         configuration["fixer_bot_token"] = bot_token
#         with open("configuration.json", "w") as config_file:
#             json.dump(configuration, config_file)
#     configuration["cwd"] = str(Path(__file__).parents[0])
#     print(f'{configuration["cwd"]}\n----------')
#     # Return the configuration
#     return configuration


# # Define the bot and set intents
# intents = discord.Intents.default()
# intents.members = True
# server = discord.Client()
# mr_hands = commands.Bot(command_prefix='/', intents=intents)

# # Once the bot is ready on the server
# @mr_hands.event
# async def on_ready():
#     random.seed()
#     print("Mr. Hands has connected to the server.")

# # Get the bot version command
# @mr_hands.command()
# async def version(ctx):
#     print(ctx.channel)
#     await ctx.send(f'Fixer Version: {configuration["app_version"]}\nMr. Hands Version: {configuration["bot_version"]}')

# @mr_hands.command()
# async def clear(ctx, ammount=10):
#     print(f'Clearing channel: {str(ctx.channel)}')
#     print(type(str(ctx.channel)))
#     if str(ctx.channel) == "fixer":
#         print(f'Clearing channel: {str(ctx.channel)}')
#         await ctx.channel.purge(limit=ammount)

# # Detect when members join the server
# @mr_hands.event
# async def on_member_join(member):
#     print(f'{member} has joined the server.')

# # Detect when members leave the server
# @mr_hands.event
# async def on_member_remove(member):
#     print(f'{member} has left the server.')

# # Configure and run the bot
# configuration = configure()
# mr_hands.run(configuration["fixer_bot_token"])
