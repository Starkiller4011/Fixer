#!/usr/bin/env python3
# This is the Discord Cyberpunk RED RPG App
# Author: Derek Blue
# Copyright (C) 2021 See LICENSE file

from pathlib import Path
from sqlite3 import connect
from Fixer.lib.core.config import Configurator
from apscheduler.triggers.cron import CronTrigger

class DataBase:

    def __str__(self) -> str: return "DataBase"

    def __init__(self, configuration: Configurator):
        self.configuration = configuration
        self.database_path = Path.joinpath(self.configuration.db_path, "database.db")
        self.build_path = Path.joinpath(self.configuration.db_path, "build.sql")
        self.connection = connect(self.database_path, check_same_thread=False)
        self.cursor = self.connection.cursor()
    
    def build(self):
        if Path.is_file(self.build_path):
            if self.configuration.verbose:
                print(f"[DataBase] >> Running initial build")
            self.scriptexec(self.build_path)
            self.configuration.logger.module_ready(self)
            # print(f"[DataBase] >> Database:         [ OK ]")
    
    def commit(self):
        if self.configuration.verbose:
            print(f"[DataBase] >> Committing")
        self.connection.commit()

    def close(self):
        self.connection.close()

    def autosave(self, scheduler):
        scheduler.add_job(self.commit, CronTrigger(second=0))

    def field(self, command, *values):
        self.cursor.execute(command, tuple(values))
        if (fetch := self.cursor.fetchone()) is not None:
            return fetch[0]

    def record(self, command, *values):
        self.cursor.execute(command, tuple(values))
        return self.cursor.fetchone()

    def records(self, command, *values):
        self.cursor.execute(command, tuple(values))
        return self.cursor.fetchall()

    def column(self, command, *values):
        self.cursor.execute(command, tuple(values))
        return [item[0] for item in self.cursor.fetchall()]

    def execute(self, command, *values):
        self.cursor.execute(command, tuple(values))

    def multiexec(self, command, valueset):
        self.cursor.executemany(command, valueset)

    def scriptexec(self, path):
        with open(path, "r", encoding="utf-8") as script:
            self.cursor.executescript(script.read())
