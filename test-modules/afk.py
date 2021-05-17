import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()
activity = discord.Activity(name='with Charity', type=discord.ActivityType.watching)
afkbot = commands.Bot(command_prefix = '.', activity = activity, intents = intents)

@afkbot.event
async def on_ready():
    print('Logged in as {} PFID: {}\n-------------------------------------------------'.format(afkbot.user, afkbot.user.id))

#*********************************************** # GLOBAL SCOPE
afk_dump = {}

#----------------------------------------------- # Module afk
@afkbot.command()
async def afk(ctx, *, afkstring):
    if "<@" in afkstring:
            await ctx.reply("You cannot tag guild members in your AFK note.")
            return
    await ctx.message.add_reaction("🌙")
    await asyncio.sleep(5)
    afk_dump[ctx.message.author.id] = afkstring

@afkbot.listen("on_message")
async def ifpingonafk(message):
    if  message.author == afkbot.user:
        return
    if len(afk_dump.keys()) == 0 or "<@" not in message.content:
        return
    afk_dump_key_state = afk_dump.keys()
    notif_msg_array = []
    for x in afk_dump_key_state:
        if "<@{}>".format(str(x)) in message.content:
            msg = await message.channel.send("`{} is AFK:` _{}_".format(afkbot.get_user(x).name, afk_dump.get(x)))
            notif_msg_array.append(msg)
    await asyncio.sleep(5)
    for y in notif_msg_array:
        await y.delete()

@afkbot.listen("on_message")
async def removeafk(message):
    if len(afk_dump.keys()) == 0:
        return
    to_be_popped_dump = []
    for x in afk_dump.keys():
        if message.author.id == x:
            await message.channel.send("<@{}> `Welcome back, removed your AFK` ✅".format(message.author.id), delete_after = 5)
            to_be_popped_dump.append(message.author.id)
    for y in to_be_popped_dump:
        afk_dump.pop(y)

afkbot.run('ODQyNjAyNjM5NjAxODI3ODgx.YJ3s3A.owkxSnN7g4aJqbwsBOTPqEIyz3E')