import discord
from discord.ext import commands
from ch_boot.startup import *
from ch_boot.cmongodb import *
import asyncio
import typing
import re

@charity.command()
async def afk(ctx, *, afkstring: typing.Optional[str] = "\0"):
    gconfig = clc_gconfig.find_one({"_id" : ctx.guild.id})
    if gconfig["utilities_config"]["afk_config"]["bool_mentions_allowed"] == False:
        if len(ctx.message.raw_mentions) != 0:
            await ctx.reply(":warning: `You cannot mention guild members in your AFK note.`")
            return
    maxlength = gconfig["utilities_config"]["afk_config"]["afk_note_max_length"]
    if len(afkstring) > maxlength:
        await ctx.reply(f":warning: `Your AFK note cannot exceed {maxlength} characters.`")
        return
    if ctx.message.mention_everyone or '@everyone' in ctx.message.content:
        await ctx.reply(f":warning: `Your AFK note cannot mention everyone.`")
        return
    if gconfig["utilities_config"]["afk_config"]["bool_link_allowed"] == False:
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex, afkstring)
        if len(url) != 0:
            await ctx.reply(":warning: `Your AFK note cannot contain links.`")
            return
    entry = {
        u"user_id" : ctx.author.id,
        u"server_id" : ctx.guild.id,
        u"afk_note" : u"{}".format(afkstring)
    }
    await ctx.message.add_reaction("🌙")
    await ctx.channel.send(f"**{ctx.author.mention} `Set your AFK`** :ballot_box_with_check:")
    await asyncio.sleep(3)
    retrieved = clc_afk.find_one({"user_id" : ctx.author.id, "server_id" : ctx.guild.id})
    if retrieved != None:
        clc_afk.update_one({"user_id" : ctx.author.id, "server_id" : ctx.guild.id}, {"$set" : {u"afk_note" : u"{}".format(afkstring)}})
    else:
        clc_afk.insert_one(entry)

@afk.error
async def afk_error(ctx, error):
    msg = "**:skull_crossbones: `An unexpected error occured.`**"
    await ctx.reply(msg)

@charity.listen("on_message")
async def ifpingonafk(message):
    if  message.author == charity.user:
        return
    if len(message.mentions) == 0:
        return
    all_mentions = [i for i in message.mentions]
    def return_discordMember_from_mention(member: typing.Optional[discord.Member]):
        return member
    for x in all_mentions:
        member = return_discordMember_from_mention(x)
        retrieved = clc_afk.find_one({"user_id" : x.id, "server_id" : message.guild.id})
        if retrieved is not None:
            if retrieved["afk_note"] == '\0':
                await message.channel.send(f"**`{member.display_name} is AFK and umm, they didn't leave a note`** :smiling_face_with_tear:")
            else:
                await message.channel.send(f"**`{member.display_name} is AFK:`** {retrieved['afk_note']}")

@charity.listen("on_message")
async def removeafk(message):
    retrieved = clc_afk.find_one({"user_id" : message.author.id, "server_id" : message.guild.id})
    if retrieved != None and message.content.startswith(";afk"):
        return
    if retrieved == None:
        return
    await message.channel.send(f"{message.author.mention} **`Welcome back, removed your AFK`** ☑️", delete_after = 5)
    clc_afk.delete_one(retrieved)
