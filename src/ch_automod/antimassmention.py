import warnings
import discord
from discord.ext import commands, tasks
import datetime
from ch_boot.startup import *
from ch_boot.cmongodb import *
from ch_discord_utils.issue_penalty import ch_warn
import time
import asyncio

@charity.listen("on_message")
async def on_mass_mention(message):
    if message.author.bot:
        return
    gconfig = clc_gconfig.find_one({"_id" : message.guild.id})
    if gconfig["automod_config"]["antimassmention_config"]["module_active"]:
        if len(message.mentions) > gconfig["automod_config"]["antimassmention_config"]["massmention_threshold"]:
            tse = time.time()
            await ch_warn(
                issuer = message.guild.me,
                server_id = message.guild.id,
                member_id = message.author.id,
                reason = gconfig["automod_config"]["antimassmention_config"]["massmention_warn_reason"]
            )
            retrieved = clc_usrinfract.find_one({ "guild_id" : message.guild.id, "user_id" : message.author.id})
            if retrieved != None:
                clc_usrinfract.update_one(
                    {
                        "guild_id" : message.guild.id,
                        "user_id" : message.author.id
                    },
                    {
                        "$push" : {
                            "active_timed_infractions" : {
                                "penalty" : "warning",
                                "ini_tse" : tse,
                                "infraction" : gconfig["automod_config"]["antimassmention_config"]["massmention_warn_reason"],
                                "termination_tse" : gconfig["automod_config"]["antimassmention_config"]["massmention_warn_record_timeout"] * 60 + tse
                            }
                        }
                    }
                )
                clc_usrinfract.update_one(
                    {
                        "guild_id" : message.guild.id,
                        "user_id" : message.author.id
                    },
                    {
                        "$push" : {
                            "infractions_record" : f'[{datetime.datetime.utcfromtimestamp(tse).isoformat()}] `Warning:` {gconfig["automod_config"]["antimassmention_config"]["massmention_warn_reason"]}'
                        }
                    }
                )
            else:
                infract_obj = {
                    "guild_id" : message.guild.id,
                    "user_id" : message.author.id,
                    "active_timed_infractions" : [
                        {
                            "penalty" : "warning",
                            "ini_tse" : tse,
                            "infraction" : gconfig["automod_config"]["antimassmention_config"]["massmention_warn_reason"],
                            "termination_tse" : gconfig["automod_config"]["antimassmention_config"]["massmention_warn_record_timeout"] * 60 + tse
                        }
                    ],
                    "infractions_record" : [
                        f'[{datetime.datetime.utcfromtimestamp(tse).isoformat()}] `Warning:` {gconfig["automod_config"]["antimassmention_config"]["massmention_warn_reason"]}'
                    ]
                }
                clc_usrinfract.insert_one(infract_obj)