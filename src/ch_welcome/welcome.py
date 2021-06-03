import discord
from discord.ext import commands
from ch_boot.startup import *

@charity.event
async def on_member_join(member):
    await charity.get_channel(830511014302842950).send(f"Welcome to **{member.guild}**, {member.mention} :innocent: Have a great time!")
