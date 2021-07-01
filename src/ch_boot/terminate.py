from ch_boot.startup import *

@charity.listen("on_message")
async def on_terminate(message):
    if message.author.id == 799186130654199809 and message.content == ";logout":
        exit()