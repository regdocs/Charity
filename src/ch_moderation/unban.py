import discord
from discord.ext import commands
from ch_boot.startup import *
from ch_boot.cmongodb import *
from ch_discord_utils.issue_penalty import ch_unban
import datetime, time

@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def unban(ctx, member: discord.User, *, message_arg):
    if not ctx.channel.permissions_for(ctx.author).ban_members:
        raise Exception("You don't have the permissions to execute this command.")
    await ch_unban(
        issuer = ctx.author,
        server_id = ctx.guild.id,
        member_id = member.id,
        reason = message_arg
    )
    tse = time.time()
    gconfig = clc_gconfig.find_one({"_id" : ctx.guild.id})
    retrieved = clc_usrinfract.find_one({ "guild_id" : ctx.guild.id, "user_id" : member.id})
    if retrieved != None:
        clc_usrinfract.update_one(
            {
                "guild_id" : ctx.guild.id,
                "user_id" : member.id
            },
            {
                "$push" : {
                    "infractions_record" : f'[{datetime.datetime.utcfromtimestamp(tse).isoformat()}] `Unban:` {message_arg}'
                }
            }
        )
    else:
        infract_obj = {
            "guild_id" : ctx.guild.id,
            "user_id" : member.id,
            "active_timed_infractions" : [],
            "infractions_record" : [
                f'[{datetime.datetime.utcfromtimestamp(tse).isoformat()}] `Unban:` {message_arg}'
            ]
        }
        clc_usrinfract.insert_one(infract_obj)
    await ctx.message.add_reaction("☑️")

@unban.error
async def ban_error(ctx, error):
    msg = error
    await ctx.reply(msg)