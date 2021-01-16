from pathlib import Path
from datetime import datetime

class Logger :
    """ Logger Class """

    def __str__(self): return "Logger"
    
    def __repr__(self): return f"Logger()"

    def __init__(self, log_path):
        self.events_log = Path.joinpath(log_path, "events.log")
        self.startup_log = Path.joinpath(log_path, "startup.log")

    def module_ready(self, module):
        m = str(module)
        print(f"[{m}] {'[ OK ]':>{30 - len(m)}}")
        with open(self.startup_log, 'a') as log_file:
            log_file.write(f"[{datetime.utcnow()}] [{m}] {'[ OK ]':>{20 - len(m)}}\n")
    
    def log(self, sender, message):
        print(f"[{str(sender)}] >> {message}")
        self.log_to_file(sender, message)
    
    def log_to_file(self, sender, message):
        with open(self.events_log, 'a') as log_file:
            log_file.write(f"[{datetime.utcnow()}] [{str(sender)}] >> {message}\n")
    
    def get_input(self, sender, prompt):
        return input(f"[{str(sender)}] >> {prompt}: ")
