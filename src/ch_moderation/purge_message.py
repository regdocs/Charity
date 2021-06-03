import discord
from discord.ext import commands
from ch_boot.startup import *

@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def clr(ctx, limit, arg = None):
    limit = int(limit)
    counter = 0
    if limit > 200:
        raise Exception("Limit cannot exceed `200` messages.")
    if arg == None:
        await ctx.channel.trigger_typing()
        counter = await ctx.channel.purge(limit = limit + 1)
        counter = len(counter)
    elif arg == "--ignore-pins":
        await ctx.channel.trigger_typing()
        async for x in ctx.channel.history(limit = limit + 1):
            if x.pinned == False:
                await x.delete()
                counter += 1
    else:
        raise Exception("Invalid argument received.")
    await ctx.channel.send(f"`{counter} messages purged.` :ballot_box_with_check:", delete_after = 7)
    
@clr.error
async def clr_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
