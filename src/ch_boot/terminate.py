from ch_boot.startup import *
from ch_discord_utils.embed_generator import meta_message

@charity.listen("on_message")
async def on_terminate(message):
    if message.author.id == 799186130654199809 and message.content == ";logout":
        message.reply(embed = meta_message(description = meta_message(description = "**`Shard logging out...`**")))
        exit()