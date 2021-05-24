import discord
import datetime

def cog_embed(ctx = None, title = "", description = "", colour = 0xf71e4b):
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
