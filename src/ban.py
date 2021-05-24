import discord
from discord.ext import commands
from startup import *

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
