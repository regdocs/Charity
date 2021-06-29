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

@sweep_warnings.before_loop
async def before_sweep_mutes():
    await charity.wait_until_ready()

@tasks.loop(seconds = 30)
async def sweep_tban():
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

@sweep_warnings.before_loop
async def before_sweep_tban():
    await charity.wait_until_ready()

sweep_warnings.start()
sweep_mutes.start()
sweep_tban.start()