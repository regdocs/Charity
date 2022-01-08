import pymongo
import os
from pymongo import MongoClient

mongoclient = MongoClient(os.getenv('MONGODB_TOKEN'))
charity_alpha_mdb = mongoclient['charity-alpha']

clc_afk = charity_alpha_mdb['away-from-keyboard']
clc_gconfig = charity_alpha_mdb['server-config']
clc_usrinfract = charity_alpha_mdb['user-infractions']
clc_starboard = charity_alpha_mdb['starboard-db']
clc_modmail = charity_alpha_mdb['modmail-active-tickets']