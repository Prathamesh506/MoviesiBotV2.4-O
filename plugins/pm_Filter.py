import re
import ast
import math
import imdb
import html
import copy 
import time
import imdb
import regex
import psutil
import random
import asyncio
import logging
import pyrogram

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters, enums
from pyrogram.errors import UserIsBlocked, MessageNotModified, PeerIdInvalid
from fuzzywuzzy import fuzz, process

from Script import script
from plugins.iwatch import watch_movies_filter
from utils import get_size, is_subscribed, temp, check_verification, get_token
from info import ADMINS, AUTH_CHANNEL, NO_RES_CNL,GRP_LINK,SUPPORT_CHAT_ID,DOWNLOAD_TIPS, CUSTOM_FILE_CAPTION, IS_VERIFY, HOW_TO_VERIFY, DLT,IMDB_IMG,PROTECT_CONTENT
from database.users_chats_db import db
from database.watch import store_movies_from_text,does_movie_exxists,search_movie_db,get_watch_movies
from database.ia_filterdb import Media, get_file_details,search_db,total_results_count,send_filex

lock = asyncio.Lock()
ia = imdb.IMDb()

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTONS = {}
SPELL_CHECK = {}
CATCH_TIME = DLT

@Client.on_message((filters.group | filters.private) & filters.text & filters.incoming)
async def message_filter(client, message):

    if message.text is None or message.text.startswith(("/", "#")):
        return
    
    if message.chat.id == SUPPORT_CHAT_ID:
        await support_grp_filter(message)
        return
    
    await auto_filter(client, message)

#SUPPORT FILTER
async def support_grp_filter(msg):
    try:
        search = await process_text(msg.text)
        total_results = await total_results_count(search)
        
        if total_results:
            btn = [[InlineKeyboardButton('Movies Group 🍿', url=GRP_LINK)]]
            cap = f"<b>Hey {msg.from_user.mention},\n\nFound {total_results} Results\nSearch:</b> {search.title()}\n\n<i><b>NOTE: </b>To get the movies, please search in the movies group.</i>"
            result_msg = await msg.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
            await asyncio.sleep(DLT)
            await result_msg.delete()
            
    except Exception as e:
        logger.exception(f'ERROR: SUPPORT GROUP FILTER\n{str(e)}')
    return

#AUTO FILTER
async def auto_filter(client, msg):
    orgmsg = msg
    ptext = await process_text(msg.text)
    search_details, search = detail_extraction(ptext, type=True)
    popularty_search = search_details["title"]
    files = []

    if is_invalid_message(msg) or contains_url(msg.text):
        return

    as_msg = await msg.reply_text("<b>Searching..</b>")
    #BASED ON PRIVIOUS SEARCH FILTER ADD ON
    if not search_details['title'] and not search_details['year']:
        last_search = await db.retrieve_latest_search(msg.from_user.id)
        if last_search is None:
            await no_resultx(msg, text="<i>Provide a Correct Title❗</i>")
            return
        search = f"{last_search} {search}"
        search_details, search = detail_extraction(search)
        files, offset, total_pages = await search_db(search.lower(), offset=0)
        await as_msg.delete()
        if not files:
            await no_resultx(msg, text=f"<i>No Files Found in Database\n<b>For Your Search:</b> {search.title()}</i>")
            return
        await db.store_search(msg.from_user.id, search)
        
    #DIRECT SEARCH 
    else:
        files, offset, total_pages = await search_db(search.lower(), offset=0)
        if files:
            await db.store_search(msg.from_user.id, search)
            await as_msg.delete()

        #LOCAL AUTOCORRECT
        else:
            as_msg = await msg.edit_text("<b>Optimizing Search ⚡</b>")
            temp_detail = search_details.copy()
            temp_detail['title'] = await search_movie_db(temp_detail['title'].lower())
            if temp_detail['title'] is not None:
                temp_search = str_to_string(temp_detail)
                files, offset, total_pages = await search_db(temp_search.lower(), offset=0)
                if files:
                    search = temp_search
                    await db.store_search(msg.from_user.id, search)
                    await as_msg.delete()

            if not files:
                imdb_res_list = None
                try:
                    search_details['title'], imdb_res_list = await imdb_S1(search_details['title'].lower())
                    if search_details['title']:
                        search_details['title'] = await process_text(search_details['title'])
                        tempsearch = str_to_string(search_details)
                        files, offset, total_pages = await search_db(tempsearch.lower(), offset=0)
                        if files:
                            search = tempsearch
                            await as_msg.delete()
                            await db.store_search(msg.from_user.id, search)
                except Exception as e:
                    logger.exception(f'ERROR: #IMDB AUTOCORRECT \n{e}')
                    pass

    if files:
        btn = await result_btn(files, msg.from_user.id, client, search)
        btn = await navigation_buttons(btn, msg, total_pages, offset)
        cap = f"<b>Hey {msg.from_user.mention},\n\nFᴏᴜɴᴅ Rᴇꜱᴜʟᴛꜱ Fᴏʀ Yᴏᴜʀ\nSearch:</b> {search.title()}"
        result_msg = await msg.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
        await popularity_store(popularty_search)


    if not files:
        imdb_msg = await as_msg.edit_text("<b>Searching On IMDb..</b>")
        if not imdb_res_list:
            await imdb_msg.delete()
            await no_resultx(msg)
            return
        score_results = find_matching_movies(search_details['title'], imdb_res_list)
        if not score_results:
            await imdb_msg.delete()
            await no_resultx(msg)
            return
        await imdb_msg.delete()
        btn = imdb_btn(score_results, msg.from_user.id)
        cap = f"<b>Hey {msg.from_user.mention},\n\nHere Some Related Titles!</b>"
        result_msg = await msg.reply_photo(photo=IMDB_IMG, caption=cap,
                                           reply_markup=InlineKeyboardMarkup(btn))
    try:
        await asyncio.sleep(DLT)
        await result_msg.delete()
    except: pass

#TREANDING MOVIES
async def popularity_store(query):
    try:
        # Check if the movie exists in the database
        if await does_movie_exxists(query.lower()):
            movie = f"2,{query.lower()},trending,1"
            await store_movies_from_text(movie)
            return
    except Exception as e:
        print(f"ERROR 1: TRENDING MOVIES\n{e}")

    try:
        # Search for the movie on IMDb
        imdb_res_up = search_movie(query)
        imdb_res = await process_text(imdb_res_up[0]) if imdb_res_up else None
        
        if not imdb_res:
            return
        
        # Calculate similarity score between query and IMDb result
        score = fuzz.token_sort_ratio(query.lower(), imdb_res.lower())
        
        if score >= 95:
            input_str = f"2,{imdb_res.lower()},trending,1"
            await store_movies_from_text(input_str)
    except Exception as e:
        print(f"ERROR 2: TRENDING MOVIES\n{e}")
        return

#BUTTONS
async def result_btn(files, user_id, bot, search,text_mode=False):
    # Extract season
    season = extract_season(search) or "01"
    
    # Check verification asynchronously
    is_verified = await check_verification(bot, user_id)
    
    # Determine if batch button should be shown
    batch_btn = any(re.search(r'\bs\d+', html.unescape(file.caption), re.IGNORECASE) for file in files)
    
    # Construct basic button structure
    if not text_mode:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] {html.unescape(file.caption[:45].strip())}",
                    url=f"https://telegram.dog/{temp.U_NAME}?start=CodeiBots_{file.file_id}"
                ),
            ]        
            for file in files
        ]
    else: btn = []
    # Construct URL for batch files
    link = f"https://telegram.me/{temp.U_NAME}?start="
    batch_url = f"{link}all_eps_files-{user_id}"
    
    # Add appropriate buttons based on conditions
    additional_btns = []
    if not is_verified and not batch_btn:
        additional_btns.append([
            InlineKeyboardButton('Hᴏᴡ Tᴏ Vᴇʀɪғʏ & Dᴏᴡɴʟᴏᴀᴅ ? 🤔', url=HOW_TO_VERIFY)
        ])
    
    if batch_btn:
        additional_btns.append([
            InlineKeyboardButton(f'📂 S{season} Bᴀᴛᴄʜ', url=batch_url),
            InlineKeyboardButton("Hᴏᴡ Tᴏ Dᴏᴡɴʟᴏᴀᴅ ?", url=HOW_TO_VERIFY) if not is_verified else
            InlineKeyboardButton("Sᴇᴀʀᴄʜ Tɪᴘs", url=DOWNLOAD_TIPS)
        ])
    
    # Insert additional buttons at the beginning of btn list
    btn = additional_btns + btn
    
    # Insert common buttons at the beginning
    common_btns = [
        [
            InlineKeyboardButton("Lᴀɴɢᴜᴀɢᴇ", callback_data=f"select_language#{user_id}#{text_mode}"),
            InlineKeyboardButton("Qᴜᴀʟɪᴛʏ", callback_data=f"select_quality#{user_id}#{text_mode}"),
            InlineKeyboardButton("Sᴇᴀꜱᴏɴ", callback_data=f"select_season#{user_id}#{text_mode}")
        ]
    ]
    btn = common_btns + btn
    
    return btn

async def result_text(files, cap):
    for file in files:
        text = f"[{get_size(file.file_size)}] {html.unescape(file.caption[:65].strip())}"
        url = f"https://telegram.dog/{temp.U_NAME}?start=CodeiBots_{file.file_id}"
        cap += f"<b>\n\n📂 <a href={url}>{text}</a></b>"
    return cap

async def navigation_buttons(btn,message, total_pages, offset,Text_mode=False):#navigation btns
    req = message.from_user.id if message.from_user else 0
    offset = int(offset)
    mode = "ʙᴛɴ" if Text_mode else "ᴛᴇxᴛ"
    offsetpageno = int(math.ceil(int(offset)/10))
    if total_pages == 1 :
        btn.append([
            InlineKeyboardButton(text=f"⚙️ {mode}",callback_data=f"text_mode#{req}#{offset}#{Text_mode}"),
            InlineKeyboardButton(text=f" 1 / {total_pages}",callback_data="callback_none")]
        )
    elif offsetpageno == total_pages :
        btn.append([
            InlineKeyboardButton(text="⌫ ʙᴀᴄᴋ",callback_data=f"next_{req}_{offset-20}_{Text_mode}"),
            InlineKeyboardButton(text=f" {offsetpageno} / {total_pages}",callback_data="callback_none")]
        )
    elif offset == 10 :
        btn.append([
            InlineKeyboardButton(text=f"⚙️ {mode}",callback_data=f"text_mode#{req}#{offset}#{Text_mode}"),
            InlineKeyboardButton(text=f" 1 / {total_pages}",callback_data="callback_none"),
            InlineKeyboardButton(text="ɴᴇxᴛ ⌦ ",callback_data=f"next_{req}_{offset}_{Text_mode}")]
        )
    else:
        btn.append([
            InlineKeyboardButton(text="⌫ ʙᴀᴄᴋ",callback_data=f"next_{req}_{offset-20}_{Text_mode}"),
            InlineKeyboardButton(text=f"{offsetpageno} / {total_pages}",callback_data="callback_none"),
            InlineKeyboardButton(text="ɴᴇxᴛ ⌦",callback_data=f"next_{req}_{offset}_{Text_mode}") ]
        )  
    
    return btn

def imdb_btn(results, user_id):#IMDB result btns
    keyboard = []
    results  = [movie.title() for movie in results]
    for i, movie in enumerate(results):
        trimmed_movie_name = movie[:30] 
        button_data = f"add_filter#{user_id}#mainpage#{trimmed_movie_name}"
        button = InlineKeyboardButton(text=movie, callback_data=button_data)
        keyboard.append([button])
    keyboard.append([
        InlineKeyboardButton(text="Close", callback_data=f"close_data#{user_id}")
    ])
    return keyboard

@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    try:
        _, req, offset,tm = query.data.split("_")
        text_mode = True if tm == "True" else False
        offset = int(offset)
        req = int(req)

        search = await db.retrieve_latest_search(query.from_user.id)

        if req != query.from_user.id:
            return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
        
    except ValueError:
        logger.exception('ERROR: #NEXT BUTTON')
        return 
    
    try:
        offset = int(offset)
    except ValueError:
        offset = 0

    if not search:
        await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name), show_alert=True)
        return

    files, n_offset, total_pages = await search_db(search, offset)

    if not files:
        return

    btn = await result_btn(files, req, bot, search,text_mode)
    query.text = search
    btn = await navigation_buttons(btn, query, total_pages, n_offset,text_mode)
    try:
        if not text_mode:
            await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btn))
        else:
            cap = f"<b>Hey {query.from_user.mention},\n\nFᴏᴜɴᴅ Rᴇꜱᴜʟᴛꜱ Fᴏʀ Yᴏᴜʀ\nSearch: </b>{search.title()}"
            cap = await result_text(files,cap)
            result_msg = await query.message.edit_text(cap, reply_markup=InlineKeyboardMarkup(btn))
    except pyrogram.errors.exceptions.flood_420.FloodWait as e:
        await query.answer("Flood Wait 15s ⌛")
    except pyrogram.errors.exceptions.bad_request_400.QueryIdInvalid as e:
        logger.error("Query ID is invalid or expired.")
        return  # Don't proceed further if the query ID is invalid
    except MessageNotModified:
        pass
    await query.answer()

@Client.on_callback_query(filters.regex(r"^select_lang"))
async def select_language(bot, query):
    _, userid,tm= query.data.split("#")
    text_mode = True if tm == "True" else False
    if int(userid) not in [query.from_user.id, 0]:
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    btn = [[
        InlineKeyboardButton("⇃  ᴄʜᴏᴏsᴇ ʟᴀɴɢᴜᴀɢᴇ  ⇂", callback_data=f"callback_none")
    ],[
        InlineKeyboardButton("Eɴɢʟɪꜱʜ", callback_data=f"add_filter#{userid}#english#{text_mode}"),
        InlineKeyboardButton("Hɪɴᴅɪ", callback_data=f"add_filter#{userid}#hindi#{text_mode}")
    ],[
        InlineKeyboardButton("Tᴀᴍɪʟ", callback_data=f"add_filter#{userid}#tamil#{text_mode}"),
        InlineKeyboardButton("Tᴇʟᴜɢᴜ", callback_data=f"add_filter#{userid}#telugu#{text_mode}")
    ],[
        InlineKeyboardButton("Mᴀʀᴀᴛʜɪ", callback_data=f"add_filter#{userid}#mar#{text_mode}"),
        InlineKeyboardButton("Mᴀʟᴀʏᴀʟᴀᴍ", callback_data=f"add_filter#{userid}#mal#{text_mode}")
    ],[
        InlineKeyboardButton("Kᴀɴɴᴀᴅᴀ", callback_data=f"add_filter#{userid}#kan#{text_mode}"),
        InlineKeyboardButton("Dᴜᴀʟ Aᴜᴅɪᴏ", callback_data=f"add_filter#{userid}#dual#{text_mode}")
    ],[
        InlineKeyboardButton("Mᴜʟᴛɪ Aᴜᴅɪᴏ", callback_data=f"add_filter#{userid}#multi#{text_mode}"),
        InlineKeyboardButton("ꜱᴜʙᴛɪᴛʟᴇꜱ", callback_data=f"add_filter#{userid}#sub#{text_mode}")
    ],[
        InlineKeyboardButton("Cʟᴇᴀʀ", callback_data=f"add_filter#{userid}#clearlanguage#{text_mode}"),
        InlineKeyboardButton("Bᴀᴄᴋ", callback_data=f"add_filter#{userid}#mainpage#{text_mode}")
    ]]
    try:
        cap = f"<b>Hey {query.from_user.mention},\n\nSᴇʟᴇᴄᴛ Aɴ Lᴀɴɢᴜᴀɢᴇ:</b>"
        await query.message.edit_text(text = cap,
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()
    
@Client.on_callback_query(filters.regex(r"^select_quality"))
async def select_quality(bot, query):
    _, userid,tm= query.data.split("#")
    text_mode = True if tm == "True" else False
    if int(userid) not in [query.from_user.id, 0]:
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    cap = f"<b>Hey {query.from_user.mention},\n\nSᴇʟᴇᴄᴛ Aɴ Qᴜᴀʟɪᴛʏ:</b>"
    btn = [[
        InlineKeyboardButton("⇃  ᴄʜᴏᴏsᴇ ϙᴜᴀʟɪᴛʏ  ⇂", callback_data=f"callback_none")
    ],[
        InlineKeyboardButton("HD/Rips", callback_data=f"add_filter#{userid}#rip#{text_mode}"),
        InlineKeyboardButton("360P", callback_data=f"add_filter#{userid}#360p#{text_mode}")
    ],[
        InlineKeyboardButton("480P", callback_data=f"add_filter#{userid}#480p#{text_mode}"),
        InlineKeyboardButton("720P", callback_data=f"add_filter#{userid}#720p#{text_mode}")
    ],[
        InlineKeyboardButton("1080P", callback_data=f"add_filter#{userid}#1080p#{text_mode}"),
        InlineKeyboardButton("4K", callback_data=f"add_filter#{userid}#4k#{text_mode}")
    ],[
        InlineKeyboardButton("Clear", callback_data=f"add_filter#{userid}#clearquality#{text_mode}"),
        InlineKeyboardButton("Back", callback_data=f"add_filter#{userid}#mainpage#{text_mode}")
    ]]
    try:
        await query.message.edit_text(text = cap,
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()

@Client.on_callback_query(filters.regex(r"^select_season"))
async def select_season(bot, query):
    _, userid,tm= query.data.split("#")
    text_mode = True if tm == "True" else False
    if int(userid) not in [query.from_user.id, 0]:
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    btn = [[
        InlineKeyboardButton("⇃  ᴄʜᴏᴏsᴇ ꜱᴇᴀꜱᴏɴ  ⇂", callback_data=f"callback_none")
    ],[
        InlineKeyboardButton("Season 01", callback_data=f"add_filter#{userid}#s01#{text_mode}"),
        InlineKeyboardButton("Season 02", callback_data=f"add_filter#{userid}#s02#{text_mode}")
    ],[
        InlineKeyboardButton("Season 03", callback_data=f"add_filter#{userid}#s03#{text_mode}"), 
        InlineKeyboardButton("Season 04", callback_data=f"add_filter#{userid}#s04#{text_mode}")
    ],[
        InlineKeyboardButton("Season 05", callback_data=f"add_filter#{userid}#s05#{text_mode}"),
        InlineKeyboardButton("Season 06", callback_data=f"add_filter#{userid}#s06#{text_mode}")
    ],[
        InlineKeyboardButton("Season 07", callback_data=f"add_filter#{userid}#s07#{text_mode}"), 
        InlineKeyboardButton("Season 08", callback_data=f"add_filter#{userid}#s08#{text_mode}")
    ],[
        InlineKeyboardButton("Season 09", callback_data=f"add_filter#{userid}#s09#{text_mode}"),
        InlineKeyboardButton("Season 10", callback_data=f"add_filter#{userid}#s10#{text_mode}")
    ],[
        InlineKeyboardButton("Season 11", callback_data=f"add_filter#{userid}#s11#{text_mode}"), 
        InlineKeyboardButton("Season 12", callback_data=f"add_filter#{userid}#s12#{text_mode}")
    ],[
        InlineKeyboardButton("Clear", callback_data=f"add_filter#{userid}#clearseason#{text_mode}"),
        InlineKeyboardButton("Back", callback_data=f"add_filter#{userid}#mainpage#{text_mode}")
    ]]
    try:
        cap = f"<b>Hey {query.from_user.mention},\n\nSᴇʟᴇᴄᴛ Aɴ Sᴇᴀꜱᴏɴ:</b>"
        await query.message.edit_text(text = cap,
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()

@Client.on_callback_query(filters.regex(r"^add_filter"))
async def filtering_results(bot, query): 
    user_id = query.from_user.id
    data_parts = query.data.split("#")
    text_mode = False
    if len(data_parts) == 4 and data_parts[3] not in ["True","False"]: #IMDB RESULT
        _, userid, the_filter, search = data_parts
        search = await process_text(search)
    else:
        _, userid, the_filter,tm = data_parts
        text_mode = True if tm == "True" else False
        if the_filter == "imdbclse":
            await query.answer(f"🤖 Closing IMDb Results")
            await query.message.delete()
            
        search = await db.retrieve_latest_search(user_id)

    if int(userid) != user_id:
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)

    if not search:
        return await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    
    if the_filter in ["clearlanguage", "clearquality", "clearseason"]:
        search = clear_filter(search, the_filter)
    elif the_filter != "mainpage":
        search = f"{search} {the_filter}"
        details, search = detail_extraction(search)

    files, offset, total_pages = await search_db(search, offset=0)

    query.text = search
    if files:
        await db.store_search(user_id, search)
        btn = await result_btn(files, user_id,bot,search,text_mode)
        btn = await navigation_buttons(btn, query, total_pages, offset,text_mode)
        try:
            cap = f"<b>Hey {query.from_user.mention},\n\nFᴏᴜɴᴅ Rᴇꜱᴜʟᴛꜱ Fᴏʀ Yᴏᴜʀ\nSearch: </b>{search.title()}"
            if text_mode:
                cap = await result_text(files,cap)
            if len(data_parts) == 4 and data_parts[3] not in ["True","False"]:
                await query.answer(f"🤖 Fetching Results")
                await query.message.delete()
                result_msg = await query.message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
                await asyncio.sleep(DLT)
                await result_msg.delete()
            else:
                await query.edit_message_text(
                    text=cap,
                    reply_markup=InlineKeyboardMarkup(btn)
                )
                if the_filter in ["clearlanguage", "clearquality", "clearseason"]:
                    await query.answer(f"🤖 Removed {the_filter[5:].title()} Filter")
                elif the_filter != "mainpage":
                    await query.answer(f"🤖 Results For : {the_filter.title()}")
        except MessageNotModified:
            pass
    else:
        if len(data_parts) == 4:
            await bot.send_message(chat_id=NO_RES_CNL, text=f"<b>iMDb:</b> <code>{search}</code>")
        return await query.answer(f"No Files Found In database For Your Query. 🔍", show_alert=True)

@Client.on_callback_query(filters.regex(r"^text_mode"))
async def add_Text_mode(bot, query): 
    user_id = query.from_user.id
    data_parts = query.data.split("#")
    _, userid, offset ,tm= data_parts
    text_mode = not (True if tm == "True" else False)
    search = await db.retrieve_latest_search(user_id)

    if int(userid) != user_id:
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)

    if not search:
        return await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    

    files, offset, total_pages = await search_db(search, offset=int(offset)-10)

    query.text = search

    if files:
        await db.store_search(user_id, search)
        btn = await result_btn(files, user_id,bot,search,text_mode=text_mode)
        btn = await navigation_buttons(btn, query, total_pages, offset,text_mode)
        try:
            cap = f"<b>Hey {query.from_user.mention},\n\nFᴏᴜɴᴅ Rᴇꜱᴜʟᴛꜱ Fᴏʀ Yᴏᴜʀ\nSearch: </b>{search.title()}"
            if text_mode:
                cap = await result_text(files,cap)
            result_msg = await query.message.edit_text(cap, reply_markup=InlineKeyboardMarkup(btn))
            await asyncio.sleep(DLT)
            await result_msg.delete()
        except MessageNotModified:
            pass
    else:
        return await query.answer(f"No Files Found In database For Your Query. 🔍", show_alert=True)

#UTILITY
async def process_text(text_caption): #text is filter and processed
    text_caption = text_caption.lower()

    # Remove emojis using regex module
    text_caption = regex.sub(r'\p{So}', '', text_caption)

    # Replace certain characters with spaces
    text_caption = re.sub(r"[@!$ _\-.+:*#⁓(),/?]", " ", text_caption)

    # Replace language abbreviations using a dictionary
    language_abbreviations = {"session":"season","hin": "hindi", "eng": "english", "tam": "tamil", "tel": "telugu","wanda vision":"wandavision","salar":"salaar","spiderman":"spider man","spiderverse":"spider verse","complete":"combined","12 th":"12th","completed":"combined","all episodes":"combined","all episode":"combined"}
    text_caption = re.sub(
        r"\b(?:session|hin|eng|tam|tel|wanda\s*vision|salar|spiderman|spiderverse|complete|12\s*th|completed|all\s*episodes|all\s*episode)\b",
        lambda match: language_abbreviations.get(match.group(0), match.group(0)),
        text_caption
    )

    # Insert space between 's' and 'e' in patterns like 's01e04'
    text_caption = re.sub(r's(\d+)e(\d+)', r's\1 e\2', text_caption, flags=re.IGNORECASE)

    # Insert space between 's' and 'e' in patterns like 's1e4'
    text_caption = re.sub(r's(\d+)e', r's\1 e', text_caption, flags=re.IGNORECASE)

    # Convert 'ep' followed by a number to 'e' followed by that number with leading zeros
    text_caption = re.sub(r'\bep(\d+)\b', r'e\1', text_caption, flags=re.IGNORECASE)
    text_caption = re.sub(r'\bep (\d)\b', r'e0\1', text_caption, flags=re.IGNORECASE)
    text_caption = re.sub(r'\bep (\d{2,})\b', r'e\1', text_caption, flags=re.IGNORECASE)

        # Convert single-digit 'e' to two-digit 'e'
    text_caption = re.sub(r'\be(\d)\b', r'e0\1', text_caption, flags=re.IGNORECASE)

    # Convert single-digit 's' to two-digit 's'
    text_caption = re.sub(r'\bs(\d)\b', r's0\1', text_caption, flags=re.IGNORECASE)

    # Formatting for season and episode numbers (padding with zeros)
    text_caption = re.sub(r'\bseason (\d+)\b', lambda x: f's{x.group(1).zfill(2)}', text_caption, flags=re.IGNORECASE)
    text_caption = re.sub(r'\bepisode (\d+)\b', lambda x: f'e{x.group(1).zfill(2)}', text_caption, flags=re.IGNORECASE)

    #testing
    text_caption = ' '.join(['e' + word[2:] if word.startswith('e0') and word[2:].isdigit() and len(word) >= 4 else word for word in text_caption.split()])

    words_to_remove = ["full","video","videos","movie", "movies","series","dubbed","send","file","audio","to","language","quality","qua","aud","give","files","hd","in","dub","review"]

    # Create a regular expression pattern with all words to remove
    pattern = r'\b(?:' + '|'.join(re.escape(word) for word in words_to_remove) + r')\b'

    # Remove the specified words in a case-insensitive manner
    text_caption = re.sub(pattern, '', text_caption, flags=re.IGNORECASE)

    # Remove extra spaces between words
    text_caption = re.sub(r'\s+', ' ', text_caption)
    
    return text_caption

def detail_extraction(text,type=False): #extractes details title ans all

    languages = ["english", "hindi", "tamil", "telugu", "kannada", "malayalam", "marathi", "multi", "dual","kan","mal","mar"]
    qualities = ["720p", "1080p", "480p", "4k", "360p","rip","hd"]
    subs = ["sub", "esub", "msub", "esubs", "msubs"]
    extra_words = ["combined"]

    # Define patterns for 's01', 'e01', 'part 1', and a four-digit number (year)
    season_pattern = re.compile(r'\bs\d+', re.IGNORECASE)
    episode_pattern = re.compile(r'\be\d+', re.IGNORECASE)
    # part_pattern = re.compile(r'part\s*(\d+)', re.IGNORECASE)
    year_pattern = re.compile(r'\b\d{4}\b')

    details = {
        'title': text,
        'year': None,
        'season': None,
        'episode': None,
        'language': None,
        'quality': None,
        'sub': None,
        'comb':None
    }

    # Extract patterns for language
    if type:
        found_languages = []
        for word in text.split():
            if word in languages:
                found_languages.append(word)

        if found_languages:
            details['language'] = ' '.join(found_languages)
        else:
            details['language'] = None
            
    else: #only one lang
        for word in text.split():
            for lang in languages:
                if lang == word:
                    details['language'] = lang

    # Extract patterns for quality
    for word in text.split():
        for quality in qualities:
            if quality == word:
                details['quality'] = quality

    # Extract patterns for subtitles
    for word in text.split():
        for sub in subs:
            if sub == word:
                details['sub'] = sub

    # Extract pattern for year
    match_year = year_pattern.search(text)
    if match_year:
        details['year'] = match_year.group()
        details['title'] = re.sub(year_pattern, '', details['title']).strip()

    # Extract patterns for season
    match_season = season_pattern.findall(text)
    if match_season:
        details['season'] = match_season[-1]
        details['title'] = re.sub(season_pattern, '', details['title']).strip()

    # Extract patterns for episode
    match_episode = episode_pattern.findall(text)
    if match_episode:
        details['episode'] = match_episode[-1]
        details['title'] = re.sub(episode_pattern, '', details['title']).strip()

     # Extract 'combined'
    details['comb'] = "combined" if "combined" in text.lower() else None

    # Remove all qualities, subtitles, year, and other languages from the title
    for term in qualities + subs + languages + extra_words:
        matches = re.findall(r'\b(?:{})\b'.format(term), details['title'])
        if matches:
            details['title'] = re.sub(r'\b(?:{})\b'.format(term), '', details['title']).strip()
    formatted_info = ' '.join(str(value) for value in details.values() if value is not None)
    formatted_info = formatted_info.replace("'", '').replace('{', '').replace('}', '')
    # Remove extra spaces between words
    formatted_info = re.sub(r'\s+', ' ', formatted_info)
    return details , formatted_info

def is_invalid_message(msg): #checks if the message is invalid ?
    if len(msg.text) < 2 or re.match(r'^\s*$', msg.text) or \
            re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", msg.text) or \
            len(msg.text) > 100:
        return True
    return False

async def no_resultx(msg,text="<i>No Results Found Please Provide Correct Title!</i>"):#no result message
    k = await msg.reply_text(f"{text}")
    await asyncio.sleep(7)
    await k.delete()
    return

async def imdb_S1(search):
    try:
        imdb_list = search_movie(search)

        if not imdb_list:
            return None, None

        imdb_list = [await process_text(str(movie)) for movie in imdb_list]
        imdb_list = list(set(imdb_list))
        match_movie, score = process.extractOne(search.lower(), imdb_list)
        if int(score) >= 75:
            return match_movie, imdb_list
        else:
            return None, imdb_list

    except Exception as e:
        return None ,None
    
def search_movie(query, results=10):
    try:
        query = query.strip().lower()
        movie_ids = ia.search_movie(query, results)

        filtered_results = []
        for movie in movie_ids:
            if movie.get('kind') in ['movie', 'tv series', 'anime']:
                filtered_results.append(movie['title'])

        return filtered_results
    except imdb.IMDbDataAccessError as e:
        print("Error accessing IMDb data:", e)
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None
        
def find_matching_movies(input_name, movie_list):
    try:
        matches = process.extract(input_name, movie_list, scorer=fuzz.ratio, limit=5)
        threshold = 30
        filtered_matches = [name for name, score in matches if score >= threshold]
        return filtered_matches
    except Exception as e:
        print(f"Error finding matching movies: {e}")
        return []

def clear_filter(search, the_filter): #function clear a type of filter
    deatails, search = detail_extraction(search)
    
    if the_filter == "clearlanguage":
        deatails['language'] = None
        deatails['sub'] = None
    elif the_filter == "clearquality":
        deatails['quality'] = None
    elif the_filter == "clearseason":
        deatails['season'] = None

    search = str_to_string(deatails)
    return search

def str_to_string(details): #converts from structure deatils to string
    formatted_info = ' '.join(str(value) for value in details.values() if value is not None)
    formatted_info = formatted_info.replace("'", '').replace('{', '').replace('}', '')
    return formatted_info

def extract_season(text):
    season_pattern = re.compile(r'\bs(\d+)', re.IGNORECASE)
    
    match_season = season_pattern.search(text)
    
    if match_season:
        return match_season.group(1)
    else:
        return None

async def loading_msg(query):
    await asyncio.sleep(0.1)
    await query.edit_message_text(
                text="▰▱▱"
            )
    await asyncio.sleep(0.1)
    await query.edit_message_text(
                text="▰▰▱"
            )
    await asyncio.sleep(0.08)
    await query.edit_message_text(
                text="▰▰▰"
            )

def contains_url(message):
    url_pattern = re.compile(r'https?://\S+')
    match = re.search(url_pattern, message)
    return bool(match)

async def send_eps_files(user_id, query, client, message):
    try:
        details, search = detail_extraction(query)
        if not details['season']:
            details['season'] = "s01"
        details['comb'] = None
        details['episode'] = None
        search = str_to_string(details)

        if search is None:
            await message.reply_text("<b>No search terms provided</b>")
            return

        # Start with a loading message
        wait_msg = await message.reply_text("<b>Fetching Files...</b>")

        # Simulate fetching files with a loading animation
        for _ in range(1):
            await asyncio.sleep(0.5)
            await wait_msg.edit_text("<b>Fetching Files.</b>")
            await asyncio.sleep(0.5)
            await wait_msg.edit_text("<b>Fetching Files..</b>")
            await asyncio.sleep(0.5)
            await wait_msg.edit_text("<b>Fetching Files...</b>")

        # Update message to indicate uploading
        await wait_msg.edit_text("<b>Uploading...</b>")
        await asyncio.sleep(1)
        await wait_msg.delete()

        for i in range(1, 26):
            query_ep = f"{search} e0{i}" if i < 10 else f"{search} e{i}"

            if not await send_filex(query_ep, user_id, client):
                if i == 1:
                    await wait_msg.edit_text("<b>No files found</b>")
                    return
                break

        comb = await message.reply_text("<b>Searching for Combined File..</b>")
        await asyncio.sleep(2)

        query_comn = f"{search} combined"
        if details['quality']:
            suc = await send_filex(query_comn, user_id, client)
            if not suc:
                details['quality'] = None
                query_comn = str_to_string(details)
                suc = await send_filex(query_comn, user_id, client)
        else:
            suc = await send_filex(query_comn, user_id, client)
        if not suc:
            await comb.edit_text("<b>No Combined File Found.</b>")
            await asyncio.sleep(1)
        await comb.delete()
        await asyncio.sleep(1)
        await comb.reply_text("<i><b>Note:</b> This feature is in <b>Beta Stage</b>\nYou might receive wrong files</i>")

    except Exception as e:
        logging.error(f"Exception in send_eps_files: {e}")
        await message.reply_text("<b>Error occurred while fetching files. Please try again later.</b>")

async def verify_msg(query, client,file_id):
    pw_msg = await query.message.reply_text("Pʟᴇᴀsᴇ Wᴀɪᴛ..")
    btn = [[
        InlineKeyboardButton("Vᴇʀɪғʏ", url=await get_token(client, query.from_user.id, f"https://telegram.me/{temp.U_NAME}?start=", file_id)),
        InlineKeyboardButton("Hᴏᴡ Tᴏ Vᴇʀɪғʏ", url=HOW_TO_VERIFY)
    ]]
    await pw_msg.delete()
    verify_btn = await query.message.reply_text(
        text="<b>Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴠᴇʀɪғɪᴇᴅ!\nKɪɴᴅʟʏ ᴠᴇʀɪғʏ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ Sᴏ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ ɢᴇᴛ ᴀᴄᴄᴇss ᴛᴏ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇs ᴜɴᴛɪʟ 16 ʜᴏᴜʀs ғʀᴏᴍ ɴᴏᴡ !</b>\n<i>or just buy /premium Membership</i>",
        protect_content=False,
        reply_markup=InlineKeyboardMarkup(btn)
    )
    await asyncio.sleep(DLT)
    await verify_btn.delete()
    return

#CALLBACKS 
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    
    if query.data == "callback_none":
        await query.answer() 

    if query.data.startswith("close_data"): 
        _,userid = query.data.split("#")
        try:
            if int(userid) != int(query.from_user.id):
                await query.answer("It's Not Your Request", show_alert=True)
                return
            await query.message.delete()
        except: pass
        return

    if query.data =="back_watch":
        await watch_movies_filter(client,query,True)
        return
    
    if query.data =="back_watch_start":
        await loading_msg(query)
        await watch_movies_filter(client,query,True,True)
        return
    
    if query.data.startswith("req_oprt"):
        _, type_op, requester_id, req_cont = query.data.split("#")
        if type_op == "req_pstd" and query.from_user.id in ADMINS:
            cap = f"<i>Your requested movie, {req_cont} is now available in Bot</i>"
            await client.send_message(chat_id=int(requester_id), text=cap)
            btn = []
            btn.insert(0, [
                InlineKeyboardButton('Uploded ✅', callback_data='callback_none'),
            ])
            await query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(btn))
        elif query.from_user.id in ADMINS:
            cap = f"<i>hey, Your Request for {req_cont} is Declined, requested movie isn't available or the requested formate is incorrect</i>"
            try:
                await client.send_message(chat_id=int(requester_id), text=cap)
            except Exception as e:
                await query.message(f"error: {e}")
            await query.message.delete() 
        else:
            await query.answer()    
        return

    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("Tʜᴀᴛ's ɴᴏᴛ ғᴏʀ ʏᴏᴜ!!", show_alert=True)

    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await None, None, None, None
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)
    
    elif query.data.startswith("checksub"):
        if AUTH_CHANNEL and not await is_subscribed(client, query):
            await query.answer("First Join My Channel", show_alert=True)
            return
        
        await query.message.delete()

        ident, file_id = query.data.split("#")

        if file_id.startswith("eps_files"):
            if IS_VERIFY and not await check_verification(client, query.from_user.id):
                await verify_msg(query,client,"all_eps")
            else: 
                search = await db.retrieve_latest_search(int(query.from_user.id))
                await send_eps_files(query.from_user.id,search,client,query.message)

            return
        
        files_ = await get_file_details(file_id)

        if not files_:
            return await query.answer('Nᴏ sᴜᴄʜ ғɪʟᴇ ᴇxɪsᴛ.')
        
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption

        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
                f_caption = f_caption
        if f_caption is None:
            f_caption = f"{title}"
        await query.answer()
        
        if IS_VERIFY and not await check_verification(client, query.from_user.id):
            await verify_msg(query,client,file_id)
            return 
        
        await client.send_cached_media(
            chat_id=query.from_user.id,
            file_id=file_id,
            caption=f_caption,
            protect_content=True if PROTECT_CONTENT else False,
        )

    elif query.data.startswith("killfilesdq"):
        ident, keyword = query.data.split("#")
        await query.message.edit_text(f"<b>Fᴇᴛᴄʜɪɴɢ Fɪʟᴇs ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {keyword} ᴏɴ DB... Pʟᴇᴀsᴇ ᴡᴀɪᴛ...</b>")
        files,offset, total = await search_db(keyword,offset=0,max=True)
        await query.message.edit_text(f"<b>Fᴏᴜɴᴅ {total} Fɪʟᴇs ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {keyword} !\n\nFɪʟᴇ ᴅᴇʟᴇᴛɪᴏɴ ᴘʀᴏᴄᴇss ᴡɪʟʟ sᴛᴀʀᴛ ɪɴ 5 sᴇᴄᴏɴᴅs!</b>")
        await asyncio.sleep(5)
        deleted = 0
        async with lock:
            try:
                for file in files:
                    file_ids = file.file_id
                    file_name = file.file_name
                    result = await Media.collection.delete_one({
                        '_id': file_ids,
                    })
                    if result.deleted_count:
                        logger.info(f'Fɪʟᴇ Fᴏᴜɴᴅ ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {keyword}! Sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ {file_name} ғʀᴏᴍ ᴅᴀᴛᴀʙᴀsᴇ.')
                    deleted += 1
                    if deleted % 20 == 0:
                        await query.message.edit_text(f"<b>Pʀᴏᴄᴇss sᴛᴀʀᴛᴇᴅ ғᴏʀ ᴅᴇʟᴇᴛɪɴɢ ғɪʟᴇs ғʀᴏᴍ DB. Sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ {str(deleted)} ғɪʟᴇs ғʀᴏᴍ DB ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {keyword} !\n\nPʟᴇᴀsᴇ ᴡᴀɪᴛ...</b>")
            except Exception as e:
                logger.exception(e)
                await query.message.edit_text(f'Eʀʀᴏʀ: {e}')
            else:
                await query.message.edit_text(f"<b>Pʀᴏᴄᴇss Cᴏᴍᴘʟᴇᴛᴇᴅ ғᴏʀ ғɪʟᴇ ᴅᴇʟᴇᴛɪᴏɴ !\n\nSᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ {str(deleted)} ғɪʟᴇs ғʀᴏᴍ DB ғᴏʀ ʏᴏᴜʀ ᴏ̨ᴜᴇʀʏ {keyword}.</b>")

    elif query.data == "private_source":
        await query.answer(f"Project isn't Open Source!", show_alert=True)
    
    elif query.data == "start_dmca":
        await query.answer(f"Bot Disclaimer: Files here are freely available or posted by others online. Original creators, if you want your files removed, contact us.", show_alert=True)

    elif query.data == "about_bot":
        await loading_msg(query)
        await asyncio.sleep(0.3)
        btns = [[
            InlineKeyboardButton('ᴄʀᴇᴀᴛᴏʀ', url="https://t.me/Shadow506"),
            InlineKeyboardButton('sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ',callback_data="private_source" )
        ], [
            InlineKeyboardButton('ᴅᴍᴄᴀ', callback_data="start_dmca"),
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data="start_home_page")  # Corrected the URL here
        ]]
        cap = f"""<B>───[ ᴅᴇᴛᴀɪʟꜱ ]───

‣ ᴍʏ ɴᴀᴍᴇ : [{temp.B_NAME}](https://t.me/{temp.U_NAME})
‣ ᴅᴇᴠᴇʟᴏᴘᴇʀ : [sʜᴀᴅᴏᴡ](https://t.me/Shadow506)
‣ ʟɪʙʀᴀʀʏ : [ᴘʏʀᴏɢʀᴀᴍ](https://docs.pyrogram.org/)
‣ ʟᴀɴɢᴜᴀɢᴇ : [ᴘʏᴛʜᴏɴ 3](https://www.python.org/download/releases/3.0/)
‣ ᴅᴀᴛᴀ ʙᴀsᴇ : [ᴍᴏɴɢᴏ ᴅʙ](https://www.mongodb.com/)
‣ ʙᴏᴛ sᴇʀᴠᴇʀ : [ᴀᴡs](https://aws.amazon.com/)
‣ ʙᴜɪʟᴅ sᴛᴀᴛᴜs : v1.9 [ sᴛᴀʙʟᴇ ]</B>
        """

        await query.edit_message_text(
                    text=cap,
                    reply_markup=InlineKeyboardMarkup(btns)
                )

    elif query.data == "start_home_page":
        await loading_msg(query)
        buttons = [[
            InlineKeyboardButton('〆   ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ   〆', url=f"http://t.me/{temp.U_NAME}?startgroup=true")
            ],[
                    InlineKeyboardButton('⍟ ᴀʙᴏᴜᴛ', callback_data="about_bot"),
                    InlineKeyboardButton('⚡ ᴛʀᴇɴᴅɪɴɢ', callback_data="back_watch_start")
            ],[      
                    InlineKeyboardButton('⎚ ᴜᴘᴅᴀᴛᴇs', url="https://t.me/VegaLatest"),
                    InlineKeyboardButton('♨ ɢʀᴏᴜᴘ', url=GRP_LINK)
        ]]
        await query.edit_message_text(
                    text=script.START_TXT.format(query.from_user.mention, temp.B_NAME),
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
        
    else: return
