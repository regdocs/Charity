import re
import discord
from discord.ext import commands
import datetime
from startup import *

@charity.listen("on_message")
async def vent_out(message):
    if message.channel.id != 846057832712765490 or message.author == charity.user:
        return
    message_obj = message
    await message.delete(delay = 0.1)
    msg = message_obj.content
    key_title = re.findall(r'[-][-][T][I][T][L][E][=]["].*?["]', msg)
    if len(key_title) == 0:
        raise Exception("Error in confession syntax")
    key_title_value = re.findall(r'["].*?[^#]["]', key_title[0])
    key_title_value = key_title_value[0][1:-1]
    msg = msg.replace(key_title[0], "")
    if "--ANONYMOUS" in message.content:
        msg = msg.replace("--ANONYMOUS", "")
        edict = {
        "color" : 0xf71e4b,
        "author" : {
            "name" : "Anonymous",
            "icon_url" : "https://lh3.googleusercontent.com/proxy/Pz5KgTRUmlIUMxxwl48WenO1yVnN-sOD4SJBHHv7LWsW0D5mlvivurY3aQfG4TtFNSW-OW9uIuneOiISBpOimUHqIDmliO0m1lW1H3zSVq7c_Vtg0w"
        },
        "title" : key_title_value,
        "description" : msg,
        "footer" : {
            "text" : f"{message.guild.name}",
            "icon_url" : f"{message.guild.icon_url}"
        },
        "timestamp" : datetime.datetime.utcnow().isoformat()
        }
        edict = discord.Embed.from_dict(edict) 
    else:
        edict = {
        "color" : 0xf71e4b,
        "author" : {
            "name" : f"{message_obj.author}",
            "icon_url" : f"{message_obj.author.avatar_url}"
        },
        "title" : key_title_value,
        "description" : msg,
        "footer" : {
            "text" : f"{message.guild.name}",
            "icon_url" : f"{message.guild.icon_url}"
        },
        "timestamp" : datetime.datetime.utcnow().isoformat()
        }
        edict = discord.Embed.from_dict(edict)
    await message_obj.channel.send(embed = edict)