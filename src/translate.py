import discord
from google_trans_new import google_translator, constant
from discord.ext import commands, tasks
from startup import *

@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def translate(ctx, *arg):
    await ctx.channel.trigger_typing()
    translator = google_translator()
    gt_LANGUAGES = constant.LANGUAGES
    src0 = ""
    dest0 = ""
    quick_translate_flag = True
    match_found = False
    if len(arg) != 0:
        for x in range(len(arg)):
            if arg[x] in gt_LANGUAGES.values() and x <= 1:
                quick_translate_flag = False
                break
        if quick_translate_flag:
            src0 = "auto"
            dest0 = "auto"
            tb_translated = ' '.join(arg)
            result = translator.translate(tb_translated, lang_src = src0, lang_tgt = dest0, pronounce = True)
            embed = cog_embed(
            ctx = ctx,
            title = f":books: Translating to **ENGLISH**",
            description = f"**`Source:`** _{tb_translated}_\n\n**`Translation:`** _{result[0]}_",
            colour = 0x38da07
            )
            await ctx.reply(embed = embed)
            return
        src0 = arg[0]
        dest0 = arg[1]
        args = ' '.join(arg[2:])
        if src0 == "english": src0 = "en"
        else:
            for i in gt_LANGUAGES.values():
                src0_lower = src0.lower()
                if src0_lower == i:
                    for x, y in gt_LANGUAGES.items():
                        if y == i:
                            src0 = x
                            match_found = True
                            break
        if dest0 == "english": dest0 = "en"
        else:
            for i in gt_LANGUAGES.values():
                dest0_lower = dest0.lower()
                if dest0_lower == i:
                    for x, y in gt_LANGUAGES.items():
                        if y == i:
                            dest0 = x
                            match_found = True
                            break
        if src0.lower() == "chinese":
            src0 = "zh-cn"
            match_found = True
        if dest0.lower() == "chinese":
            dest0 = "zh-cn"
            match_found = True
    else:
        src0 = "auto"
        dest0 = "auto"
        tb_translated = await ctx.fetch_message(ctx.message.reference.message_id)
        result = translator.translate(tb_translated.content, lang_src = src0, lang_tgt = dest0, pronounce = True)
        embed = cog_embed(
        ctx = ctx,
        title = f":books: Translating to **ENGLISH**",
        description = f"**`Source:`** _{tb_translated.content}_\n\n**`Translation:`** _{result[0]}_",
        colour = 0x38da07
        )
        await tb_translated.reply(embed = embed, mention_author = False)
        return
    if not match_found:
        raise Exception("Invalid arguments provided.")
    result = translator.translate(args, lang_src = src0, lang_tgt = dest0, pronounce = True)
    pronounce_src = result[1]
    pronounce_dest = result[2]
    if pronounce_src == None:
        pronounce_src = ":warning: N/A"
    if pronounce_dest == None:
        pronounce_dest = ":warning: N/A"
    embed = cog_embed(
        ctx = ctx,
        title = f":books: Translating from **{gt_LANGUAGES[src0].upper()}** to **{gt_LANGUAGES[dest0].upper()}**",
        description = f"**`Source:`** _{args}_\n**`Source pronunciation:`** _{pronounce_src}_\n\n**`Translation:`** _{result[0]}_\n**`Translation pronunciation:`** _{pronounce_dest}_",
        colour = 0x38da07,
        )
    await ctx.reply(embed = embed)

@translate.error
async def translate_error(ctx, error):
    msg = "**ERROR:** {}".format(error)
    await ctx.reply(msg)
