from ch_boot.startup import *
import discord
from discord.ext import commands
from ch_boot.cmongodb import *
from ch_boot.client_token import GUILD_CONFIGURATION

@charity.event
async def on_guild_join(guild):
    if clc_gconfig.find_one({ "_id" : f"{guild.id}" }) is not None:
        return
    new_config = GUILD_CONFIGURATION
    new_config["_id"] = guild.id
    clc_gconfig.insert_one(new_config)