import discord
from discord.ext import commands
from startup import *

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
