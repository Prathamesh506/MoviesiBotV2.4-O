import re
import ast
import math
import imdb
import html
import imdb
import regex
import psutil
import asyncio
import logging
import pyrogram
from datetime import datetime,timedelta
from info import OWNER_USERNAME
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters, enums
from pyrogram.errors import MessageNotModified
from fuzzywuzzy import fuzz, process
from Script import script
from plugins.iwatch import watch_movies_filter
from utils import get_size, is_subscribed, temp, check_verification, get_token
from info import ADMINS, AUTH_CHANNEL, NO_RES_CNL,GRP_LINK, CUSTOM_FILE_CAPTION, IS_VERIFY, HOW_TO_VERIFY, DLT,PROTECT_CONTENT,UPIQRPIC
from database.users_chats_db import db
from database.watch import store_movies_from_text,does_movie_exxists,search_movie_db
from database.ia_filterdb import Media, get_file_details,search_db,send_filex

lock = asyncio.Lock()
ia = imdb.IMDb()

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTONS = {}
SPELL_CHECK = {}


@Client.on_message((filters.group | filters.private) & filters.text & filters.incoming)
async def auto_filter(client, msg):
    await msg.reply_text("<b>We’ve Moved to: @Scarleti2Bot</b>")
    return
