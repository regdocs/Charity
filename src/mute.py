import discord
from discord.ext import commands
from startup import *

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
