# from random import choice
# from random import randint
# from typing import Optional
# from aiohttp import request

# from discord import Embed
# from discord import Member
# from discord.ext.commands import Cog
# from discord.ext.commands import command
# from discord.ext.commands import BadArgument

# from Fixer.lib.core import MrHands
# from Fixer.lib.core import Configurator
# from Fixer.lib.core import get_colour
# from Fixer.lib.core import get_colour


# class DiceCountException(Exception):
#     pass

# class DiceTypeException(Exception):
#     pass

# class Fun(Cog):

#     activated = True

#     def __init__(self, bot: MrHands) -> None:
#         self.bot = bot
#         self.configuration: Configurator = bot.configuration
#         super().__init__()

#     @Cog.listener()
#     async def on_ready(self):
#         if not self.bot.ready:
#             self.bot.cog_tracker.ready_up('fun_tut_cog')
#         # print(f"[Fun Cog] >> Fun Cog:           [ OK ]")
    
#     # Test Command
#     @command(name="test", aliases=["test1", "test2"])
#     async def test(self, context):
#         if not self.activated:
#             if self.configuration.verbose:
#                 print(f"[Fun Cog] >> Cog not active")
#             return
#         if self.configuration.verbose:
#             print(f"[Fun Cog] >> Test command sent")
#         await context.message.delete()
#         await context.send(f"{choice(('Hello', 'Hi', 'Hey', 'Hiya'))} {context.author.mention}")
    
#     # # Roll Dice Command
#     # @command(name="dice", aliases=["roll"])
#     # async def roll_dice(self, context, die_string: str):
#     #     if not self.activated:
#     #         if self.configuration.verbose:
#     #             print(f"[Fun Cog] >> Cog not active")
#     #         return
#     #     if self.configuration.verbose:
#     #         print(f"[Fun Cog] >> Dice command sent")
#     #     dice, value = (int(term) for term in die_string.split("d"))
#     #     if dice <= 50:
#     #         rolls = [randint(1, value) for i in range(dice)]
#     #         if self.configuration.verbose:
#     #             print(f"[Fun Cog] >> Dice roll result: " + " + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")
#     #         await context.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")
#     #     else:
#     #         raise DiceCountException
    
#     # # Roll Dice Command Error Handling
#     # @roll_dice.error
#     # async def roll_dice_error(self, context, exception):
#     #     if isinstance(exception.original, DiceCountException):
#     #         if self.configuration.verbose:
#     #             print(f"[Fun Cog] >> Too many dice rolls requested")
#     #         await context.send(f"Too many dice rolls punk, use less dice dumbass!")
    
#     # Slap Member Command
#     @command(name="slap")
#     async def slap_member(self, context, member: Member, *, reason: Optional[str] = "for no reason"):
#         if not self.activated:
#             if self.configuration.verbose:
#                 print(f"[Fun Cog] >> Cog not active")
#             return
#         if self.configuration.verbose:
#             print(f"[Fun Cog] >> {context.author.display_name} slapped {member.display_name} {reason}!")
#         await context.send(f"{context.author.display_name} slapped {member.display_name} {reason}!")
    
#     # Slap Member Command Error Handling
#     @slap_member.error
#     async def slap_member_error(self, context, exception):
#         if isinstance(exception, BadArgument):
#             if self.configuration.verbose:
#                 print(f"[Fun Cog] >> Could not find member to slap")
#             await context.send(f"I couldn't find that member... Are you sure they exist moron?")
    
#     # Fact Command, external API tut
#     @command(name="fact")
#     async def animal_fact(self, context, animal: str):
#         if not self.activated:
#             if self.configuration.verbose:
#                 print(f"[Fun Cog] >> Cog not active")
#             return
#         fact_colours = {
#             "dog": get_colour("cyan", "primary"),
#             "cat": get_colour("pink", "primary"),
#             "panda": get_colour("white", "primary"),
#             "fox": get_colour("amber", "primary"),
#             "bird": get_colour("green", "primary"),
#             "koala": get_colour("brown", "primary")
#         }
#         if (animal := animal.lower()) in ["dog", "cat", "panda", "fox", "bird", "koala"]:
#             if self.configuration.verbose:
#                 print(f"[Fun Cog] >> Getting fact on animal: {animal}")
#             fact_url = f"https://some-random-api.ml/facts/{animal}"
#             img_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"
#             if self.configuration.verbose:
#                 print(f"[Fun Cog] >> Requesting fact URL: {fact_url}")
#                 print(f"[Fun Cog] >> Requesting image URL: {img_url}")
#             async with request("GET", img_url, headers={}) as response:
#                 if self.configuration.verbose:
#                     print(f"[Fun Cog] >> Recieved response")
#                 if response.status == 200:
#                     if self.configuration.verbose:
#                         print(f"[Fun Cog] >> Image available, getting image")
#                     data = await response.json()
#                     image_link = data["link"]
#                 else:
#                     if self.configuration.verbose:
#                         print(f"[Fun Cog] >> Image not available")
#                     image_link = None
#             async with request("GET", fact_url, headers={}) as response:
#                 if response.status == 200:
#                     if self.configuration.verbose:
#                         print(f"[Fun Cog] >> Fact available, getting fact")
#                     data = await response.json()
#                     embed = Embed(title=f"{animal.title()} fact",
#                                   description=data["fact"],
#                                   colour=fact_colours[animal.lower()])
#                     if image_link is not None:
#                         embed.set_image(url=image_link)
#                     if self.configuration.verbose:
#                         print(f"[Fun Cog] >> Sending fact to server")
#                     await context.send(embed=embed)
#                 else:
#                     if self.configuration.verbose:
#                         print(f"[Fun Cog] >> API returned a {response.status} status")
#                     await self.bot.stderr.send(f"API returned a {response.status} status")
#         else:
#             if self.configuration.verbose:
#                 print(f"[Fun Cog] >> No facts available for animal: {animal}")
#             await context.send(f"No facts available for that animal")

#     # Echo Command
#     @command(name="echo")
#     async def echo_message(self, context, *, message):
#         if not self.activated:
#             if self.configuration.verbose:
#                 print(f"[Fun Cog] >> Cog not active")
#             return
#         if self.configuration.verbose:
#             print(f"[Fun Cog] >> Echoing message: {message}")
#         # await context.message.delete()
#         await context.send(message)

#     @Cog.listener()
#     async def on_ready(self):
#         if not self.bot.ready:
#             self.bot.cog_tracker.ready_up('fun_tut_cog')
#         # print(f"[Fun Cog] >> Fun Cog:           [ OK ]")

# def setup(bot):
#     bot.add_cog(Fun(bot))
