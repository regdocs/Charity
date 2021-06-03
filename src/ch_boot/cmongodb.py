import pymongo
from pymongo import MongoClient

mongoclient = MongoClient(r"mongodb+srv://jayantapandit:JI%26%2ACJ%25AAmongodb871@cluster0.5bm98.mongodb.net/test")
charity_alpha_mdb = mongoclient['charity-alpha']

clc_afk = charity_alpha_mdb['away-from-keyboard']
clc_polls = charity_alpha_mdb['polls']
clc_announcements = charity_alpha_mdb['scheduled-announcements']
clc_reminders = charity_alpha_mdb['scheduled-reminders']
clc_infractions = charity_alpha_mdb['server-config']
clc_gconfig = charity_alpha_mdb['user-infractions']