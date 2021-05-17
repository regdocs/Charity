import token
import discord
from discord.ext import commands, tasks
import urllib.parse, urllib.request, re
from googlesearch import search
import youtube_dl
import asyncio
import logging
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
    print("  # Description     : Versatile moderation bot utilising modern Pythonic Discord API (pypi v1.7.2)")
    print("  # Dependencies    : Python 3.5.3 or higher,")
    print("                      Python libraries including discord, PyNaCl (Voice Support)")
    print("                      discord.ext, youtube_dl, googlesearch, beautifulsoup4")
    print("                      urllib.parse, urllib.request, re, threading")
    print("  # Author          : github.com/ivorytone")
    print("  # Email           : jay.dnb@protonmail.ch")
    print()
    print("=============================================================================")
    for i in range(3):    
        for j in range(3):
            if j == 0:
                print("Logging in.  ", end='', flush=True)
                time.sleep(0.5)
                print("\b\b\b\b\b\b\b\b\b\b\b\b\b", end='', flush=True)
            elif j == 1:
                print("Logging in.. ", end='', flush=True)
                time.sleep(0.5)
                print("\b\b\b\b\b\b\b\b\b\b\b\b\b", end='', flush=True)
            elif j == 2:
                print("Logging in...", end='', flush=True)
                time.sleep(0.5)
                print("\b\b\b\b\b\b\b\b\b\b\b\b\b", end='', flush=True)


@charity.event
async def on_ready():
    print(f"\b\b\b\b\b\b\b\b\b\b\b\b\bLogged in as {charity.user} PFID: {charity.user.id}")
    time.sleep(1)
    print("-----------------------------------------------------------------------------\nLog:")

#----------------------------------------------- # Module logout
@charity.command()
async def logout(ctx):
    if ctx.author.id == 799186130654199809:
        await ctx.channel.send("Logging out...")
        exit()
#----------------------------------------------- # Module spam warn
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
SPAM_WARN_MCOUNT = 5
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
            user = charity.get_user(m.author.id)
            await user.send("You have been **muted** for **{} minutes**.\n**INFRACTION:** {}".format(60, "Spamming in public chat."))
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
#----------------------------------------------- # Module afk
afk_dump = {}
@charity.command()
@commands.has_any_role(840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
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
            await message.channel.send("<@{}> `Welcome back, removed your AFK` ✅".format(message.author.id), delete_after = 5)
            to_be_popped_dump.append(message.author.id)
    for y in to_be_popped_dump:
        afk_dump.pop(y)
#----------------------------------------------- # Module web
@charity.command()
@commands.has_any_role(840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def web(ctx, *, searchstring):
    await ctx.channel.trigger_typing()
    results = search(searchstring, safe='on', tld="com", num=1, stop=1, pause=0.5)
    for j in results:
        await ctx.channel.send(":card_box: `TOP RESULT FROM google, tld:com` {}".format(j))

@web.error
async def web_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#----------------------------------------------- # Module youtube
@charity.command()
@commands.has_any_role(840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def yt(ctx, *, search):
    query_string = urllib.parse.urlencode({'search_query': search})
    htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
    await ctx.reply('`TOP RESULT:` http://www.youtube.com/watch?v=' + search_results[0])

@yt.error
async def yt_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#----------------------------------------------- # Module announce
@charity.command()
async def schedule(ctx, tcid, countd, *, msg):
    dump_channel = charity.get_channel(int(tcid))
    await ctx.message.add_reaction("✅")
    await asyncio.sleep(60 * int(countd))
    await dump_channel.send(msg)

@schedule.error
async def schedule_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#----------------------------------------------- # Module ban user
@charity.command()
@commands.has_any_role(840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def ban(ctx, pfid, del_msg_history: int, *, reason):
    member = ctx.guild.get_member(int(pfid))
    embed_var = discord.Embed(title = "**:hammer: Ban**", colour = 0x67aa30, description = "**Banned** {} _(ID: {})_\n**Reason:** {}\n".format(member, member.id, reason))
    embed_var.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    embed_var.set_footer(text = "Solaris DS Administration", icon_url = "https://cdn.discordapp.com/attachments/830787117118521375/836352545965211700/Untitled.png")
    embed_var.set_thumbnail(url = member.avatar_url)
    await charity.get_channel(840669966621212732).send(embed = embed_var)
    await member.send("You have been banned from Solaris Server.\n**REASON:** {}".format(reason))
    await ctx.guild.ban(user = member, reason = reason, delete_message_days = del_msg_history)
    await ctx.message.add_reaction("✅")

@ban.error
async def ban_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#----------------------------------------------- # Module kick user
@charity.command()
@commands.has_any_role(840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def kick(ctx, pfid, *, reason):
    user = ctx.guild.get_member(int(pfid))
    embed_var = discord.Embed(title = "**:athletic_shoe: Kick**", colour = 0x67aa30, description = "**Kicked** {} _(ID: {})_\n**Reason:** {}\n".format(user, user.id, reason))
    embed_var.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    embed_var.set_footer(text = "Solaris DS Administration", icon_url = "https://cdn.discordapp.com/attachments/830787117118521375/836352545965211700/Untitled.png")
    embed_var.set_thumbnail(url = user.avatar_url)
    await charity.get_channel(840669966621212732).send(embed = embed_var)
    await user.send("You have been kicked from Solaris Server.\n**REASON:** {}".format(reason))
    await ctx.guild.kick(user = user, reason = reason)
    await ctx.message.add_reaction("✅")

@kick.error
async def kick_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#----------------------------------------------- # Module Unmute user
@charity.command()
@commands.has_any_role(840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def unmute(ctx, pfid, *, message_arg: str):
    user = ctx.guild.get_member(int(pfid))
    if "Muted" not in user.roles:
        await ctx.reply("`The user is not muted.`")
        return
    await user.send("You have been **unmuted**.\n**REASON:** {}".format(message_arg))
    await ctx.message.add_reaction("✅")
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
#----------------------------------------------- # Module Mute user
@charity.command()
@commands.has_any_role(840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def mute(ctx, pfid, duration, *, message_arg: str):
    user = charity.get_user(int(pfid))
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
    await ctx.message.add_reaction("✅")
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
#----------------------------------------------- # Module Warn user
@charity.command()
@commands.has_any_role(840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def warn(ctx, pfid, *, message_arg: str):
    user = charity.get_user(int(pfid))
    await user.send("You have been **warned** by a moderator.\n**INFRACTION:** {}".format(message_arg))
    await ctx.message.add_reaction("✅")
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
#----------------------------------------------- # Module DM user
@charity.command()
@commands.has_any_role(840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def dmsg(ctx, pfid, *, message_arg: str):
    user = charity.get_user(int(pfid))
    await user.send(message_arg)
    await ctx.message.add_reaction("✅")

@dmsg.error
async def dmsg_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#----------------------------------------------- # Module cmsgthread
@charity.command()
@commands.has_any_role(840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def cmsgthread(ctx, channel_id):
    xmsg = "**INFO**: Auto-message thread invoked. All messages sent by you next will be dumped into the channel <#" + channel_id +">. Reply with `.haltcmsgthread` to end the thread."
    await ctx.reply(xmsg)
    def check(m):
        return m.author == ctx.author
    cmsgflag = 1
    msg = 0
    while (cmsgflag == 1):
        try:
            msg = await charity.wait_for("message", check=check, timeout = 300)
        except asyncio.TimeoutError:
            await ctx.send("**INFO:** `asyncio.TimeoutError` encountered after `300 seconds`. Closing thread...")
            cmsgflag = 0
        if msg.content == ".haltcmsgthread":
            cmsgflag = 0
            await ctx.send("**INFO:** Thread terminated by <@{}>.".format(ctx.author.id))
        else:
            target = charity.get_channel(int(channel_id))
            await target.send(msg.content)

@cmsgthread.error
async def cmsgthread_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#----------------------------------------------- # Module cmsg
@charity.command()
@commands.has_any_role(840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def cmsg(ctx, channel_id, *, msg):
    target = charity.get_channel(int(channel_id))
    await target.send(msg)
    await ctx.message.add_reaction("✅")

@cmsgthread.error
async def cmsg_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#----------------------------------------------- # Module Modmail
@charity.listen("on_message")
async def on_dmessage(message):
    if not message.guild and message.author.id != charity.user.id:
        await message.add_reaction("✅")
        dm_dump_channel = charity.get_channel(840645965949829140)
        await dm_dump_channel.send("**DIRECT MESSAGE FROM <@{}> PFID:** `{}`**:**\n**CONTENT:** {}".format(message.author.id, message.author.id, message.content))
#----------------------------------------------- # Module hello
@charity.command(name = "hello")
async def say_hello(ctx, arg):
    if arg.lower() == "charity":
        await ctx.reply("Hello {}! <:mari_smile:840561703157628938>".format(ctx.author.name))

@say_hello.error
async def say_hello_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#----------------------------------------------- # Module cc (custom commands)
@charity.command()
@commands.has_any_role(840545860101210122, 830486598050119740, 843198710782361682)
async def cc(ctx):
    embed_var = discord.Embed(title = "Title", colour = 0xff6700, description = "Description")
    embed_var.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    embed_var.set_footer(text = "Solaris Discord Server", icon_url = "https://cdn.discordapp.com/attachments/830787117118521375/836352545965211700/Untitled.png")
    await ctx.reply(embed = embed_var)

@cc.error
async def cc_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
#-----------------------------------------------

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
@commands.has_any_role(840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def join(ctx):
    """Joins a voice channel"""
    channel = ctx.author.voice.channel
    await channel.connect()

@charity.command()
@commands.has_any_role(840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
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
@commands.has_any_role(840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
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
charity.run(token.CHARITY_TOKEN)
logger()
