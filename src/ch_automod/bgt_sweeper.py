import discord
from discord.ext import commands, tasks
import datetime
from ch_boot.cmongodb import *
from ch_boot.startup import *
from ch_discord_utils.issue_penalty import *
import time

@tasks.loop(seconds = 30)
async def sweep_warnings():
    current_tse = time.time()
    query = { "active_timed_infractions" : { "$elemMatch" : { "penalty" : "warning", "termination_tse" : { "$lte" : current_tse } } } }
    for doc in clc_usrinfract.find(query):
        for i in doc["active_timed_infractions"]:
            if i["penalty"] == "warning" and i["termination_tse"] <= current_tse:
                clc_usrinfract.update_one(
                    { "guild_id" : doc["guild_id"], "user_id" : doc["user_id"] },
                    { "$pull" : { "active_timed_infractions" : i } }
                )

@sweep_warnings.before_loop
async def before_sweep_warnings():
    await charity.wait_until_ready()

@tasks.loop(seconds = 30)
async def sweep_mutes():
    current_tse = time.time()
    query = { "active_timed_infractions" : { "$elemMatch" : { "penalty" : "mute", "termination_tse" : { "$lte" : current_tse } } } }
    for doc in clc_usrinfract.find(query):
        for i in doc["active_timed_infractions"]:
            if i["penalty"] == "mute" and i["termination_tse"] <= current_tse:
                clc_usrinfract.update_one(
                    { "guild_id" : doc["guild_id"], "user_id" : doc["user_id"] },
                    { "$pull" : { "active_timed_infractions" : i } }
                )
                await ch_unmute(
                    issuer = charity.get_guild(doc["guild_id"]).me,
                    server_id = doc["guild_id"],
                    member_id = doc["user_id"],
                    reason = "Mute duration expired"
                )
                gconfig = clc_gconfig.find_one({ '_id' : doc['guild_id'] })
                if gconfig["moderation_config"]["mute_config"]["bool_remove_existing_roles_and_reassign"]:
                    for x in doc["active_timed_infractions"]:
                        if x["penalty"] == "mute":
                            t = []
                            guild = charity.get_guild(doc['guild_id'])
                            for i in x["r@ini_tse"]:
                                t.append(guild.get_role(i))
                            nitro_booster_role = guild.premium_subscriber_role
                            if nitro_booster_role in t:
                                t.remove(nitro_booster_role)
                            await guild.get_member(doc['user_id']).add_roles(*t)

@sweep_mutes.before_loop
async def before_sweep_mutes():
    await charity.wait_until_ready()

@tasks.loop(seconds = 30)
async def sweep_tbans():
    current_tse = time.time()
    query = { "active_timed_infractions" : { "$elemMatch" : { "penalty" : "tban", "termination_tse" : { "$lte" : current_tse } } } }
    for doc in clc_usrinfract.find(query): 
        for i in doc["active_timed_infractions"]:
            if i["penalty"] == "tban" and i["termination_tse"] <= current_tse:
                clc_usrinfract.update_one(
                    { "guild_id" : doc["guild_id"], "user_id" : doc["user_id"] },
                    { "$pull" : { "active_timed_infractions" : i } }
                )
                clc_usrinfract.update_one(
                    { "guild_id" : doc["guild_id"], "user_id" : doc["user_id"] },
                    { "$push" : { "infractions_record" : f'[{datetime.datetime.utcfromtimestamp(current_tse).isoformat()}] `Unban:` Temporary ban duration expired' } }
                )
                await ch_unban(
                    issuer = charity.get_guild(doc["guild_id"]).me,
                    server_id = doc["guild_id"],
                    member_id = doc["user_id"],
                    reason = "Temporary ban duration expired"
                )

@sweep_tbans.before_loop
async def before_sweep_tbans():
    await charity.wait_until_ready()

sweep_warnings.start()
sweep_mutes.start()
sweep_tbans.start()