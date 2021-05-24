import discord
from discord.ext import commands, tasks
import datetime
from startup import *
import time
import asyncio

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
