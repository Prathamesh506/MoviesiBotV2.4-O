import re
from os import environ
from Script import script 

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

####################################################################################################################################################################
####################################################################################################################################################################

# --------------------------- ULTRON -----------------------------------

# BOT_TOKEN = environ.get("BOT_TOKEN", "7247107038:AAFMRijILhwy9ESt2t9e6kFTY7JQk4XwTew")

# DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://shadow:shadow506@cluster0.srfnz9s.mongodb.net/?retryWrites=true&w=majority")

# PICS = (environ.get('PICS', 'https://telegra.ph/file/96aa21c66eec5a24b9644.jpg https://telegra.ph/file/84bd10861f905d72adcaf.jpg https://telegra.ph/file/d315eaa802cdb2f790a5a.jpg https://telegra.ph/file/a25ea7f7a746ac1c544e3.jpg https://telegra.ph/file/40d555da9059bb1b0fcd7.jpg https://telegra.ph/file/2efd3b607301d692a634b.jpg https://telegra.ph/file/6e66b7dd8b9b30ace0f93.jpg https://telegra.ph/file/a320d989754c8dea12b02.png')).split()


#--------------------------- OPTIMUS -----------------------------------

# BOT_TOKEN = environ.get("BOT_TOKEN", "7229261743:AAEcDqJZkF9KVwDaBpV3iUdekLL21WLKD7k")

# DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://Optimus:Optimus@cluster0.uztjyky.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# PICS = (environ.get('PICS', 'https://telegra.ph/file/6d0ac3a97740c0d9b4932.jpg https://telegra.ph/file/e2c6fcd43ec729f63572a.jpg https://telegra.ph/file/a6328a8ea1ed1bfbe0e6d.jpg https://telegra.ph/file/e08b02941d5738d6b934b.jpg https://telegra.ph/file/4df4f4f20c19bd00f9908.jpg')).split()


# #--------------------------- SCARLET WITCH ( old )-----------------------------------


BOT_TOKEN = environ.get("BOT_TOKEN", "7189786967:AAFHHQ23HfVgsYgbFsMruKgf6jUYtSztS1k")

DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://scarlet:scarlet@cluster0.iibbctz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")


PICS = (environ.get('PICS', 'https://telegra.ph/file/9203de86a8e55d14fa304.jpg https://telegra.ph/file/b9ed75fcef91d7edd629b.jpg https://telegra.ph/file/931798c653da0fa85b182.jpg https://telegra.ph/file/45162159d9b57fe6b270c.jpg ')).split()


#--------------------------- MAKIMA -----------------------------------

# BOT_TOKEN = environ.get("BOT_TOKEN", "7195878471:AAGjpjZCZgvsMrIViQB3cxrUv8A7_fX8870")

# DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://makima:makima@cluster0.covyf0w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# PICS = (environ.get('PICS', 'https://telegra.ph/file/7ad2ddfeedf7396acb82f.jpg')).split()


#--------------------------- TESTING -----------------------------------

# BOT_TOKEN = environ.get("BOT_TOKEN", "6583753281:AAFtg5TYcGEToa99k0hbOYrrkZXJIXWQXHk")

# DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://Testing:Testing@cluster0.6fjlhzr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# PICS = (environ.get('PICS', 'https://telegra.ph/file/6e7b046bdf205092f798b.jpg')).split()

####################################################################################################################################################################
####################################################################################################################################################################


#------------------ BOT DETAILS ----------------------------------------
    
SESSION = environ.get('SESSION', 'MoviesiBotV4')
API_ID = "3704207"
API_HASH = environ.get("API_HASH", "8d20e46f5413139329f2ec753f7c482a")

#------------------- ADMINS & AUTH_USERS -------------------------------

ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '1531899507').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]


#-------------------PAYMENTS AND VERIFICATION INFO----------------

UPI_ID = "atvixt-2@oksbi"
OWNER_USERNAME ="Shadow506"
UPIQRPIC = "https://telegra.ph/file/6eaf67a6b34db55957412.jpg"

#--------------------- DATABSES & CHANNLS ----------------------

GRP_LINK = environ.get('GRP1', 'https://t.me/+D-ijrG90oYw3NWNl') 
SUP_LINK = environ.get('SUP_LINK', 'https://t.me/TeamiVega') 
UPDATES =environ.get('UPDATES', 'CineArcade') 

# auth_channel = "-1002086574998"
auth_channel = "-1002217702204"#OPTIMUS
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002131280557'))
NO_RES_CNL = int(environ.get('NO_RES_CNL', '-1002137535594')) 
support_chat_id = environ.get('support_chat_id',"-1002044884739")
reqst_channel = environ.get('reqst_channel',"-1002019169484")

#DATABASE CHANNELS
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1001997311406 -1001908988097 -1001977939308 -1002052107035 -1002031777198 -1002120266966 -1001638006524').split()]

#MULTI FILE AUTO DELETE
DELETE_CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1001997311406 -1001908988097 -1001977939308 -1002052107035 -1002031777198 -1002120266966').split()] 

#-------------------------- IMAGES -------------------------------

IMDB_IMG = environ.get("IMDB_IMG", "https://telegra.ph/file/4b873b46bb4861f78ce6d.jpg")
WATCH_IMG = environ.get("WATCH_IMG", "https://telegra.ph/file/b9ed75fcef91d7edd629b.jpg")
WELCOME_PICS = environ.get("WELCOME_PICS", "https://telegra.ph/file/4b873b46bb4861f78ce6d.jpg")

#-------------------------- DATABASE MONGODB -------------------------

DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'MoviesiBotV4')


#-------------------------VERIFY AND SHORTNER--------------------------

IS_VERIFY = is_enabled((environ.get('IS_VERIFY', 'True')), True) 
SHORTLINKS = is_enabled((environ.get('SHORTLINKS', 'False')), False)

# SHORTLINK_URL = environ.get('SHORTLINK_URL', 'afly.in')
# SHORTLINK_API = environ.get('SHORTLINK_API', '77e4228021224fb293f6be6afc41d10c01087800')

SHORTLINK_URL = environ.get('SHORTLINK_URL', 'easysky.in')
SHORTLINK_API = environ.get('SHORTLINK_API', 'aeefe7b8bdf0d505ecf7c778f067fa1c4c65df04')#cinearcade

#SECOUNDY BACKUP SHORTNER IN CASE OF PRIMARY WEB FAILUAR
SHORTLINK_URL_BKUP = environ.get('SHORTLINK_URL_BKUP', 'tnshort.net')
SHORTLINK_API_BKUP = environ.get('SHORTLINK_API_BKUP',"5b8c9497bbeabea5a30c16062eeba6b3fe6bbd13")

DOWNLOAD_TIPS = environ.get('HOW_TO_VERIFY', "https://t.me/Vegalatest/15")
HOW_TO_VERIFY = environ.get('HOW_TO_VERIFY', "https://t.me/Vegalatest/12")

#--------------------------BOT SETTINGS-----------------------------

DLT = int(environ.get('DLT', 600))
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", f"{script.CAPTION}")
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
WELCOW_NEW_USERS = is_enabled((environ.get('WELCOW_NEW_USERS', "False")), False)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), False)
SRC_MSG = True
PORT = environ.get("PORT", "8080")

#---------------------------- LOGS -----------------------------------

REQST_CHANNEL = int(reqst_channel) if reqst_channel and id_pattern.search(reqst_channel) else None
SUPPORT_CHAT_ID = int(support_chat_id) if support_chat_id and id_pattern.search(support_chat_id) else None  
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
AUTH_USERS = (auth_users + ADMINS) if auth_users else []

LOG_STR = "Current Cusomized Configurations are:-\n"
LOG_STR += (f"CUSTOM_FILE_CAPTION enabled with value {CUSTOM_FILE_CAPTION}, your files will be send along with this customized caption.\n" if CUSTOM_FILE_CAPTION else "No CUSTOM_FILE_CAPTION Found, Default captions of file will be used.\n")
LOG_STR += (f"MAX_LIST_ELM Found, long list will be shortened to first {MAX_LIST_ELM} elements\n" if MAX_LIST_ELM else "Full List of casts and crew will be shown in imdb template, restrict them by adding a value to MAX_LIST_ELM\n")
