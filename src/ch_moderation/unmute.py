import discord
from discord.ext import commands
from ch_boot.startup import *

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
