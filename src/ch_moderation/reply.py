import discord
from discord.ext import commands
from ch_discord_utils.embed_generator import *
from ch_boot.startup import *
import typing
import re

@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def reply(
        ctx,
        jump_url,
        *, args):
    msg = "" # --msg-content
    title = ""  # --title
    description = ""  # --description
    embed = {}
    for x in args.split(sep = " "):
        if x == "--rich-embed":
            keys = re.findall(r'[-][-][^r].*?[=]', args, re.IGNORECASE)
            values = re.findall(r'["][^-].*?["]', args, re.IGNORECASE)
            for i in range(len(keys)):
                if re.search("msg-content", keys[i], re.IGNORECASE): msg = values[i][1:-1]
                elif re.search("title", keys[i], re.IGNORECASE): title = values[i][1:-1]
                elif re.search("description", keys[i], re.IGNORECASE): description = values[i][1:-1]
            kwargs = {
                "title" : title,
                "description" : description,
                "footer_text" : ctx.guild.name,
                "footer_icon_url" : ctx.guild.icon_url
            }
            embed = create_embed(**kwargs)
            dump = 0
            channel_id = jump_url[-37:][0:18]
            for i in ctx.guild.text_channels:
                if i.id == int(channel_id):
                    dump = await i.fetch_message(jump_url[-18:])
                    break
            await dump.send(content = msg, embed = embed)
            await ctx.message.add_reaction("☑️")
            return
        elif x == "--raw-embed":
            key = re.findall(r'[-][-][^r].*?[=]', args, re.IGNORECASE)
            value = re.findall(r'["][^-].*?["]', args, re.IGNORECASE)
            try:
                if re.search("description", key[0], re.IGNORECASE): description = value[0][1:-1]
                else: raise Exception("Invalid argument(s) or value(s) provided.")
            except:
                raise Exception("Invalid argument(s) or value(s) provided.")
            edict = {
                "color" : 0xf71e4b,
                "description" : description,
            }
            embed = discord.Embed.from_dict(edict)
            dump = 0
            channel_id = jump_url[-37:][0:18]
            for i in ctx.guild.text_channels:
                if i.id == int(channel_id):
                    dump = await i.fetch_message(jump_url[-18:])
                    break
            await dump.send(embed = embed)
            await ctx.message.add_reaction("☑️")
            return
    dump = 0
    channel_id = jump_url[-37:][0:18]
    for i in ctx.guild.text_channels:
        if i.id == int(channel_id):
            dump = await i.fetch_message(jump_url[-18:])
            break
    await dump.reply(content = args)
    await ctx.message.add_reaction("☑️")

@reply.error
async def msg_error(ctx, error):
    msg = "**`You lack the required permissions to perform the task.`**"
    await ctx.reply(msg + error)
