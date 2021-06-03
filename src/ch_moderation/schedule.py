import discord
from discord.ext import commands
import asyncio
from ch_boot.startup import *

@charity.command()
async def schedule(ctx, tcid, countd, *, msg):
    dump_channel = charity.get_channel(int(tcid))
    await ctx.message.add_reaction("☑️")
    await asyncio.sleep(60 * int(countd))
    await dump_channel.send(msg)

@schedule.error
async def schedule_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
