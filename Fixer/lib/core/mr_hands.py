#!/usr/bin/env python3
# This is the Discord Cyberpunk RED RPG Bot Mr Hands
# Author: Derek Blue
# Copyright (C) 2021 See LICENSE file

# Import required libraries
import os
import json
from pathlib import Path
from discord import File
from asyncio import sleep
from discord import Embed
from discord import Intents
from datetime import datetime
from Fixer.lib.core.config import Configurator
from discord.ext.commands import Bot
from discord.ext.commands import CommandNotFound
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

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
    
    async def print_message(self):
        print(f"[Mr. Hands] >> {datetime.utcnow()}")
        # channel = self.get_channel(796810313033842710)
        # await channel.send("I am a timed notification!")
    
    async def on_connect(self):
        if self.configuration.verbose:
            print(f"[Mr Hands] >> Connected")
    
    async def on_disconnect(self):
        if self.configuration.verbose:
            print(f"[Mr Hands] >> Disconnected")
    
    async def on_error(self, event_method, *args, **kwargs):
        if event_method == "on_command_error":
            await args[0].send(f"Something went wrong.")
        channel = self.get_channel(796810313033842710)
        await channel.send(f"An error occured.")
        raise Exception
    
    async def on_command_error(self, context, exception):
        if isinstance(exception, CommandNotFound):
            pass
        elif hasattr(exception, "original"):
            raise exception.original
        else:
            raise exception
    
    async def on_ready(self):
        if not self.ready:
            self.stdout = self.get_channel(797202603565252608)
            self.scheduler.add_job(self.print_message, CronTrigger(second="1"))
            self.scheduler.start()
            self.guild = self.get_guild(796810312187641878)
            print(f"[Mr Hands] >> Mr Hands:         [ OK ]")
            while not self.cog_tracker.all_ready():
                await sleep(0.5)
            self.ready = True
        if self.configuration.verbose:
            print(f"[Mr Hands] >> Now online")
        print(f"[Fixer] >> Fixer:               [ OK ]")
        print(f"\n[Fixer] >> Fixer is now loaded and ready\n[Fixer] >> Mr Hands has been deployed to servers.\n")
    
    async def on_message(self, message):
        pass
