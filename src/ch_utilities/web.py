import discord
from discord.ext import commands
from googlesearch import search
from ch_boot.startup import *

@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def web(ctx, *, searchstring):
    await ctx.channel.trigger_typing()
    results = search(searchstring, safe='on', tld="com", num=1, stop=1, pause=0.5)
    for j in results:
        await ctx.channel.send(":card_box: `TOP RESULT FROM google, tld:com` {}".format(j))

@web.error
async def web_error(ctx, error):
    msg = error
    await ctx.reply(msg)
