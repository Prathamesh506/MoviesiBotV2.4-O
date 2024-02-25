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


#BOT
SESSION = environ.get('SESSION', 'MoviesiBotV4') #Bot name
API_ID = "3704207"
API_HASH = environ.get("API_HASH", "8d20e46f5413139329f2ec753f7c482a")
BOT_TOKEN = environ.get("BOT_TOKEN", "6583753281:AAFtg5TYcGEToa99k0hbOYrrkZXJIXWQXHk")

#ADMINS & DB CHANNEL IDS
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '1531899507').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1001997311406 -1001908988097 -1001977939308 -1002052107035 -1002031777198 -1002120266966').split()] #DATABASE
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002131280557')) #LOG CHANNEL

#PAYMENTS AND VERIFICATION INFO
UPI_ID = "mrnova@hdfcbank"
OWNER_USERNAME ="Shadow506"

#CHANNLS
GRP_LINK = environ.get('GRP1', 'https://t.me/+T7Q3qsiyv9cxOGM1') 
GRP1 = environ.get('GRP1', 'https://t.me/+T7Q3qsiyv9cxOGM1') 
GRP2 = environ.get('GRP2', 'https://t.me/+3evIddbYTPZiMDU9')
SUP_LNK = environ.get('SUP_LNK', 'https://t.me/TeamiVeGa') #support
CHNL_LNK = environ.get('CHNL_LNK', 'https://t.me/Vegalatest') #main Channel
UPDATES = "CineArcade"
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'TeamiVeGa') #ignore
auth_channel = "-1002086574998" #FOECE SUB CHANNEL
# auth_channel = environ.get('AUTH_CHANNEL')
auth_grp = environ.get('AUTH_GROUP') #FOECE SUB GROUP
SEARCH_B = "https://t.me/VegaMoviesXBot" #bot username
SEARCH_G = "https://t.me/+T7Q3qsiyv9cxOGM1" # group link 
MOV_REQ = environ.get('MOV_REQ', 'https://t.me/TeamiVeGa') #support
NO_RES_CNL = int(environ.get('LOG_CHANNEL', '-1002137535594')) #NO RESULT CHANNEL

support_chat_id = environ.get('support_chat_id',"-1002044884739")
reqst_channel = environ.get('reqst_channel',"-1002069948824")
REQST_CHANNEL = int(reqst_channel) if reqst_channel and id_pattern.search(reqst_channel) else None
SUPPORT_CHAT_ID = int(support_chat_id) if support_chat_id and id_pattern.search(support_chat_id) else None  


AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None

PICS = (environ.get('PICS', 'https://telegra.ph/file/96aa21c66eec5a24b9644.jpg https://telegra.ph/file/84bd10861f905d72adcaf.jpg https://telegra.ph/file/d315eaa802cdb2f790a5a.jpg https://telegra.ph/file/a25ea7f7a746ac1c544e3.jpg https://telegra.ph/file/40d555da9059bb1b0fcd7.jpg https://telegra.ph/file/2efd3b607301d692a634b.jpg https://telegra.ph/file/6e66b7dd8b9b30ace0f93.jpg https://telegra.ph/file/a320d989754c8dea12b02.png')).split()
NOR_IMG = environ.get("NOR_IMG", "https://telegra.ph/file/46443096bc6895c74a716.jpg")
MELCOW_VID = environ.get("MELCOW_VID", "https://telegra.ph/file/406961f53ed2b6f3735c4.gif")
SPELL_IMG = environ.get("SPELL_IMG", "https://telegra.ph/file/5e2d4418525832bc9a1b9.jpg")
IMDB_IMG = environ.get("IMDB_IMG", "https://telegra.ph/file/4b873b46bb4861f78ce6d.jpg")

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://MoviesiBotV6:MoviesiBotV5@cluster0.zs9smub.mongodb.net/?retryWrites=true&w=majority")
DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'MoviesiBotV4')

#SHORTNER
IS_VERIFY = is_enabled((environ.get('IS_VERIFY', 'True')), True)
SHORTLINKS = is_enabled((environ.get('SHORTLINKS', 'False')), False)

DOWNLOAD_TIPS = environ.get('HOW_TO_VERIFY', "https://t.me/Vegalatest/15")
HOW_TO_VERIFY = environ.get('HOW_TO_VERIFY', "https://t.me/Vegalatest/12")

SHORTLINK_URL = environ.get('SHORTLINK_URL', 'easysky.in')
SHORTLINK_API = environ.get('SHORTLINK_API', 'a1a45bfd3be9e758537846a3617b24c5d8be7d34')
SHORTLINK_URL_BKUP = environ.get('SHORTLINK_URL_BKUP', 'tnshort.net')
SHORTLINK_API_BKUP = environ.get('SHORTLINK_API_BKUP',"5b8c9497bbeabea5a30c16062eeba6b3fe6bbd13")
IS_SHORTLINK = is_enabled((environ.get('IS_SHORTLINK', 'False')), False)
DELETE_CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1001997311406 -1001908988097 -1001977939308 -1002052107035 -1002031777198 -1002120266966').split()] 

#BOT SETTINGS
DLT = int(environ.get('DLT', 600))
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", f"{script.CAPTION}")
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "False")), False)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), False)
PORT = environ.get("PORT", "8080")

LOG_STR = "Current Cusomized Configurations are:-\n"
LOG_STR += ("IMDB Results are enabled, Bot will be showing imdb details for you queries.\n" if IMDB else "IMBD Results are disabled.\n")
LOG_STR += ("P_TTI_SHOW_OFF found , Users will be redirected to send /start to Bot PM instead of sending file file directly\n" if P_TTI_SHOW_OFF else "P_TTI_SHOW_OFF is disabled files will be send in PM, instead of sending start.\n")
LOG_STR += (f"CUSTOM_FILE_CAPTION enabled with value {CUSTOM_FILE_CAPTION}, your files will be send along with this customized caption.\n" if CUSTOM_FILE_CAPTION else "No CUSTOM_FILE_CAPTION Found, Default captions of file will be used.\n")
LOG_STR += (f"MAX_LIST_ELM Found, long list will be shortened to first {MAX_LIST_ELM} elements\n" if MAX_LIST_ELM else "Full List of casts and crew will be shown in imdb template, restrict them by adding a value to MAX_LIST_ELM\n")
