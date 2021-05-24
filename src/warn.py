import discord
from discord.ext import commands
from startup import *

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
