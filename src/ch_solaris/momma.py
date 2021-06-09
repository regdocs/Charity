from ch_boot.startup import *
import discord
from discord.ext import commands

charity.listen("on_message")
async def react_on_mommas_oranges(message):
  if "<:orange:830823490503442482>" in message.content and (message.author.id == 805108723387334657 or message.author.id == 799186130654199809:
    await message.add_reaction("<:orange:830823490503442482>")
    return
