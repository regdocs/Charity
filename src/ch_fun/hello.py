import discord
from discord.ext import commands
from ch_boot.startup import *

@charity.command(name = "hello")
async def say_hello(ctx, arg):
    if ctx.author.id == 799186130654199809:
        await ctx.reply("Hey Dad! <:heartz:844352117674082305>")
    elif ctx.author.id == 819439855880372246:
        await ctx.reply("Hello son of WhiteFang of Hidden Leaf, Disciple of YellowFlash, Sixth Hokage of Leaf, The Copy Ninja, Hatake Kakashi of Sharingan! <:drake_yes:830863359716229160>")
    elif ctx.author.id == 798549177755107329:
        await ctx.reply("Hello Aunt! <:slsm:845359515570667550>")
    elif arg.lower() == "charity":
        await ctx.reply("Hello {}! <:orange:841124452283580417>".format(ctx.author.name))

@say_hello.error
async def say_hello_error(ctx, error):
    msg = error
    await ctx.reply(msg)
