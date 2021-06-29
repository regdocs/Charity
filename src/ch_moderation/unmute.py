import discord
from discord.ext import commands
from ch_boot.startup import *
from ch_boot.cmongodb import *
from ch_discord_utils.issue_penalty import ch_unmute
import datetime, time

@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def unmute(ctx, member: discord.Member, *, message_arg: str):
    gconfig = clc_gconfig.find_one({"_id" : ctx.guild.id})
    mute_role_id = gconfig['moderation_config']['mute_config']['guild_mute_role_id']
    if mute_role_id == None:
        raise Exception("Mute role is not defined for the server.")
    if ctx.guild.get_role(mute_role_id) not in member.roles:
        raise Exception("The member is not muted.")
    await ch_unmute(
        issuer = ctx.author,
        server_id = ctx.guild.id,
        member_id = member.id,
        reason = message_arg
    )
    retrieved = clc_usrinfract.find_one({ "guild_id" : ctx.guild.id, "user_id" : member.id})
    if gconfig["moderation_config"]["mute_config"]["bool_remove_existing_roles_and_reassign"]:
        for x in retrieved["active_timed_infractions"]:
            if x["penalty"] == "mute":
                t = [ ctx.guild.get_role(i) for i in x["r@ini_tse"] ]
                await member.add_roles(*t)
    tse = time.time()
    clc_usrinfract.update_one(
        {
            "guild_id" : ctx.guild.id,
            "user_id" : member.id
        },
        {
            "$pull" : {
                "active_timed_infractions" : { "penalty" : "mute" }
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
                "infractions_record" : f'[{datetime.datetime.utcfromtimestamp(tse).isoformat()}] `Unmute:` {message_arg}'
            }
        }
    )
    await ctx.message.add_reaction("☑️")

@unmute.error
async def unmute_error(ctx, error):
    msg = error
    await ctx.reply(msg)