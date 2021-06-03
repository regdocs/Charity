import discord
from discord.ext import commands
from ch_boot.startup import *

@charity.listen("on_message")
async def on_dmessage(message):
    if not message.guild and message.author.id != charity.user.id:
        await message.add_reaction("☑️")
        dm_dump_channel = charity.get_channel(840645965949829140)
        await dm_dump_channel.send("**DIRECT MESSAGE FROM <@{}> PFID:** `{}`**:**\n**CONTENT:** {}".format(message.author.id, message.author.id, message.content))
