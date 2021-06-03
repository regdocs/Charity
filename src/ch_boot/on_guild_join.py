from ch_boot.startup import *
import discord
from discord.ext import commands
from ch_boot.cmongodb import *

@charity.event
async def on_guild_join(guild):
    if clc_gconfig.find_one({ "_id" : f"{guild.id}" }) is not None:
        new_config = {
            u"_id" : guild.id,
            
            # for analysis and mass-exit
            u"bool_attempted_setup" : False,
            u"bool_setup" : False,

            # the following are given the permission to handle the bot
            # permission for guild administrators are enabled by default
            u"bot_handlers_roles" : [],

            # anti mass-mention module configuration
            u"antimassmention_config" : {
                u"module_active" : False,
                u"massmention_threshold" : 8
            },
            
            # antispam module configuration
            u"antispam_config" : {
                u"module_active" : False,
                u"spam_filter_text_channel_exceptions" : [],
                u"spam_warn_msg_count" : 8,
                u"spam_warn_timeout" : 10,
                u"penalty" : 0, # penalty is 0 for mute, 1 for kick, 2 for ban 
                
                u"spam_warn_reason" : u"Spamming in public chat",
                u"spam_warn_duration" : 60,

                u"spam_mute_duration" : 60,
                u"spam_mute_reason" : u"Spamming in public chat",
                
                u"spam_kick_reason" : u"Spamming in public chat",
                
                u"spam_ban_reason" : u"Spamming in public chat",
                u"spam_ban_history_delete_daycount" : 0,
                u"spam_ban_duration" : 7 # days
            },

            # modmail module configuration
            u"modmail_v2_config": {
                u"module_active" : False,
                u"modmail_channel_category_id" : None,
                u"modmail_log_dump_text_channel_id" : None
            },

            # logger module configuration
            u"logger_config" : {
                u"module_active" : False,
                u"logger_log_dump_text_channel_id" : None,
                u"bool_on_message_delete" : False,
                u"bool_on_bulk_message_delete" : False,
                u"bool_on_message_edit" : False,
                u"bool_on_guild_channel_create" : False,
                u"bool_on_guild_channel_delete" : False,
                u"bool_on_member_join" : False,
                u"bool_on_member_remove" : False,
                u"bool_on_member_update" : False,
                u"bool_on_guild_role_create" : False,
                u"bool_on_guild_role_delete" : False,
                u"bool_nonapi_warn" : False,
                u"bool_nonapi_mute" : False,
                u"bool_on_member_ban" : False,
                u"bool_on_member_unban" : False,
                u"bool_on_invite_create" : False, 
                u"bool_on_voice_state_update" : False,
            },

            # infractions module [warn] log configuration
            u"warn_config" : {
                # :(
            },

            # infractions module [mute] log configuration
            u"mute_config" : {
                u"bool_guild_mute_role_id" : None
            },

            # infractions module [ban] log configuration
            u"ban_config" : {
                u"ban_history_delete_daycount" : 0
            },

            # infractions module [temporary ban] log configuration
            u"tban_config" : {
                u"history_delete_daycount" : 0
            }
        }