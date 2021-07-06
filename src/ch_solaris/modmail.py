import discord
from discord.ext import commands
from ch_boot.startup import *

@charity.listen("on_message")
async def on_dmessage(message):
    return