import discord
from discord.ext import commands
from ch_boot.startup import *
import asyncio
from ch_boot.cmongodb import *

afk_dump = {}
@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def afk(ctx, *afkstring):
    if len(ctx.message.raw_mentions) != 0:
            await ctx.reply(":warning: `You cannot tag guild members in your AFK note.`")
            return
    afkstring = ' '.join(afkstring)
    if len(afkstring) == 0: afkstring = "No reason specified."
    await ctx.message.add_reaction("🌙")
    await ctx.channel.send(f"**{ctx.author.mention} Set you AFK.** :ballot_box_with_check:")
    await asyncio.sleep(3)
    afk_dump[ctx.message.author.id] = afkstring

@afk.error
async def afk_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)

@charity.listen("on_message")
async def ifpingonafk(message):
    if  message.author == charity.user:
        return
    if len(afk_dump.keys()) == 0 or len(message.mentions) == 0:
        return
    notif_msg_array = []
    for x in afk_dump.keys():
        if message.guild.get_member(x) in message.mentions:
            msg = await message.channel.send("**{}** is AFK: _{}_".format(message.guild.get_member(x).name, afk_dump.get(x)), delete_after = 5)
            notif_msg_array.append(msg)

@charity.listen("on_message")
async def removeafk(message):
    if len(afk_dump.keys()) == 0:
        return
    to_be_popped_dump = []
    for x in afk_dump.keys():
        if message.author.id == x:
            await message.channel.send("<@{}> `Welcome back, removed your AFK` ☑️".format(message.author.id), delete_after = 5)
            to_be_popped_dump.append(message.author.id)
    for y in to_be_popped_dump:
        afk_dump.pop(y)