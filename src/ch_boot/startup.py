from discord.ext import commands
import ch_boot.client_token
import discord
import typing
import time

def startup():
    print()
    print("  ░█████╗░██╗░░██╗░█████╗░██████╗░██╗████████╗██╗░░░██╗░░░██████╗░██╗░░░██╗")
    print("  ██╔══██╗██║░░██║██╔══██╗██╔══██╗██║╚══██╔══╝╚██╗░██╔╝░░░██╔══██╗╚██╗░██╔╝")
    print("  ██║░░╚═╝███████║███████║██████╔╝██║░░░██║░░░░╚████╔╝░░░░██████╔╝░╚████╔╝░")
    print("  ██║░░██╗██╔══██║██╔══██║██╔══██╗██║░░░██║░░░░░╚██╔╝░░░░░██╔═══╝░░░╚██╔╝░░")
    print("  ╚█████╔╝██║░░██║██║░░██║██║░░██║██║░░░██║░░░░░░██║░░░██╗██║░░░░░░░░██║░░░")
    print("  ░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░╚═╝░░░░░░╚═╝░░░╚═╝╚═╝░░░░░░░░╚═╝░░░")
    print()
    print("  # Script           : charity.py")
    print("  # Version          : 1.0rc")
    print("  # Description      : Versatile moderation bot utilising modern Pythonic Discord API (PyPi v1.7.2)")
    print("  # Env Dependency   : Python 3.5.3 or higher")
    print("  # Author           : github.com/ivorytone")
    print("  # Email            : jay.dnb@protonmail.ch")
    print()

intents = discord.Intents.all()
activity = discord.Activity(name='over Solaris', type=discord.ActivityType.watching)
charity = commands.Bot(command_prefix = ';', activity = activity, intents = intents, status=discord.Status.dnd)

@charity.event
async def on_ready():
    print(f"  Logged in as {charity.user} PFID: {charity.user.id}:\n")

def run():
    startup()
    charity.run(ch_boot.client_token.CHARITY_TOKEN)