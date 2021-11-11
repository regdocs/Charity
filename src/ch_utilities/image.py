import discord
from discord.ext import commands
from googlesearch import search
from ch_boot.startup import *
from ch_discord_utils.embed_generator import *
import urllib.request
import urllib
import re

class Bing:
    def __init__(self, query, limit, adult, timeout,  filters='', verbose=True):
        self.download_count = 0
        self.query = query
        self.adult = adult
        self.filters = filters
        self.verbose = verbose
        self.links = ['heh']

        assert type(limit) == int, "limit must be integer"
        self.limit = limit
        assert type(timeout) == int, "timeout must be integer"
        self.timeout = timeout

        # self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        self.page_counter = 0
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
      'AppleWebKit/537.11 (KHTML, like Gecko) '
      'Chrome/23.0.1271.64 Safari/537.11',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}
    
    def run(self):
        # Parse the page source and download pics
        request_url = 'https://www.bing.com/images/async?q=' + urllib.parse.quote_plus(self.query) \
                      + '&first=' + str(self.page_counter) + '&count=' + str(self.limit) \
                      + '&adlt=' + self.adult + '&qft=' + ('' if self.filters is None else str(self.filters))
        request = urllib.request.Request(request_url, None, headers=self.headers)
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf8')
        if html ==  "":
            self.links = [0]
            return
        links = re.findall('murl&quot;:&quot;(.*?)&quot;', html)
        self.links = links

def download(query, limit=100, output_dir='dataset', adult_filter_off=True, force_replace=False, timeout=60, verbose=True):
    # engine = 'bing'
    if adult_filter_off:
        adult = 'off'
    else:
        adult = 'on'
    bing = Bing(query, limit, adult, timeout, verbose)
    bing.run()
    return bing.links

@charity.command()
@commands.has_any_role("Alpha tester", 840545860101210122, 830486598050119740, 843198710782361682, 836122037009121312)
async def image(ctx, limit: typing.Optional[int] = 1, *, searchstring):
    await ctx.channel.trigger_typing()
    if limit > 5:
        limit = 3
        await ctx.message.reply(content='Download limit cannot exceed 5: Resorting to 3...')
    links = download(searchstring, limit=limit, adult_filter_off=False, timeout=60, verbose=False)
    if links[0] == 0:
        await ctx.reply(embed=meta_message(colour=0x007c6d, description=f'No image results found :face_in_clouds: Try searching again with related keywords?'))
    for j in links:
        await ctx.reply(embed=meta_message(colour=0x007c6d, description=f'`IMAGE RESULT #{links.index(j)+1}` from [`Bing`](https://bing.com) & the [**`MEDIA LINK`**]({j})', image_url=j), mention_author=False)

@image.error
async def web_error(ctx, error):
    msg = error
    await ctx.reply('An unexpected error occured :(\n**!**:bellhop: <@799186130654199809>')
