import discord
from PyDictionary import PyDictionary as Pydict
from ch_discord_utils.embed_generator import *
from discord.ext import commands
from ch_boot.startup import *

@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def define(ctx, arg):
    await ctx.channel.trigger_typing()
    try: dict = Pydict(arg)
    except: raise Exception("No results found.")

    meanings = dict.getMeanings()
    synonyms = dict.synonym(arg)
    antonyms = dict.antonym(arg)

    keyerror_noun = False
    keyerror_verb = False
    keyerror_adverb = False
    keyerror_adjective = False
    keyerror_pronoun = False
    keyerror_preposition = False
    keyerror_conjunction = False
    keyerror_interjection = False

    try: noun_meanings = meanings[arg]['Noun']
    except KeyError: keyerror_noun = True
    try: noun_meanings = meanings[arg]['Verb']
    except KeyError: keyerror_verb = True
    try: noun_meanings = meanings[arg]['Adjective']
    except KeyError: keyerror_adjective = True
    try: noun_meanings = meanings[arg]['Adverb']
    except KeyError: keyerror_adverb = True
    try: noun_meanings = meanings[arg]['Pronoun']
    except KeyError: keyerror_pronoun = True
    try: noun_meanings = meanings[arg]["Proposition"]
    except KeyError: keyerror_preposition = True
    try: noun_meanings = meanings[arg]['Conjunction']
    except KeyError: keyerror_conjunction = True
    try: noun_meanings = meanings[arg]['Interjection']
    except KeyError: keyerror_interjection = True

    dsc = "**`Meanings:`**\n"
    if not keyerror_noun:
        dsc += "**_Noun:_**\n"
        for i in range(len(meanings[arg]['Noun'])):
            dsc = dsc + f"{i+1}. _{meanings[arg]['Noun'][i]}_\n"
        dsc += "\n"
    if not keyerror_verb:
        dsc += "**_Verb:_**\n"
        for i in range(len(meanings[arg]['Verb'])):
            dsc = dsc + f"{i+1}. _{meanings[arg]['Verb'][i]}_\n"
        dsc += "\n"
    if not keyerror_adjective:
        dsc += "**_Adjective:_**\n"
        for i in range(len(meanings[arg]['Adjective'])):
            dsc = dsc + f"{i+1}. _{meanings[arg]['Adjective'][i]}_\n"
        dsc += "\n"
    if not keyerror_adverb:
        dsc += "**_Adverb:_**\n"
        for i in range(len(meanings[arg]['Adverb'])):
            dsc = dsc + f"{i+1}. _{meanings[arg]['Adverb'][i]}_\n"
        dsc += "\n"
    if not keyerror_pronoun:
        dsc += "**_Pronoun:_**\n"
        for i in range(len(meanings[arg]['Pronoun'])):
            dsc = dsc + f"{i+1}. _{meanings[arg]['Pronoun'][i]}_\n"
        dsc += "\n"
    if not keyerror_preposition:
        dsc += "**_Preposition:_**\n"
        for i in range(len(meanings[arg]['Preposition'])):
            dsc = dsc + f"{i+1}. _{meanings[arg]['Preposition'][i]}_\n"
        dsc += "\n"
    if not keyerror_conjunction:
        dsc += "**_Conjunction:_**\n"
        for i in range(len(meanings[arg]['Conjunction'])):
            dsc = dsc + f"{i+1}. _{meanings[arg]['Conjunction'][i]}_\n"
        dsc += "\n"
    if not keyerror_interjection:
        dsc += "**_Interjection:_**\n"
        for i in range(len(meanings[arg]['Interjection'])):
            dsc = dsc + f"{i+1}. _{meanings[arg]['Interjection'][i]}_\n"
        dsc += "\n"

    if len(synonyms) != 0:
        dsc += "**`Synonyms:`**\n" + ', '.join(synonyms) + "\n\n"
    if len(antonyms) != 0:
        dsc += "**`Antonyms:`**\n" + ', '.join(antonyms)
            
    embed = create_embed(
        title = f":book: **Entry: _`{arg.lower()}`_**",
        description = dsc,
        colour = 0x38da07,
        footer_text = ctx.guild.name,
        footer_icon_url = ctx.guild.icon_url
        )    
    await ctx.reply(embed = embed)

@define.error
async def define_error(ctx, error):
    msg = error
    await ctx.reply(msg)

