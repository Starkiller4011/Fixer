#!/usr/bin/env python3
# This is the Discord Cyberpunk RED RPG Bot Mr Hands
# Author: Derek Blue
# Copyright (C) 2021 See LICENSE file

# Import required libraries
import os
import json
from pathlib import Path
from discord import Intents
from discord.ext.commands import Bot
from .config import Configurator

# Mr Hands Class
class MrHands(Bot):
    def __init__(self, configuration: Configurator):
        self.configuration = configuration
        self.ready = False
        self.servers = {}
        super().__init__(
            command_prefix=self.configuration.command_prefix,
            case_insensitive=self.configuration.case_insensitive,
            intents=Intents.all()
        )
    
    def run(self):
        print("[Mr Hands] >> Running bot")
        super().run(self.configuration.token)
    
    async def on_connect(self):
        print("[Mr Hands] >> Bot has connected to the server")
    
    async def on_disconnect(self):
        print("[Mr Hands] >> Bot has disconnected from the server")
    
    async def on_ready(self):
        if not self.ready:
            for guild in self.guilds:
                guid = str(guild.id)
                if not Path.exists(Path.joinpath(self.configuration.data_path, guid)):
                    print(f'[Mr Hands] >> Joined new server: {str(guild)}, running initialization')
                    os.makedirs(Path.joinpath(self.configuration.data_path, guid))
                    category = await guild.create_category("FIXER")
                    config_channel = await category.create_text_channel("config")
                    await config_channel.send("Hey there! Looks like this is your first time using a Fixer! Let me help you get everything setup!")
                    await config_channel.send("You can use the '/config [command]' command in this channel to get things rolling for starters why don't you try running '/config help'?")
                    # system_channel = await category.create_text_channel("system")
                    # resources_channel = await category.create_text_channel("resources")
                    # await resources_channel.send(f'Rule Book:\nhttps://thetrove.is/Books/Cyberpunk/Cyberpunk%20Red/CPR%20-%20Corebook%20-%20Cyberpunk%20Red%20v122.pdf\nCharacter Sheet:\nhttps://thetrove.is/Books/Cyberpunk/Cyberpunk%20Red/CPR%20-%20Character%20Sheet%20-%20Fillable.pdf')
                    # scheduling_channel = await category.create_text_channel("scheduling")
                    # rolling_channel = await category.create_text_channel("rolling")
                    # character_sheets_channel = await category.create_text_channel("character_sheets")
                    # party_chat = await category.create_voice_channel("Party")
                    # whisper_chat = await category.create_voice_channel("Whispering")
                    # gm_chat = await category.create_voice_channel("GM-Direct")
                    # self.servers[guid] = {
                    #     "category": repr(category),
                    #     "config": repr(config_channel),
                    #     "system": repr(system_channel),
                    #     "resources": repr(resources_channel),
                    #     "scheduling": repr(scheduling_channel),
                    #     "rolling": repr(rolling_channel),
                    #     "character_sheets_channel": repr(character_sheets_channel),
                    #     "party_chat": repr(party_chat),
                    #     "whisper_chat": repr(whisper_chat),
                    #     "gm_chat": repr(gm_chat)
                    # }
                    # with open(Path.joinpath(Path.joinpath(self.configuration.data_path, guid), "config.json"), "w") as config_file:
                    #     json.dump(self.servers[guid], config_file)
                # else:
                #     print(f"[Mr Hands] >> Data folder exists for server: {str(guild)}")
                #     with open(Path.joinpath(Path.joinpath(self.configuration.data_path, guid), "config.json"), "r") as config_file:
                #         self.servers[guid] = json.load(config_file)
                # if guid in self.servers:
                #     print(f'[Mr Hands] >> Reconnected to server: {str(guild)}')
                # else:
                #     print(f'[Mr Hands] >> Joined new server: {str(guild)}')
            self.ready = True
            print("[Mr Hands] >> Bot is ready")
    
    async def on_message(self, message):
        pass
