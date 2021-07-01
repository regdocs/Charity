from ch_boot.client_token import GENIUS_API_TOKEN
from discord.ext import commands
from ch_discord_utils.embed_generator import *
from ch_boot.startup import *
import lyricsgenius, multiprocessing

@charity.command()
async def lyrics(ctx, *, song):
    msg = await ctx.reply(f":mag: **Searching lyrics for** `{song}`")
    await ctx.channel.trigger_typing()
    genius = lyricsgenius.Genius(GENIUS_API_TOKEN)
    try:
        retrieved = genius.search_song(title = song, get_full_info = False)
    except: pass
    if retrieved == None:
        await msg.edit(content = ":mag: **No results found :(**")
        raise Exception("Song not found :(")
    await msg.edit(
        content = f":mag: **Match found for** `{song}`",
        embed = create_embed(
            author_name = "",
            author_icon_url = "",
            title = retrieved.full_title.replace(u'\xa0', u' '),
            thumbnail_url = retrieved.header_image_thumbnail_url,
            description = retrieved.lyrics,
            footer_text = "Lyrics from Genius.com",
            footer_icon_url = f"{ctx.author.avatar_url}"
        )
    )

@lyrics.error
async def lyrics_error(ctx, error):
    msg = error
    await ctx.reply(msg)