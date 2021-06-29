import discord
from discord.ext import commands
import urllib.parse, urllib.request, re
from ch_boot.startup import *

@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def yt(ctx, *, search):
    query_string = urllib.parse.urlencode({'search_query': search})
    htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
    await ctx.reply('`TOP RESULT:` http://www.youtube.com/watch?v=' + search_results[0])

@yt.error
async def yt_error(ctx, error):
    msg = error
    await ctx.reply(msg)
