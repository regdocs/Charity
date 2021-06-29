import discord
from discord.ext import commands
from ch_boot.startup import *
import asyncio
from ch_discord_utils.issue_penalty import ch_mute
from ch_boot.cmongodb import *
import time, datetime

@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def mute(ctx, member: discord.Member, duration: float, *, message_arg: str):
    gconfig = clc_gconfig.find_one({"_id" : ctx.guild.id})
    mute_role_id = gconfig['moderation_config']['mute_config']['guild_mute_role_id']
    if mute_role_id == None:
        raise Exception("Mute role is not defined for the server.")
    if ctx.guild.get_role(mute_role_id) in member.roles:
        raise Exception("The member is already muted.")
    roles_at_ini_tse = member.roles
    if gconfig["moderation_config"]["mute_config"]["bool_remove_existing_roles_and_reassign"]:
        await member.remove_roles(*roles_at_ini_tse)
    await ch_mute(
        issuer = ctx.author,
        server_id = ctx.guild.id,
        member_id = member.id,
        duration = duration,
        reason = message_arg
    )
    tse = time.time()
    retrieved = clc_usrinfract.find_one({ "guild_id" : ctx.guild.id, "user_id" : member.id })
    if retrieved != None:
        clc_usrinfract.update_one(
            {
                "guild_id" : ctx.guild.id,
                "user_id" : member.id
            },
            {
                "$push" : {
                    "active_timed_infractions" : {
                        "penalty" : "mute",
                        "ini_tse" : tse,
                        "infraction" : message_arg,
                        "termination_tse" : duration * 60 + tse,
                        "r@ini_tse" : roles_at_ini_tse
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
                    "infractions_record" : f'[{datetime.datetime.utcfromtimestamp(tse).isoformat()}] `Mute for {duration} minute(s):` {message_arg}'
                }
            }
        )
    else:
        infract_obj = {
            "guild_id" : ctx.guild.id,
            "user_id" : member.id,
            "active_timed_infractions" : [
                {
                    "penalty" : "mute",
                    "ini_tse" : tse,
                    "infraction" : f'{message_arg}',
                    "termination_tse" : duration * 60 + tse,
                    "r@ini_tse" : roles_at_ini_tse
                }
            ],
            "infractions_record" : [
                f'[{datetime.datetime.utcfromtimestamp(tse).isoformat()}] `Mute for {duration} minute(s):` {message_arg}'
            ]
        }
        clc_usrinfract.insert_one(infract_obj)
    await ctx.message.add_reaction("☑️")
""" 
@mute.error
async def mute_error(ctx, error):
    msg = error
    await ctx.reply(msg) """