#!/usr/bin/env python3
# This is the Discord Cyberpunk RED RPG Bot Mr Hands
# Author: Derek Blue
# Copyright (C) 2021 See LICENSE file

# Import required libraries
from Fixer.lib.core.dice_roller import DiceExpressionError, DiceTypeError
import os
import json
from pathlib import Path
from asyncio import sleep
from datetime import datetime
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from discord import File
from discord import Embed
from discord import Intents
from discord.errors import HTTPException
from discord.errors import Forbidden
from discord.ext.commands import Bot
from discord.ext.commands import Context
from discord.ext.commands import CommandNotFound
from discord.ext.commands import BadArgument
from discord.ext.commands import MissingRequiredArgument

from Fixer.lib.core.config import Configurator
from Fixer.lib.core.dice_roller import DiceTypeError
from Fixer.lib.core.dice_roller import DiceExpressionError

# Cog tracking class to ensure that all cogs are loaded before accepting commands
class CogTracker(object):
    def __init__(self, cogs):
        self.cogs = cogs
        for cog in self.cogs:
            setattr(self, cog, False)
    def ready_up(self, cog):
        setattr(self, cog, True)
    def all_ready(self):
        return all([getattr(self, cog) for cog in self.cogs])

class FixerBot(Bot):
    ignore_exceptions = (CommandNotFound, BadArgument)

    def __str__(self) -> str: return "Fixer Bot"

    def __init__(self, configuration: Configurator):
        self.name = "Fixer Bot"
        self.logger = configuration.logger
        self.configuration = configuration
        self.scheduler = AsyncIOScheduler()
        self.ready = False
        self.servers = {}
        super().__init__(
            command_prefix=self.configuration.command_prefix,
            case_insensitive=self.configuration.case_insensitive,
            intents=Intents.all()
        )
    
    def setup(self, cogs):
        self.cog_tracker = CogTracker(cogs)
        if self.configuration.verbose:
            self.logger.log(self.name, f"Loading cogs")
        else:
            self.logger.log_to_file(self.name, f"Loading cogs")
            # print(f"[Mr Hands] >> Loading cogs")
        for cog in cogs:
            if cog != '__init__':
                self.load_extension(f"Fixer.cogs.{cog}")
                if self.configuration.verbose:
                    self.logger.log(self.name, f"{cog} cog loaded")
                else:
                    self.logger.log_to_file(self.name, f"{cog} cog loaded")
                    # print(f"[Mr Hands] >> {cog} cog loaded")
        if self.configuration.verbose:
            self.logger.log(self, f"Cog setup complete")
        else:
            self.logger.log_to_file(self, f"Cog setup complete")
        # print(f"[Mr Hands] >> Cogs:             [ OK ]")

    def run(self, cogs):
        if self.configuration.verbose:
            self.logger.log(self, f"Running setup")
        else:
            self.logger.log_to_file(self, f"Running setup")
        self.setup(cogs)
        if self.configuration.verbose:
            self.logger.log(self, f"Running bot")
        else:
            self.logger.log_to_file(self, f"Running bot")
        super().run(self.configuration.token, reconnect=True)
    
    async def process_commands(self, message):
        context = await self.get_context(message, cls=Context)
        if context.command is not None and context.guild is not None:
            if self.ready:
                if self.configuration.verbose:
                    self.logger.log(self, f"Processing commands")
                else:
                    self.logger.log_to_file(self, f"Processing commands")
                await self.invoke(context)
            else:
                if self.configuration.verbose:
                    self.logger.log(self, f"Bot not ready yet, cannot process commands")
                else:
                    self.logger.log_to_file(self, f"Bot not ready yet, cannot process commands")
                await context.send(f"I'm not ready to receive commands yet punk, calm your tits!")
        # return super().process_commands(message)
    
    async def print_message(self):
        if self.configuration.verbose:
            self.logger.log(self, f"Scheduled task: {datetime.utcnow()}")
        else:
            self.logger.log_to_file(self, f"Scheduled task: {datetime.utcnow()}")
        # channel = self.get_channel(796810313033842710)
        # await channel.send("I am a timed notification!")
    
    async def on_connect(self):
        if self.configuration.verbose:
            self.logger.log(self, f"Connected")
        else:
            self.logger.log_to_file(self, f"Connected")
    
    async def on_disconnect(self):
        if self.configuration.verbose:
            self.logger.log(self, f"Disconnected")
        else:
            self.logger.log_to_file(self, f"Disconnected")
    
    async def on_error(self, event_method, *args, **kwargs):
        # if event_method == "on_command_error":
        #     await args[0].send(f"Something went wrong.")
        if self.configuration.verbose:
            self.logger.log(self, f"An error occured")
        else:
            self.logger.log_to_file(self, f"An error occured")
        await self.stderr.send(f"An error occured")
        raise Exception
    
    async def on_command_error(self, context: Context, exception: Exception):
        # self.logger.log(self, f"on_command_error {exception} being handled, deleting offending command")
        # await context.message.delete()
        if any([isinstance(exception, error) for error in self.ignore_exceptions]):
            pass
        elif isinstance(exception.original, DiceTypeError):
            self.logger.log(self, f"{exception.original.message}")
        elif isinstance(exception.original, DiceExpressionError):
            self.logger.log(self, f"{exception.original.message}")
        elif isinstance(exception, MissingRequiredArgument):
            if self.configuration.verbose:
                self.logger.log(self, f"One or more required arguments are missing in command: {self.configuration.command_prefix}{context.command}")
            else:
                self.logger.log_to_file(self, f"One or more required arguments are missing in command: {self.configuration.command_prefix}{context.command}")
            await context.send(f"One or more required arguments are missing in command: {self.configuration.command_prefix}{context.command}")
        elif isinstance(exception.original, HTTPException):
            if self.configuration.verbose:
                self.logger.log(self, f"Bot couldn't send the message")
            else:
                self.logger.log_to_file(self, f"Bot couldn't send the message")
            await context.send(f"I couldn't send the message")
        elif isinstance(exception.original, Forbidden):
            if self.configuration.verbose:
                self.logger.log(self, f"Bot doesn't have permission to conduct action")
            else:
                self.logger.log_to_file(self, f"Bot doesn't have permission to conduct action")
            await context.send(f"I don't have permission to do that")
        elif hasattr(exception, "original"):
            raise exception.original
        else:
            raise exception
    
    async def on_ready(self):
        if not self.ready:
            if self.configuration.verbose:
                self.logger.log(self, f"Setting stdout and stderr channels")
            else:
                self.logger.log_to_file(self, f"Setting stdout and stderr channels")
            self.stdout = self.get_channel(799322874824491079)
            self.stderr = self.get_channel(799322861343866910)
            if self.configuration.verbose:
                self.logger.log(self, f"Scheduling tut timed task")
            else:
                self.logger.log_to_file(self, f"Scheduling tut timed task")
            self.scheduler.add_job(self.print_message, CronTrigger(second="1"))
            self.scheduler.start()
            if self.configuration.verbose:
                self.logger.log(self, f"Setting guild")
            else:
                self.logger.log_to_file(self, f"Setting guild")
            self.guild = self.get_guild(796810312187641878)
            self.configuration.logger.module_ready(self)
            while not self.cog_tracker.all_ready():
                if self.configuration.verbose:
                    self.logger.log(self, f"Waiting for cogs to load")
                else:
                    self.logger.log_to_file(self, f"Waiting for cogs to load")
                await sleep(0.5)
            self.ready = True
        if self.configuration.verbose:
            self.logger.log(self, f"All cogs loaded and bot ready")
        else:
            self.logger.log_to_file(self, f"All cogs loaded and bot ready")
        self.configuration.logger.module_ready("Fixer")
        if self.configuration.verbose:
            self.logger.log(self, f"Fixer is now loaded and ready")
            self.logger.log(self, f"Fixer Bot has been deployed to servers")
        else:
            self.logger.log_to_file(self, f"Fixer is now loaded and ready")
            self.logger.log_to_file(self, f"Fixer Bot has been deployed to servers")
    
    async def on_message(self, message):
        if message.author.bot and message.author != message.guild.me:
            if self.configuration.verbose:
                self.logger.log(self, f"Received a command from another bot")
            else:
                self.logger.log_to_file(self, f"Received a command from another bot")
        if not message.author.bot:
            await self.process_commands(message)
