import pymongo
from pymongo import MongoClient

mongoclient = MongoClient(r"mongodb+srv://jayantapandit:JI%26%2ACJ%25AAmongodb871@cluster0.5bm98.mongodb.net/test")
charity_alpha_mdb = mongoclient['charity-alpha']
clc_gconfig = charity_alpha_mdb['server-config']


new_config = {
    u"_id" : 802459550434852894,
    
    # for analysis and mass-exit
    u"bool_attempted_setup" : False,
    u"bool_setup" : False,

    # the following are given the permission to handle the bot
    # permission for guild administrators are enabled by default
    u"bot_handlers_roles" : [],

    u"automod_config" : {
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
            # warning level 1
            u"spam_warn_reason" : u"Spamming in public chat",
            u"spam_warn_duration" : 60,
            # mute level 2
            u"spam_mute_duration" : 60,
            u"spam_mute_reason" : u"Spamming in public chat",
            # kick level 3
            u"spam_kick_reason" : u"Spamming in public chat",
            # ban level 4
            u"spam_ban_reason" : u"Spamming in public chat",
            u"def_spam_ban_history_delete_daycount" : 0,    # this is a default argument
            u"spam_ban_duration" : 7 # days
        },
    },

    u"moderation_config" : {
        # modmail module configuration
        u"modmail_v2_config": {
            u"module_active" : False,
            u"modmail_category_id" : None,
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
            u"def_ban_history_delete_daycount" : 0
        },

        # infractions module [temporary ban] log configuration
        u"tban_config" : {
            u"def_tban_history_delete_daycount" : 0
        }
    },

    u"utilities_config" : {
        u"afk_config" : {
            u"afk_note_max_length" : 100,
            u"bool_link_allowed" : False,
            u"bool_mentions_allowed" : False
        }
    }
}

clc_gconfig.insert_one(new_config)
