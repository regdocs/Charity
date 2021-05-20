import client_token
import discord
from discord.ext import commands, tasks
import urllib.parse, urllib.request, re
from googlesearch import search
import youtube_dl
import datetime
import asyncio
import logging
import typing
import time

intents = discord.Intents.all()
activity = discord.Activity(name='over Solaris', type=discord.ActivityType.watching)
charity = commands.Bot(command_prefix = ';', activity = activity, intents = intents, status=discord.Status.dnd)

def logger():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='./log/high-charity.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

def startup():
    print()
    print("  ░█████╗░██╗░░██╗░█████╗░██████╗░██╗████████╗██╗░░░██╗░░░██████╗░██╗░░░██╗")
    print("  ██╔══██╗██║░░██║██╔══██╗██╔══██╗██║╚══██╔══╝╚██╗░██╔╝░░░██╔══██╗╚██╗░██╔╝")
    print("  ██║░░╚═╝███████║███████║██████╔╝██║░░░██║░░░░╚████╔╝░░░░██████╔╝░╚████╔╝░")
    print("  ██║░░██╗██╔══██║██╔══██║██╔══██╗██║░░░██║░░░░░╚██╔╝░░░░░██╔═══╝░░░╚██╔╝░░")
    print("  ╚█████╔╝██║░░██║██║░░██║██║░░██║██║░░░██║░░░░░░██║░░░██╗██║░░░░░░░░██║░░░")
    print("  ░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░╚═╝░░░░░░╚═╝░░░╚═╝╚═╝░░░░░░░░╚═╝░░░")
    print()
    print("  # Script          : charity.py")
    print("  # Version         : 1.0rc")
    print("  # Description     : Versatile moderation bot utilising modern Pythonic Discord API (PyPi v1.7.2)")
    print("  # Dependencies    : Python 3.5.3 or higher,")
    print("                      Python libraries including discord, PyNaCl (Voice Support)")
    print("                      discord.ext, youtube_dl, googlesearch, beautifulsoup4")
    print("                      urllib.parse, urllib.request, re, threading")
    print("  # Author          : github.com/ivorytone")
    print("  # Email           : jay.dnb@protonmail.ch")
    print()
    print("=============================================================================")

@charity.event
async def on_ready():
    print(f"\b\b\b\b\b\b\b\b\b\b\b\b\bLogged in as {charity.user} PFID: {charity.user.id}")
    time.sleep(1)
    print("-----------------------------------------------------------------------------")

def cog_embed(ctx, title = "", description = "This is message description.", colour = 0xf71e4b):
    edict = {
        "color" : colour,
        "author" : {
            "name" : "Charity#2894",
            "icon_url" : "https://cdn.discordapp.com/attachments/841538439606304818/844773173895364608/mSE4lwS.gif",
        },
        "title" : title,
        "description" : description,
        "footer" : {
            "text" : f"{ctx.guild.name}",
            "icon_url" : f"{ctx.guild.icon_url}"
        },
        "timestamp" : datetime.datetime.utcnow().isoformat()
    }
    embed = discord.Embed.from_dict(edict)
    return embed

@charity.event
async def on_member_join(member):
    await charity.get_channel(830511014302842950).send(f"Welcome to **{member.guild}**, {member.mention} :innocent: Have a great time!")

#------------------------------------------------------------------------------------------------------------------- # Module poll
@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def poll(ctx):
    poll = {}
    def check(m):
        return m.channel == ctx.channel and ctx.author == m.author

    continue_loop = True
    wizard = await ctx.channel.send("Poll wizard invoked. Type `.cancel` to end the wizard. This will lead to loss of unsaved information. Choose your type of poll:\n`1. Anonymous`\n`2. Non-anonymous`")
    while continue_loop:
        reply = await charity.wait_for("message", check = check, timeout = 120)
        if reply.content == ".cancel":
            raise Exception("Poll wizard revoked.")
        elif reply.content == "1":
            poll["type"] = "anonymous"
            poll["epoch_t"] = time.time()
            continue_loop = False
            await reply.add_reaction('☑️')
        elif reply.content == "2":
            poll["type"] = "non-anonymous"
            poll["epoch_t"] = time.time()
            continue_loop = False
            await reply.add_reaction('☑️')
        else:
            await ctx.channel.send("Invalid input. Try again.", delete_after = 3)
        await reply.delete(delay = 3)

    continue_loop = True
    await wizard.edit(content = "Enter the poll title [question] below.")
    while continue_loop:
        reply = await charity.wait_for("message", check = check, timeout = 120)
        if reply.content == ".cancel":
            raise Exception("Poll wizard revoked.")
        else:
            poll["title"] = reply.content
            continue_loop = False
            await reply.add_reaction('☑️')
        await reply.delete(delay = 3)

    continue_loop = True
    await wizard.edit(content = "Enter the number of choices. Upto 15 choices supported.")
    while continue_loop:
        reply = await charity.wait_for("message", check = check, timeout = 120)
        if reply.content == ".cancel":
            raise Exception("Poll wizard revoked.")
        try:
            integer = int(reply.content)
        except TypeError:
            await ctx.channel.send("Invalid input. Try again.", delete_after = 3)
            continue
        if integer > 15:
            await ctx.channel.send("Invalid input. Try again.", delete_after = 3)
        else:
            poll["no_of_choices"] = integer
            continue_loop = False
            await reply.add_reaction('☑️')
        await reply.delete(delay = 3)

    choice_counter = 1
    choice_list = []
    while choice_counter != poll["no_of_choices"] + 1:
        await wizard.edit(content = f"Enter choice #{choice_counter} text.")
        reply = await charity.wait_for("message", check = check, timeout = 120)
        if reply.content == ".cancel":
            raise Exception("Poll wizard revoked.")
        elif len(reply.content) > 350:
            await ctx.channel.send("The length of the option's string cannot exceed 350 characters. Try again.", delete_after = 3)
        else:
            choice_list.append(reply.content)
            await reply.add_reaction('☑️')
            choice_counter += 1
        await reply.delete(delay = 3)

    continue_loop = True
    choice_counter = 1
    choices_dict = {}
    choice_emotes_def = [
        "🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴"
    ]
    await wizard.edit(content = "Type `.default` to let me assign the default reacts against the requested options, or type `.custom` to continue to the next step of assigning custom reacts.")
    while continue_loop:
        reply = await charity.wait_for("message", check = check, timeout = 120)
        if reply.content == ".cancel":
            raise Exception("Poll wizard revoked.")
        elif reply.content == ".default":
            for i in range(poll["no_of_choices"]):
                choices_dict[choice_emotes_def[i]] = choice_list[i]
                await reply.add_reaction('☑️')
                continue_loop = False
        elif reply.content == ".custom":
            pass # to be continued
        else:
            await ctx.channel.send("Invalid input. Try again.", delete_after = 3)
        await reply.delete(delay = 3)

    poll["choices"] = choices_dict
    print (poll)
    """ continue_loop = False
    while continue_loop:
        await wizard.edit(content = f"React the emote ") """
        
#------------------------------------------------------------------------------------------------------------------- # Module logout
@charity.command()
async def logout(ctx):
    if ctx.author.id == 799186130654199809:
        await ctx.channel.send("Logging out...")
        exit()
#------------------------------------------------------------------------------------------------------------------- # Module clr [messages]
@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def clr(ctx, limit, arg = None):
    limit = int(limit)
    counter = 0
    if limit > 200:
        raise Exception("Limit cannot exceed `200` messages.")
    if arg == None:
        await ctx.channel.trigger_typing()
        counter = await ctx.channel.purge(limit = limit + 1)
        counter = len(counter)
    elif arg == "--ignore-pins":
        await ctx.channel.trigger_typing()
        async for x in ctx.channel.history(limit = limit + 1):
            if x.pinned == False:
                await x.delete()
                counter += 1
    else:
        raise Exception("Invalid argument received.")
    await ctx.channel.send(f"`{counter} messages purged.` :ballot_box_with_check:", delete_after = 7)
    
@clr.error
async def clr_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#------------------------------------------------------------------------------------------------------------------- # Module spam warn
# under active observation, no threat
undr_surveillance_lvl_0 = []
undr_surveillance_lvl_1 = []
undr_surveillance_lvl_2 = []
undr_surveillance_lvl_3 = []

# under surveillance after the reported infraction
warned_for_spam_lvl_1 = {} # next step: warning 2
warned_for_spam_lvl_2 = {} # next step: warning 3
warned_for_spam_lvl_3 = {} # next step: mute

# invoke if
SPAM_WARN_MCOUNT = 6
# within a span of
SPAM_WARN_TIMEOUT = 10
LEVEL_0_TIMEOUT = 0
LEVEL_1_TIMEOUT = 2
LEVEL_2_TIMEOUT = 5
LEVEL_3_TIMEOUT = 10

@tasks.loop(seconds = 30)
async def updt_spam_record():
    global warned_for_spam_lvl_1
    global warned_for_spam_lvl_2
    global warned_for_spam_lvl_3
    tbpopped = []
    # ---
    x = warned_for_spam_lvl_1
    for key, value in x:
        if time.time() - value >= LEVEL_1_TIMEOUT*60:
            tbpopped.append(key)
    for item in tbpopped:
        x.pop(item)
    warned_for_spam_lvl_1 = x
    # ---
    x = warned_for_spam_lvl_2
    for key, value in x:
        if time.time() - value >= LEVEL_2_TIMEOUT*60:
            tbpopped.append(key)
    for item in tbpopped:
        x.pop(item)
    warned_for_spam_lvl_2 = x
    # ---
    x = warned_for_spam_lvl_3
    for key, value in x:
        if time.time() - value >= LEVEL_3_TIMEOUT*60:
            tbpopped.append(key)
    for item in tbpopped:
        x.pop(item)
    warned_for_spam_lvl_3 = x

@updt_spam_record.before_loop
async def before_my_task():
    await charity.wait_until_ready()

@charity.listen("on_message")
async def invoke_spam_purge_lvl_0(m):
    if m.author == charity.user or m.channel.id == 830641426466996235 or m.channel.id == 833987331018981386:
        return
    if m.author.id in undr_surveillance_lvl_0 or m.author.id in warned_for_spam_lvl_1 or m.author.id in warned_for_spam_lvl_2 or m.author.id in warned_for_spam_lvl_3:
        return
    undr_surveillance_lvl_0.append(m.author.id)
    c = 0
    def check(thread):
        return m.author == thread.author and m.channel == thread.channel
    time_since_epoch = time.time()
    while True:
        try:
            await charity.wait_for("message", check = check, timeout = SPAM_WARN_TIMEOUT)
        except asyncio.TimeoutError:
            undr_surveillance_lvl_0.remove(m.author.id)
            break
        c += 1
        if c > (SPAM_WARN_MCOUNT - 1):
            await m.channel.send("<@{}> Woah Woah, slow down there...".format(m.author.id, c))
            undr_surveillance_lvl_0.remove(m.author.id)
            warned_for_spam_lvl_1[m.author.id] = time.time()
            break
        if time.time() - time_since_epoch >= SPAM_WARN_TIMEOUT:
            undr_surveillance_lvl_0.remove(m.author.id)
            break

@charity.listen("on_message")
async def invoke_spam_purge_lvl_1(m):
    if m.author == charity.user or m.channel.id == 830641426466996235 or m.channel.id == 833987331018981386:
        return
    if m.author.id not in warned_for_spam_lvl_1.keys():
        return
    if m.author.id in undr_surveillance_lvl_1:
        return
    undr_surveillance_lvl_1.append(m.author.id)
    def check(thread):
        return m.author == thread.author and m.channel == thread.channel
    c = 0
    time_since_epoch = time.time()
    while True:
        try:
            await charity.wait_for("message", check = check, timeout = SPAM_WARN_TIMEOUT)
        except asyncio.TimeoutError:
            undr_surveillance_lvl_1.remove(m.author.id)
            break
        c += 1
        if c > (SPAM_WARN_MCOUNT - 1):
            await m.channel.send("<@{}> This is your second warning. Do not spam, or you will be muted.".format(m.author.id))
            undr_surveillance_lvl_1.remove(m.author.id)
            warned_for_spam_lvl_1.pop(m.author.id)
            warned_for_spam_lvl_2[m.author.id] = time.time()
            break
        if time.time() - time_since_epoch >= SPAM_WARN_TIMEOUT:
            undr_surveillance_lvl_1.remove(m.author.id)
            break

@charity.listen("on_message")
async def invoke_spam_purge_lvl_2(m):
    if m.author == charity.user or m.channel.id == 830641426466996235 or m.channel.id == 833987331018981386:
        return
    if m.author.id not in warned_for_spam_lvl_2.keys():
        return
    if m.author.id in undr_surveillance_lvl_2:
        return
    undr_surveillance_lvl_2.append(m.author.id)
    def check(thread):
        return m.author == thread.author and m.channel == thread.channel
    c = 0
    time_since_epoch = time.time()
    while True:
        try:
            await charity.wait_for("message", check = check, timeout = SPAM_WARN_TIMEOUT)
        except asyncio.TimeoutError:
            undr_surveillance_lvl_2.remove(m.author.id)
            break
        c += 1
        if c > (SPAM_WARN_MCOUNT - 1):
            await m.channel.send("<@{}> This is your final warning. DO NOT SPAM or you will be muted.".format(m.author.id))
            undr_surveillance_lvl_2.remove(m.author.id)
            warned_for_spam_lvl_2.pop(m.author.id)
            warned_for_spam_lvl_3[m.author.id] = time.time()
            break
        if time.time() - time_since_epoch >= SPAM_WARN_TIMEOUT:
            undr_surveillance_lvl_2.remove(m.author.id)
            break

@charity.listen("on_message")
async def invoke_spam_purge_lvl_3(m):
    if m.author == charity.user or m.channel.id == 830641426466996235 or m.channel.id == 833987331018981386:
        return
    if m.author.id not in warned_for_spam_lvl_3.keys():
        return
    if m.author.id in undr_surveillance_lvl_3:
        return
    undr_surveillance_lvl_3.append(m.author.id)
    def check(thread):
        return m.author == thread.author and m.channel == thread.channel
    c = 0
    time_since_epoch = time.time()
    while True:
        try:
            await charity.wait_for("message", check = check, timeout = SPAM_WARN_TIMEOUT)
        except asyncio.TimeoutError:
            undr_surveillance_lvl_3.remove(m.author.id)
            break
        c += 1
        if c > (SPAM_WARN_MCOUNT - 1):
            await m.channel.send("<@{}> Ad majórem Dei glóriam, muted for 60 minutes. :slight_smile:".format(m.author.id))
            undr_surveillance_lvl_3.remove(m.author.id)
            warned_for_spam_lvl_3.pop(m.author.id)
            user = charity.get_member(m.author.id)
            await user.member("You have been **muted** for **{} minutes**.\n**INFRACTION:** {}".format(60, "Spamming in public chat."))
            embed_var = discord.Embed(title = "**:mute: Mute**", colour = 0xda0000, description = "**Muted** {} _(ID: {})_\n**Reason:** {}\n".format(user, user.id, "Spamming in public chat."))
            embed_var.set_author(name = charity.user, icon_url = charity.user.avatar_url)
            embed_var.set_footer(text = "Solaris DS Administration", icon_url = "https://cdn.discordapp.com/attachments/830787117118521375/836352545965211700/Untitled.png")
            embed_var.set_thumbnail(url = user.avatar_url)
            mute_dump = charity.get_channel(840669966621212732)
            ref_msg = await mute_dump.send(embed = embed_var)
            muted_role = m.guild.get_role(831609804254085200)
            member = m.guild.get_member(m.author.id)
            await member.add_roles(muted_role)
            await asyncio.sleep(60 * 60)
            await member.remove_roles(muted_role)
            embed_var = discord.Embed(title = "**:speaker: Unmute**", colour = 0x67aa30, description = "**Unmuted** {} _(ID: {})_\n**Reason:** [Mute duration expired.]({})\n".format(user, user.id, ref_msg.jump_url))
            embed_var.set_author(name = charity.user, icon_url = charity.user.avatar_url)
            embed_var.set_footer(text = "Solaris DS Administration", icon_url = "https://cdn.discordapp.com/attachments/830787117118521375/836352545965211700/Untitled.png")
            embed_var.set_thumbnail(url = user.avatar_url)
            await mute_dump.send(embed = embed_var)
            await user.send("You have been unmuted.\n**REASON:** Mute duration expired.")
            break
        if time.time() - time_since_epoch >= SPAM_WARN_TIMEOUT:
            undr_surveillance_lvl_3.remove(m.author.id)
            break
#------------------------------------------------------------------------------------------------------------------- # Module afk
afk_dump = {}
@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def afk(ctx, *, afkstring):
    if "<@" in afkstring:
            await ctx.reply("You cannot tag guild members in your AFK note.")
            return
    await ctx.message.add_reaction("🌙")
    await asyncio.sleep(5)
    afk_dump[ctx.message.author.id] = afkstring

@afk.error
async def afk_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)

@charity.listen("on_message")
async def ifpingonafk(message):
    if  message.author == charity.user:
        return
    if len(afk_dump.keys()) == 0 or "<@" not in message.content:
        return
    afk_dump_key_state = afk_dump.keys()
    notif_msg_array = []
    for x in afk_dump_key_state:
        if "<@{}>".format(str(x)) in message.content:
            msg = await message.channel.send("`{} is AFK:` _{}_".format(charity.get_user(x).name, afk_dump.get(x)))
            notif_msg_array.append(msg)
    await asyncio.sleep(5)
    for y in notif_msg_array:
        await y.delete()

@charity.listen("on_message")
async def removeafk(message):
    if len(afk_dump.keys()) == 0:
        return
    to_be_popped_dump = []
    for x in afk_dump.keys():
        if message.author.id == x:
            await message.channel.send("<@{}> `Welcome back, removed your AFK` ☑️".format(message.author.id), delete_after = 5)
            to_be_popped_dump.append(message.author.id)
    for y in to_be_popped_dump:
        afk_dump.pop(y)
#------------------------------------------------------------------------------------------------------------------- # Module web
@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def web(ctx, *, searchstring):
    await ctx.channel.trigger_typing()
    results = search(searchstring, safe='on', tld="com", num=1, stop=1, pause=0.5)
    for j in results:
        await ctx.channel.send(":card_box: `TOP RESULT FROM google, tld:com` {}".format(j))

@web.error
async def web_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#------------------------------------------------------------------------------------------------------------------- # Module youtube
@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def yt(ctx, *, search):
    query_string = urllib.parse.urlencode({'search_query': search})
    htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
    await ctx.reply('`TOP RESULT:` http://www.youtube.com/watch?v=' + search_results[0])

@yt.error
async def yt_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#------------------------------------------------------------------------------------------------------------------- # Module announce
@charity.command()
async def schedule(ctx, tcid, countd, *, msg):
    dump_channel = charity.get_channel(int(tcid))
    await ctx.message.add_reaction("☑️")
    await asyncio.sleep(60 * int(countd))
    await dump_channel.send(msg)

@schedule.error
async def schedule_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#------------------------------------------------------------------------------------------------------------------- # Module unban user
@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def unban(ctx, pfid, *, reason):
    member = ctx.guild.get_member(int(pfid))
    embed_var = discord.Embed(title = "**:cake: Unban**", colour = 0x67aa30, description = "**Unbanned** {} _(ID: {})_\n**Reason:** {}\n".format(member, member.id, reason))
    embed_var.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    embed_var.set_footer(text = "Solaris DS Administration", icon_url = "https://cdn.discordapp.com/attachments/830787117118521375/836352545965211700/Untitled.png")
    embed_var.set_thumbnail(url = member.avatar_url)
    await ctx.guild.unban(member, reason)
    await charity.get_channel(840669966621212732).send(embed = embed_var)
    await member.send("You have been unbanned in Solaris.\n**REASON:** {}".format(reason))
    await ctx.message.add_reaction("☑️")

@unban.error
async def ban_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#------------------------------------------------------------------------------------------------------------------- # Module ban user
@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def ban(ctx, pfid, del_msg_history: int, *, reason):
    member = ctx.guild.get_member(int(pfid))
    embed_var = discord.Embed(title = "**:hammer: Ban**", colour = 0x67aa30, description = "**Banned** {} _(ID: {})_\n**Reason:** {}\n".format(member, member.id, reason))
    embed_var.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    embed_var.set_footer(text = "Solaris DS Administration", icon_url = "https://cdn.discordapp.com/attachments/830787117118521375/836352545965211700/Untitled.png")
    embed_var.set_thumbnail(url = member.avatar_url)
    await charity.get_channel(840669966621212732).send(embed = embed_var)
    await member.send("You have been banned from Solaris.\n**REASON:** {}".format(reason))
    await ctx.guild.ban(user = member, reason = reason, delete_message_days = del_msg_history)
    await ctx.message.add_reaction("☑️")

@ban.error
async def ban_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#------------------------------------------------------------------------------------------------------------------- # Module kick user
@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def kick(ctx, pfid, *, reason):
    user = ctx.guild.get_member(int(pfid))
    embed_var = discord.Embed(title = "**:athletic_shoe: Kick**", colour = 0x67aa30, description = "**Kicked** {} _(ID: {})_\n**Reason:** {}\n".format(user, user.id, reason))
    embed_var.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    embed_var.set_footer(text = "Solaris DS Administration", icon_url = "https://cdn.discordapp.com/attachments/830787117118521375/836352545965211700/Untitled.png")
    embed_var.set_thumbnail(url = user.avatar_url)
    await charity.get_channel(840669966621212732).send(embed = embed_var)
    await user.send("You have been kicked from Solaris.\n**REASON:** {}".format(reason))
    await ctx.guild.kick(user = user, reason = reason)
    await ctx.message.add_reaction("☑️")

@kick.error
async def kick_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#------------------------------------------------------------------------------------------------------------------- # Module Unmute user
@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def unmute(ctx, pfid, *, message_arg: str):
    user = ctx.guild.get_member(int(pfid))
    if "Muted" not in user.roles:
        await ctx.reply("`The user is not muted.`")
        return
    await user.send("You have been **unmuted**.\n**REASON:** {}".format(message_arg))
    await ctx.message.add_reaction("☑️")
    embed_var = discord.Embed(title = "**:speaker: Unmute**", colour = 0x67aa30, description = "**Unmuted** {} _(ID: {})_\n**Reason:** {}\n".format(user, user.id, message_arg))
    embed_var.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    embed_var.set_footer(text = "Solaris DS Administration", icon_url = "https://cdn.discordapp.com/attachments/830787117118521375/836352545965211700/Untitled.png")
    embed_var.set_thumbnail(url = user.avatar_url)
    await charity.get_channel(840669966621212732).send(embed = embed_var)
    await user.send("You have been unmuted.\n**REASON:** {}".format(message_arg))

@unmute.error
async def unmute_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#------------------------------------------------------------------------------------------------------------------- # Module Mute user
@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def mute(ctx, pfid, duration, *, message_arg: str):
    user = ctx.guild.get_member(int(pfid))
    await user.send("You have been **muted** by a moderator for **{} minutes**.\n**INFRACTION:** {}".format(duration, message_arg))
    embed_var = discord.Embed(title = "**:mute: Mute**", colour = 0xda0000, description = "**Muted** {} _(ID: {})_\n**Reason:** {}\n".format(user, user.id, message_arg))
    embed_var.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    embed_var.set_footer(text = "Solaris DS Administration", icon_url = "https://cdn.discordapp.com/attachments/830787117118521375/836352545965211700/Untitled.png")
    embed_var.set_thumbnail(url = user.avatar_url)
    mute_dump = charity.get_channel(840669966621212732)
    ref_msg = await mute_dump.send(embed = embed_var)
    muted_role = ctx.guild.get_role(831609804254085200)
    member = ctx.guild.get_member(int(pfid))
    await member.add_roles(muted_role)
    await ctx.message.add_reaction("☑️")
    await asyncio.sleep(60 * int(duration))
    await member.remove_roles(muted_role)
    embed_var = discord.Embed(title = "**:speaker: Unmute**", colour = 0x67aa30, description = "**Unmuted** {} _(ID: {})_\n**Reason:** [Mute duration expired.]({})\n".format(user, user.id, ref_msg.jump_url))
    embed_var.set_author(name = charity.user, icon_url = charity.user.avatar_url)
    embed_var.set_footer(text = "Solaris DS Administration", icon_url = "https://cdn.discordapp.com/attachments/830787117118521375/836352545965211700/Untitled.png")
    embed_var.set_thumbnail(url = user.avatar_url)
    await mute_dump.send(embed = embed_var)
    await user.send("You have been unmuted.\n**REASON:** Mute duration expired.")

@mute.error
async def mute_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#------------------------------------------------------------------------------------------------------------------- # Module Warn user
@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def warn(ctx, pfid, *, message_arg: str):
    user = charity.get_user(int(pfid))
    await user.send("You have been **warned** by a moderator.\n**INFRACTION:** {}".format(message_arg))
    await ctx.message.add_reaction("☑️")
    embed_var = discord.Embed(title = "**:warning: Warning**", colour = 0xff6700, description = "**Warned** {} _(ID: {})_\n**Reason:** {}\n".format(user, user.id, message_arg))
    embed_var.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    embed_var.set_footer(text = "Solaris DS Administration", icon_url = "https://cdn.discordapp.com/attachments/830787117118521375/836352545965211700/Untitled.png")
    embed_var.set_thumbnail(url = user.avatar_url)
    warn_dump = charity.get_channel(840669966621212732)
    await warn_dump.send(embed = embed_var)

@warn.error
async def warn_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#------------------------------------------------------------------------------------------------------------------- # Module msg
@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def msg(
        ctx,
        dump: typing.Union[discord.Member, discord.TextChannel],
        *, args):
    msg = "" # --msg-content
    title = ""  # --title
    description = ""  # --description
    embed = {}
    for x in args.split(sep = " "):
        if x == "--rich-embed":
            keys = re.findall(r'[-][-][^r].*?[=]', args, re.IGNORECASE)
            values = re.findall(r'["][^-].*?["]', args, re.IGNORECASE)
            for i in range(len(keys)):
                if re.search("msg-content", keys[i], re.IGNORECASE): msg = values[i][1:-1]
                elif re.search("title", keys[i], re.IGNORECASE): title = values[i][1:-1]
                elif re.search("description", keys[i], re.IGNORECASE): description = values[i][1:-1]
            kwargs = {
                "ctx" : ctx,
                "title" : title,
                "description" : description,
            }
            embed = cog_embed(**kwargs)
            await dump.send(content = msg, embed = embed)
            await ctx.message.add_reaction("☑️")
            return
        elif x == "--raw-embed":
            key = re.findall(r'[-][-][^r].*?[=]', args, re.IGNORECASE)
            value = re.findall(r'["][^-].*?["]', args, re.IGNORECASE)
            try:
                if re.search("description", key[0], re.IGNORECASE): description = value[0][1:-1]
                else: raise Exception("Invalid argument(s) or value(s) provided.")
            except:
                raise Exception("Invalid argument(s) or value(s) provided.")
            edict = {
                "color" : 0xf71e4b,
                "description" : description,
            }
            embed = discord.Embed.from_dict(edict)
            await dump.send(embed = embed)
            await ctx.message.add_reaction("☑️")
            return
    await dump.send(content = args)
    await ctx.message.add_reaction("☑️")

@msg.error
async def msg_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#------------------------------------------------------------------------------------------------------------------- # Module Modmail
@charity.listen("on_message")
async def on_dmessage(message):
    if not message.guild and message.author.id != charity.user.id:
        await message.add_reaction("☑️")
        dm_dump_channel = charity.get_channel(840645965949829140)
        await dm_dump_channel.send("**DIRECT MESSAGE FROM <@{}> PFID:** `{}`**:**\n**CONTENT:** {}".format(message.author.id, message.author.id, message.content))
#------------------------------------------------------------------------------------------------------------------- # Module hello
@charity.command(name = "hello")
async def say_hello(ctx, arg):
    if ctx.author.id == 805108723387334657:
        await ctx.reply("Hello Momma! Stay safe. <:heartz:844352117674082305>")
    elif ctx.author.id == 799186130654199809:
        await ctx.reply("Hey Dad! <:heartz:844352117674082305>")
    elif arg.lower() == "charity":
        await ctx.reply("Hello {}! <:orange:841124452283580417>".format(ctx.author.name))

@say_hello.error
async def say_hello_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#------------------------------------------------------------------------------------------------------------------- # Module cc (custom commands)
@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, "Beta tester")
async def emsg(ctx, dump_txtchannel, msg, title, description, enable_footer):
    await cog_embed(ctx = ctx, dump_txtchannel = int(dump_txtchannel), msg = msg, title = title, description = description, enable_footer = bool(enable_footer))

@emsg.error
async def emsg_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#-------------------------------------------------------------------------------------------------------------------

# ===================== MUSIC.PY ======================
youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return filename

@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def join(ctx):
    """Joins a voice channel"""
    channel = ctx.author.voice.channel
    await channel.connect()

@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def play(ctx, *, search):
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            if search[0:31] == "http://www.youtube.com/watch?v=" or search[0:32] == "https://www.youtube.com/watch?v=":
                url = search
            else:
                query_string = urllib.parse.urlencode({'search_query': search})
                htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
                search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
                await ctx.send('`PLAYING TOP RESULT:` http://www.youtube.com/watch?v=' + search_results[0])
                url = 'http://www.youtube.com/watch?v=' + search_results[0]
            filename = await YTDLSource.from_url(url, loop=charity.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename))
        await ctx.send('**Now playing :)**')
    except:
        await ctx.send("**An error occurred :(**")

@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def stop(ctx):
    await ctx.voice_client.disconnect()

@play.before_invoke
async def ensure_voice(ctx):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()
# ===================== MUSIC.PY ======================

startup()
charity.run(client_token.CHARITY_TOKEN)
logger()