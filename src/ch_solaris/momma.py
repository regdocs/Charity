from ch_boot.startup import *
import discord
from discord.ext import commands

@charity.listen("on_message")
async def react_on_mommas_oranges(message):
  if "<:orange:" in message.content and message.author.id == 805108723387334657:
    humble_abode = await charity.fetch_guild(829811466906632213)
    await message.add_reaction(await humble_abode.fetch_emoji(841124452283580417))
    return
