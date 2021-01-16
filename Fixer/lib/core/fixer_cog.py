from Fixer.lib.core import MrHands
from Fixer.lib.core import Configurator
from discord.ext.commands import Cog

class FixerCog(Cog):
    
    def __init__(self, bot: MrHands, filename: str, cog_name: str) -> None:
        self.bot: MrHands = bot
        self.cname: str = str(cog_name)
        self.fname: str = str(filename)
        self.configuration: Configurator = bot.configuration
        super().__init__()

    @Cog.listener()
    async def on_ready(self) -> None:
        if not self.bot.ready:
            if self.configuration.verbose:
                print(f"[{self.cname}] >> Bot is not ready, readying up")
            self.bot.cog_tracker.ready_up(self.fname)
        self.bot.configuration.logger.module_ready(self.cname)
        # print(f"[{self.cname}] >> Cog:          [ OK ]")
