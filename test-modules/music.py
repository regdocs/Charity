import discord
from discord.ext import commands
import youtube_dl
import urllib.parse, urllib.request, re
from startup import * # include run('token')

# ===================== MUSIC.PY ======================
youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return filename

@charity.command()
async def join(ctx):
    """Joins a voice channel"""
    channel = ctx.author.voice.channel
    await channel.connect()

@charity.command()
async def play(ctx, *, search):
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            if search[0:31] == "http://www.youtube.com/watch?v=" or search[0:32] == "https://www.youtube.com/watch?v=":
                url = search
            else:
                query_string = urllib.parse.urlencode({'search_query': search})
                htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
                search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
                await ctx.send('`PLAYING TOP RESULT:` http://www.youtube.com/watch?v=' + search_results[0])
                url = 'http://www.youtube.com/watch?v=' + search_results[0]
            filename = await YTDLSource.from_url(url, loop=charity.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename))
        await ctx.send('**Now playing :)**')
    except:
        await ctx.send("**An error occurred :(**")

@charity.command()
async def stop(ctx):
    await ctx.voice_client.disconnect()

@play.before_invoke
async def ensure_voice(ctx):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()
# ===================== MUSIC.PY ======================
