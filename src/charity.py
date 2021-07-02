# API Trigger & RDBMS
from ch_boot.client_token import *
from ch_boot.on_guild_join import *

# welcome
from ch_welcome.welcome import *               # | requires setup

# utilities
from ch_utilities.afk import *
from ch_utilities.dictionary import *
from ch_utilities.poll import *
from ch_utilities.translate import *
from ch_utilities.web import *
from ch_utilities.youtube import *
from ch_utilities.songlyrics import *

# automod
from ch_automod.antimassmention import *       # | requires setup
from ch_automod.antispam import *              # | requires setup
from ch_automod.bgt_sweeper import *           # | background process

# moderation
from ch_moderation.warn import *
from ch_moderation.mute import *              
from ch_moderation.unmute import *            
from ch_moderation.kick import *              
from ch_moderation.ban import *               
from ch_moderation.tban import *              
from ch_moderation.unban import *
from ch_moderation.modmail_v2 import *         # | requires setup
from ch_moderation.purge_message import *
from ch_moderation.modlogger import *          # | requires setup
from ch_moderation.message import *
from ch_moderation.reply import *
from ch_moderation.schedule import *

# fun
from ch_fun.hello import *
from ch_fun.starboard import *

# solaris exclusive
from ch_solaris.modmail import *
from ch_solaris.confession import *
from ch_solaris.momma import *

# Boot
from ch_boot.startup import *

run()