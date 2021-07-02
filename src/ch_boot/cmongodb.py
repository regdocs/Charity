import pymongo
from pymongo import MongoClient

mongoclient = MongoClient(r"mongodb+srv://jayantapandit:JI%26%2ACJ%25AAmongodb871@cluster0.5bm98.mongodb.net/test")
charity_alpha_mdb = mongoclient['charity-alpha']

clc_afk = charity_alpha_mdb['away-from-keyboard']
clc_gconfig = charity_alpha_mdb['server-config']
clc_usrinfract = charity_alpha_mdb['user-infractions']
clc_starboard = charity_alpha_mdb['starboard-db']