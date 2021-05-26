import client_token
import discord
from discord.ext import commands, tasks
import typing
import time

from afk import *
from announce import *
from antispam import *
from ban import *
from confession import *
from dictionary import *
from embed_generator import *
from hello import *
from kick import *
from message import *
from modmail import *
# from music import *
from mute import *
from poll import *
from purge import *
from reply import *
from startup import *
from translate import *
from unban import *
from unmute import *
from warn import *
from web import *
from welcome import *
from youtube import *

logger()
startup()

@charity.event
async def on_ready():
    print(f"Logged in as {charity.user} PFID: {charity.user.id}")
    time.sleep(1)
    print("-----------------------------------------------------------------------------")

charity.run(client_token.CHARITY_TOKEN)
