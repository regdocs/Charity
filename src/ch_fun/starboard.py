from ch_boot.startup import *
from ch_boot.cmongodb import *
from ch_discord_utils.embed_generator import *

@charity.listen("on_raw_reaction_add")
async def get_star_react(raw_reaction):
    guild_id = raw_reaction.guild_id
    channel_id = raw_reaction.channel_id
    message_id = raw_reaction.message_id
    gconfig = clc_gconfig.find_one({ "_id" : guild_id })
    if gconfig['utilities_config']['starboard_config']['module_active'] == False:
        return
    if gconfig['utilities_config']['starboard_config']['starboard_dump'] == channel_id:
        return
    x = charity.get_guild(guild_id).get_channel(channel_id)
    message = await x.fetch_message(message_id)
    reactions = message.reactions
    star_count = 0
    for i in reactions:
        if i.emoji == '⭐':
            star_count = i.count
            users = await i.users().flatten()
            if message.author in users:
                star_count -= 1
            break
    qposted = clc_starboard.find_one({ "_id" : f"{message.jump_url}" })
    if star_count == gconfig['utilities_config']['starboard_config']['starboard_min_score'] and qposted == None:
        dump = charity.get_guild(guild_id).get_channel(gconfig['utilities_config']['starboard_config']['starboard_dump'])
        await dump.send(
            embed = create_embed(
                author_name = f'{message.author}',
                author_icon_url = f'{message.author.avatar_url}',
                title = "Starboard message URL ⭐",
                title_url = f'{message.jump_url}',
                description = f'{message.content}',
                footer_text = f'{message.guild.name}',
                footer_icon_url = f'{message.guild.icon_url}',
                timestamp = "",
                colour = 0xffea00
            )
        )
        insert = {
            "_id" : f"{message.jump_url}"
        }
        clc_starboard.insert_one(insert)