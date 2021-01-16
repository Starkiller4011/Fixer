#!/usr/bin/env python3
# This is the Discord Cyberpunk RED RPG Bot Mr Hands
# Author: Derek Blue
# Copyright (C) 2021 See LICENSE file

# Import required libraries
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

class CogTracker(object):
    def __init__(self, cogs):
        self.cogs = cogs
        for cog in self.cogs:
            setattr(self, cog, False)
    def ready_up(self, cog):
        setattr(self, cog, True)
    def all_ready(self):
        return all([getattr(self, cog) for cog in self.cogs])

# Mr Hands Class
class MrHands(Bot):
    ignore_exceptions = (CommandNotFound, BadArgument)

    def __init__(self, configuration: Configurator):
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
            print(f"[Mr Hands] >> Loading cogs")
        for cog in cogs:
            if cog != '__init__':
                self.load_extension(f"Fixer.cogs.{cog}")
                if self.configuration.verbose:
                    print(f"[Mr Hands] >> {cog} cog loaded")
        if self.configuration.verbose:
            print(f"[Mr Hands] >> Cog setup complete")
        print(f"[Mr Hands] >> Cogs:             [ OK ]")

    def run(self, cogs):
        if self.configuration.verbose:
            print(f"[Mr Hands] >> Running setup")
        self.setup(cogs)
        if self.configuration.verbose:
            print(f"[Mr Hands] >> Running bot")
        super().run(self.configuration.token, reconnect=True)
    
    async def process_commands(self, message):
        context = await self.get_context(message, cls=Context)
        if context.command is not None and context.guild is not None:
            if self.ready:
                if self.configuration.verbose:
                    print(f"[Mr Hands] >> Processing commands")
                await self.invoke(context)
            else:
                if self.configuration.verbose:
                    print(f"[Mr Hands] >> Bot not ready yet, cannot process commands")
                await context.send(f"I'm not ready to receive commands yet punk, calm your tits!")
        # return super().process_commands(message)
    
    async def print_message(self):
        if self.configuration.verbose:
            print(f"[Mr Hands] >> {datetime.utcnow()}")
        # channel = self.get_channel(796810313033842710)
        # await channel.send("I am a timed notification!")
    
    async def on_connect(self):
        if self.configuration.verbose:
            print(f"[Mr Hands] >> Connected")
    
    async def on_disconnect(self):
        if self.configuration.verbose:
            print(f"[Mr Hands] >> Disconnected")
    
    async def on_error(self, event_method, *args, **kwargs):
        # if event_method == "on_command_error":
        #     await args[0].send(f"Something went wrong.")
        if self.configuration.verbose:
            print(f"[Mr Hands] >> An error occured")
        await self.stderr.send(f"An error occured")
        raise Exception
    
    async def on_command_error(self, context: Context, exception: Exception):
        # if isinstance(exception, CommandNotFound):
        #     pass
        # elif isinstance(exception, BadArgument):
        #     pass
        await context.message.delete()
        if any([isinstance(exception, error) for error in self.ignore_exceptions]):
            pass
        elif isinstance(exception, MissingRequiredArgument):
            if self.configuration.verbose:
                print(f"[Mr Hands] >> One or more required arguments are missing in command: {self.configuration.command_prefix}{context.command}")
            await context.send(f"One or more required arguments are missing in command: {self.configuration.command_prefix}{context.command}")
        elif isinstance(exception.original, HTTPException):
            if self.configuration.verbose:
                print(f"[Mr Hands] >> Bot couldn't send the message")
            await context.send(f"I couldn't send the message")
        elif isinstance(exception.original, Forbidden):
            if self.configuration.verbose:
                print(f"[Mr Hands] >> Bot doesn't have permission to conduct action")
            await context.send(f"I don't have permission to do that")
        elif hasattr(exception, "original"):
            raise exception.original
        else:
            raise exception
    
    async def on_ready(self):
        if not self.ready:
            if self.configuration.verbose:
                print(f"[Mr Hands] >> Setting stdout and stderr channels")
            self.stdout = self.get_channel(799322874824491079)
            self.stderr = self.get_channel(799322861343866910)
            if self.configuration.verbose:
                print(f"[Mr Hands] >> Scheduling tut timed task")
            self.scheduler.add_job(self.print_message, CronTrigger(second="1"))
            self.scheduler.start()
            if self.configuration.verbose:
                print(f"[Mr Hands] >> Setting guild")
            self.guild = self.get_guild(796810312187641878)
            print(f"[Mr Hands] >> Mr Hands:         [ OK ]")
            while not self.cog_tracker.all_ready():
                if self.configuration.verbose:
                    print(f"[Mr Hands] >> Waiting for cogs to load")
                await sleep(0.5)
            self.ready = True
        if self.configuration.verbose:
            print(f"[Mr Hands] >> All cogs loaded and bot ready")
        print(f"[Fixer] >> Fixer:               [ OK ]")
        if self.configuration.verbose:
            print(f"[Fixer] >> Fixer is now loaded and ready")
            print(f"[Fixer] >> Mr Hands has been deployed to servers")
    
    async def on_message(self, message):
        if message.author.bot and message.author != message.guild.me:
            if self.configuration.verbose:
                print("[Mr Hands] >> Received a command from another bot")
        if not message.author.bot:
            await self.process_commands(message)
