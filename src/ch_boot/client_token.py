import os

CHARITY_TOKEN = os.getenv('CHARITY_TOKEN')
GENIUS_API_TOKEN = os.getenv('GENIUS_API_TOKEN')

GUILD_CONFIGURATION = {
    # insert GUILD ID here
    "_id" : None,
    
    # for analysis and mass-exit
    "bool_attempted_setup" : False,
    "bool_setup" : False,

    # the following are given the permission to handle the bot
    # permission for guild administrators are enabled by default
    "bot_handlers_roles" : [],

    "automod_config" : {
        # anti mass-mention module configuration
        "antimassmention_config" : {
            "module_active" : False,
            "massmention_threshold" : 8,
            "massmention_warn_reason" : "Mass-mentioning guild members",
            "massmention_warn_record_timeout" : 60,
        },
        
        # antispam module configuration
        "antispam_config" : {
            "module_active" : False,
            "spam_filter_text_channel_exceptions" : [],
            "spam_warn_msg_count" : 8,
            "spam_warn_timeout" : 10,
            "spam_warn_reason" : "Spamming in public chat",
            "spam_warn_record_timeout" : 60,
        },
    },

    "moderation_config" : {
        # modmail module configuration
        "modmail_v2_config": {
            "module_active" : False,
            "modmail_category_id" : None,
            "modmail_log_dump_text_channel_id" : None
        },

        # logger module configuration
        "logger_config" : {
            "module_active" : False,
            "logger_log_dump_text_channel_id" : None,
            "bool_on_message_delete" : False,
            "bool_on_bulk_message_delete" : False,
            "bool_on_message_edit" : False,
            "bool_on_guild_channel_create" : False,
            "bool_on_guild_channel_delete" : False,
            "bool_on_member_join" : False,
            "bool_on_member_remove" : False,
            "bool_on_member_update" : False,
            "bool_on_guild_role_create" : False,
            "bool_on_guild_role_delete" : False,
            "bool_nonapi_warn" : False,
            "bool_nonapi_mute" : False,
            "bool_on_member_kick" : False,
            "bool_on_member_ban" : False,
            "bool_on_member_unban" : False,
            "bool_on_invite_create" : False, 
            "bool_on_voice_state_update" : False,
        },

        # infractions module [warn] log configuration
        "warn_config" : {
            # :(
        },

        # infractions module [mute] log configuration
        "mute_config" : {
            "guild_mute_role_id" : None,
            "bool_remove_existing_roles_and_reassign" : True
        },

        # infractions module [ban] log configuration
        "ban_config" : {
            "def_ban_history_delete_daycount" : 0
        },

        # infractions module [temporary ban] log configuration
        "tban_config" : {
            "def_tban_history_delete_daycount" : 0
        }
    },

    "utilities_config" : {
        "afk_config" : {
            "module_active" : False,
            "afk_note_max_length" : 100,
            "bool_link_allowed" : False,
            "bool_mentions_allowed" : False
        },

        "starboard_config" : {
            "module_active" : False,
            "starboard_min_score" : 8,
            "starboard_dump" : None,
        }
    }
}