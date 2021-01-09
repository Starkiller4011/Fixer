#!/usr/bin/env python3
# This is the Discord Cyberpunk RED RPG Bot Configurator
# Author: Derek Blue
# Copyright (C) 2021 See LICENSE file

# Import required libraries
from pathlib import Path
import json

class Configurator:
    def __init__(self, cwd = None):
        if cwd is not None:
            self.cwd = cwd
        else:
            self.cwd = Path(__file__).parents[2]
        self.config_path = Path.joinpath(self.cwd, "config")
        self.data_path = Path.joinpath(self.cwd, "data")
        self.res_path = Path.joinpath(self.cwd, "res")
        self.libs_path = Path.joinpath(self.cwd, "libs")
        self.db_path = Path.joinpath(self.cwd, "db")
        if Path.exists(Path.joinpath(self.config_path, "config.json")):
            print("[Configurator] >> Configurator: [ OK ]")#Configuration file exists, loading config.json")
            with open(Path.joinpath(self.config_path, "config.json"), "r") as config_file:
                config = json.load(config_file)
                if "initialized" in config:
                    self.initialized = config["initialized"]
                if self.initialized:
                    print("[Configurator] >> Bot:          [ OK ]")# has been initialized, loading bot configuration")
                    if Path.exists(Path.joinpath(self.config_path, "token.json")):
                        with open(str(Path.joinpath(self.config_path, "token.json")), "r") as token_file:
                            self.token = json.load(token_file)["token"]
                    else:
                        print("[Configurator] >> Bot token is missing")
                        self.getToken()
                    self.verbose = config["verbose"]
                    self.command_prefix = config["command_prefix"]
                    self.case_insensitive = config["case_insensitive"]
                else:
                    print("[Configurator] >> Bot has not been initialized, running intial bot configuration")
                    config_file.close()
                    self.run()
        else:
            print(f"[Configurator] >> No configuration file found, running first time setup")
            print("[Configurator] >> This is the Fixer configrator. It manages the settings of the Fixer discord app.")
            self.run()
        with open(str(Path.joinpath(self.config_path, "version.json")), "r") as version_file:
            versions = json.load(version_file)
            self.app_version = versions["app_version"]
            self.bot_version = versions["bot_version"]
    
    def __str__(self): return str(repr(self))
    
    def __repr__(self): return f'Configurator(pathlib.{repr(self.cwd)})'
    
    def run(self):
        self.getToken()
        self.configureBot()
        self.initialized = True

    def getToken(self):
        self.token = input("[Configurator] >> Please enter your bot token: ")
        self.writeToken()
    
    def writeToken(self):
        with open(str(Path.joinpath(self.config_path, "token.json")), "w") as token_file:
            json.dump({"token": self.token}, token_file)

    def configureBot(self):
        self.command_prefix = input("[Configurator] >> Please enter your command prefix: ")
        self.case_insensitive = self.getYesNo("[Configurator] >> Do you want case sensitive commands? [Y|N]: ")
        self.verbose = self.getYesNo("[Configurator] >> Do you want to run in verbose mode? [Y|N]: ")
        self.initialized = True
        config = {
            "initialized": self.initialized,
            "verbose": self.verbose,
            "command_prefix": self.command_prefix,
            "case_insensitive": self.case_insensitive
        }
        with open(str(Path.joinpath(self.config_path, "config.json")), "w") as config_file:
            json.dump(config, config_file)
    
    def getYesNo(self, prompt):
        result = False
        invalid = True
        while(invalid):
            response = input(prompt)
            if response == 'y' or response == 'Y':
                result = True
                invalid = False
            elif response == 'n' or response == 'N':
                result = False
                invalid = False
            else:
                print("[Configurator] >> Invalid response")
        return result
