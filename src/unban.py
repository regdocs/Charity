import discord
from discord.ext import commands
from startup import *

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
