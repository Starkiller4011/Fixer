#!/usr/bin/env python3
# This is the Discord Cyberpunk RED RPG Bot Configurator
# Author: Derek Blue
# Copyright (C) 2021 See LICENSE file

# Import required libraries
import json
from pathlib import Path

# Import Fixer specific libraries
from Fixer.lib.core.logger import Logger

class Configurator:
    """Configurator Class"""
    
    def __str__(self): return "Configurator"
    
    def __repr__(self): return f"Configurator({'True' if self.verbose else 'False'})"

    def __init__(self, verbose = False):
        self.verbose = verbose
        self.initialized = False
        self.new_verbosity = None
        self.cwd = Path(__file__).parents[2]
        self.config_path = Path.joinpath(self.cwd, "config")
        self.res_path = Path.joinpath(self.cwd, "res")
        self.libs_path = Path.joinpath(self.cwd, "libs")
        self.db_path = Path.joinpath(self.cwd, "db")
        self.log_path = Path.joinpath(self.cwd, "logs")
        self.logger = Logger(self.log_path)
        self._token_exists = Path.exists(Path.joinpath(self.config_path, "token.json"))
        self._config_exists = Path.exists(Path.joinpath(self.config_path, "config.json"))
        if self.verbose:
            self.logger.log(self, f"CWD: {self.cwd}")
            self.logger.log(self, f"Config path: {self.config_path}")
            self.logger.log(self, f"Resources path: {self.res_path}")
            self.logger.log(self, f"Libraries path: {self.libs_path}")
            self.logger.log(self, f"Database path: {self.db_path}")
            self.logger.log(self, f"Log path: {self.log_path}")
            self.logger.log(self, f"Token file exists: {'True' if self._token_exists else 'False'}")
            self.logger.log(self, f"Config file exists: {'True' if self._config_exists else 'False'}")
        else:
            self.logger.log_to_file(self, f"CWD: {self.cwd}")
            self.logger.log_to_file(self, f"Config path: {self.config_path}")
            self.logger.log_to_file(self, f"Resources path: {self.res_path}")
            self.logger.log_to_file(self, f"Libraries path: {self.libs_path}")
            self.logger.log_to_file(self, f"Database path: {self.db_path}")
            self.logger.log_to_file(self, f"Log path: {self.log_path}")
            self.logger.log_to_file(self, f"Token file exists: {'True' if self._token_exists else 'False'}")
            self.logger.log_to_file(self, f"Config file exists: {'True' if self._config_exists else 'False'}")
    
    # Log configurator as ready
    def ready(self):
        self.logger.module_ready(self)

    # Write the token to token file
    def writeToken(self):
        if self.verbose:
            self.logger.log(self, f"Writing token to file")
        else:
            self.logger.log_to_file(self, f"Writing token to file")
        with open(str(Path.joinpath(self.config_path, "token.json")), "w") as token_file:
            json.dump({"token": self.token}, token_file)
    
    # Load token from token file
    def loadToken(self):
        if self.verbose:
            self.logger.log(self, f"Loading token from file")
        else:
            self.logger.log_to_file(self, f"Loading token from file")
        with open(str(Path.joinpath(self.config_path, "token.json")), "r") as token_file:
            self.token = json.load(token_file)["token"]
    
    # Get the user to set the token
    def getToken(self):
        self.token = self.logger.get_input(self, "Please enter your bot token")
        self.writeToken()
    
    # Write the configuration to config file
    def writeConfig(self):
        config = {
            "initialized": self.initialized,
            "verbose": self.verbose,
            "command_prefix": self.command_prefix,
            "case_insensitive": self.case_insensitive
        }
        with open(str(Path.joinpath(self.config_path, "config.json")), "w") as config_file:
            json.dump(config, config_file)
    
    # Load configuration from config file
    def loadConfig(self):
        with open(str(Path.joinpath(self.config_path, "config.json")), "r") as config_file:
            config = json.load(config_file)
            self.initialized = config["initialized"]
            self.command_prefix = config["command_prefix"]
            self.case_insensitive = config["case_insensitive"]
            if self.verbose != config["verbose"]:
                self.new_verbosity = config["verbose"]
            else:
                self.verbose = config["verbose"]
    
    # Get configuration from user
    def getConfig(self):
        self.command_prefix = self.logger.get_input(self, f"Please enter your command prefix")#input(f"[Configurator] >> Please enter your command prefix: ")
        self.case_insensitive = self.getYesNo(f"Do you want case sensitive commands? [Y|N]")
        verbose = self.getYesNo(f"Do you want to run in verbose mode? [Y|N]")
        if self.verbose != verbose:
            self.new_verbosity = verbose
        else:
            self.verbose = verbose
        self.initialized = True
        self.writeConfig()
    
    # Set the token directly
    def setToken(self, token):
        self.token = token
        self.writeToken()
    
    # Set the verbosity directly
    def setVerbose(self, verbose):
        self.verbose = verbose
    
    # Set the command prefix directly
    def setCommandPrefix(self, command_prefix):
        self.command_prefix = command_prefix
    
    # Set the case insensitivity directly
    def setCaseInsensitive(self, case_insensitive):
        self.case_insensitive = case_insensitive
    
    # Set the intialized state directly
    def initialize(self):
        self.initialized = True
    
    # Load configuration and token if available
    # Get user input if not
    def load(self):
        if self._config_exists:
            if self.verbose:
                self.logger.log(self, f"Config file found, loading existing configuration")
            else:
                self.logger.log_to_file(self, f"Config file found, loading existing configuration")
            self.loadConfig()
            if self.verbose:
                self.logger.log(self, f"Initialized: {'True' if self.initialized else 'False'}")
                self.logger.log(self, f"Command Prefix: '{self.command_prefix}'")
                self.logger.log(self, f"Case Sensitive: {'False' if self.case_insensitive else 'True'}")
            else:
                self.logger.log_to_file(self, f"Initialized: {'True' if self.initialized else 'False'}")
                self.logger.log_to_file(self, f"Command Prefix: '{self.command_prefix}'")
                self.logger.log_to_file(self, f"Case Sensitive: {'False' if self.case_insensitive else 'True'}")
        else:
            print("************** USER INPUT **************")
            if self.verbose:
                self.logger.log(self, f"Config file not found, getting initial configuration")
            else:
                self.logger.log_to_file(self, f"Config file not found, getting initial configuration")
            self.getConfig()
            if self.verbose:
                self.logger.log(self, f"Configuration set")
            else:
                self.logger.log_to_file(self, f"Configuration set")
            if self._token_exists:
                print("****************************************")
        if self._token_exists:
            if self.verbose:
                self.logger.log(self, f"Token file found, loading bot token")
            else:
                self.logger.log_to_file(self, f"Token file found, loading bot token")
            self.loadToken()
        else:
            if self._config_exists:
                print("************** USER INPUT **************")
            if self.verbose:
                self.logger.log(self, f"No token file found, getting token")
            else:
                self.logger.log_to_file(self, f"No token file found, getting token")
            self.getToken()
            if self.verbose:
                self.logger.log(self, f"Token set")
            else:
                self.logger.log_to_file(self, f"Token set")
            print("****************************************")
        if self.new_verbosity is not None:
            if self.verbose:
                self.logger.log(self, "Changing verbosity")
            else:
                self.logger.log_to_file(self, "Changing verbosity")
            self.verbose = self.new_verbosity
            del self.new_verbosity
        self.ready()
    
    def getYesNo(self, prompt):
        while(True):
            response = self.logger.get_input(self, prompt)
            if (response == 'y' or response == 'Y' or response == 'n' or response == 'N'):
                return (response == 'y' or response == 'Y')
            else:
                self.logger.log(self, f"Invalid response")
