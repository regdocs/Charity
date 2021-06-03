import discord
import logging
from discord.ext import commands

def startup():
    print()
    print("  ░█████╗░██╗░░██╗░█████╗░██████╗░██╗████████╗██╗░░░██╗░░░██████╗░██╗░░░██╗")
    print("  ██╔══██╗██║░░██║██╔══██╗██╔══██╗██║╚══██╔══╝╚██╗░██╔╝░░░██╔══██╗╚██╗░██╔╝")
    print("  ██║░░╚═╝███████║███████║██████╔╝██║░░░██║░░░░╚████╔╝░░░░██████╔╝░╚████╔╝░")
    print("  ██║░░██╗██╔══██║██╔══██║██╔══██╗██║░░░██║░░░░░╚██╔╝░░░░░██╔═══╝░░░╚██╔╝░░")
    print("  ╚█████╔╝██║░░██║██║░░██║██║░░██║██║░░░██║░░░░░░██║░░░██╗██║░░░░░░░░██║░░░")
    print("  ░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░╚═╝░░░░░░╚═╝░░░╚═╝╚═╝░░░░░░░░╚═╝░░░")
    print()
    print("  # Script          : charity.py")
    print("  # Version         : 1.0rc")
    print("  # Description     : Versatile moderation bot utilising modern Pythonic Discord API (PyPi v1.7.2)")
    print("  # Dependencies    : Python 3.5.3 or higher,")
    print("                      Python libraries including discord, PyNaCl (Voice Support)")
    print("                      discord.ext, youtube_dl, googlesearch, beautifulsoup4")
    print("                      urllib.parse, urllib.request, re, threading")
    print("  # Author          : github.com/ivorytone")
    print("  # Email           : jay.dnb@protonmail.ch")
    print()
    print("=============================================================================")
    
intents = discord.Intents.all()
activity = discord.Activity(name='over Solaris', type=discord.ActivityType.watching)
charity = commands.Bot(command_prefix = ';', activity = activity, intents = intents, status=discord.Status.dnd)
