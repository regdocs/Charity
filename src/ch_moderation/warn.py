import discord
from discord.ext import commands
from ch_boot.startup import *
from ch_boot.cmongodb import *
from ch_discord_utils.issue_penalty import ch_warn
import time, datetime, typing

@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def warn(ctx, member: discord.Member, duration: typing.Optional[float] = 86400, *, message_arg: str):
    if ctx.author.top_role.position <= member.top_role.position:
        raise Exception("Cannot execute moderation commands for members ranked same or higher than you.")
    await ch_warn(
        issuer = ctx.author,
        server_id = ctx.guild.id,
        member_id = member.id,
        reason = message_arg
    )
    tse = time.time()
    retrieved = clc_usrinfract.find_one({ "guild_id" : ctx.guild.id, "user_id" : member.id})
    if retrieved != None:
        clc_usrinfract.update_one(
            {
                "guild_id" : ctx.guild.id,
                "user_id" : member.id
            },
            {
                "$push" : {
                    "active_timed_infractions" : {
                        "penalty" : "warning",
                        "ini_tse" : tse,
                        "infraction" : message_arg,
                        "termination_tse" : duration * 60 + tse
                    }
                }
            }
        )
        clc_usrinfract.update_one(
            {
                "guild_id" : ctx.guild.id,
                "user_id" : member.id
            },
            {
                "$push" : {
                    "infractions_record" : f'[{datetime.datetime.utcfromtimestamp(tse).isoformat()}] `Warning for {duration} minute(s):` {message_arg}'
                }
            }
        )
    else:
        infract_obj = {
            "guild_id" : ctx.guild.id,
            "user_id" : member.id,
            "active_timed_infractions" : [
                {
                    "penalty" : "warning",
                    "ini_tse" : tse,
                    "infraction" : f'{message_arg}',
                    "termination_tse" : duration * 60 + tse
                }
            ],
            "infractions_record" : [
                f'[{datetime.datetime.utcfromtimestamp(tse).isoformat()}] `Warning for {duration} minute(s):` {message_arg}'
            ]
        }
        clc_usrinfract.insert_one(infract_obj)
    await ctx.message.add_reaction("☑️")

@warn.error
async def warn_error(ctx, error):
    msg = error
    await ctx.reply(msg)