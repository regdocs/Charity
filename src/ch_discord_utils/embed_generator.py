import discord
import datetime

def create_embed(
    author_name = "Charity#2894",
    author_url = "",
    author_icon_url = "https://cdn.discordapp.com/attachments/841538439606304818/844773173895364608/mSE4lwS.gif",
    title = "",
    title_url = "",
    thumbnail_url = "",
    description = "",
    image_url = "",
    footer_text = "",
    footer_icon_url = "",
    timestamp = datetime.datetime.utcnow().isoformat(),
    colour = 0xf71e4b
    ):
    edict = {
        "color" : colour,
        "author" : {
            "name" : author_name,
            "url" : author_url,
            "icon_url" : author_icon_url,
        },
        "title" : title,
        "url" : title_url,
        "thumbnail" : {
            "url" : thumbnail_url
        },
        "description" : description,
        "image" : {
            "url" : image_url
        },
        "footer" : {
            "text" : footer_text,
            "icon_url" : footer_icon_url
        },
        "timestamp" : timestamp
    }
    embed = discord.Embed.from_dict(edict)
    return embed

def meta_message(
    colour = 0xf71e4b,
    description = "",
    image_url = ""
    ):
    edict  = {
        "colour" : colour,
        "description" : description,
        "image" : {
            "url" : image_url
        }
    }
    embed = discord.Embed.from_dict(edict)
    return embed