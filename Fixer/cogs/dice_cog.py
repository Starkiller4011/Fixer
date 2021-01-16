from pathlib import Path

from discord.ext.commands import command

from Fixer.lib.core import DiceRoll
from Fixer.lib.core import FixerBot
from Fixer.lib.core import FixerCog

class DiceCog(FixerCog):

    def __str__(self) -> str: return "Dice Cog"
    
    def __init__(self, bot: FixerBot) -> None:
        super().__init__(bot, Path(__file__).stem, self)
    
    @command(name="roll")
    async def roll_dice(self, context, dice_expression: str) -> None:
        """Rolls dice based on the passed expression
        """
        if 'eval' in dice_expression:
            self.configuration.logger.log(self, f"Some SERIOUSLY fishy business is going on!!!!")
            # dice_expression = dice_expression.replace('eval', '')
        self.configuration.logger.log(self, f"Evaluating roll expression: {dice_expression}")
        roll = DiceRoll(dice_expression)
        roll.to_tokens()
        roll.to_rpn()
        roll.evaluate()
        roll.to_string()
        total = roll.result
        rolls = roll.rolls
        self.configuration.logger.log(self, roll.result_string)
    
    @roll_dice.error
    async def roll_dice_error(self, context, exception):
        await context.send(f"{exception.original.message}")

def setup(bot: FixerBot) -> None:
    bot.add_cog(DiceCog(bot))
