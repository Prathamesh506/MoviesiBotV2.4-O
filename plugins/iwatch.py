from pyrogram import Client, filters, enums

from database.watch import store_movies_from_text,delete_category,get_all_movies
from info import ADMINS
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio
from info import DLT
from Script import script
from database.watch import store_movies_from_text,does_movie_exxists,search_movie_db,get_watch_movies
from plugins.pm_Filter import process_text


#WATCH COMMAHDS   
@Client.on_message(filters.command('watch'))
async def watch_cmd(bot, message):
    await watch_movies_filter(bot, message)
    return

@Client.on_message(filters.command('store') & filters.user(ADMINS))
async def store_movie_search(bot, message):
    input_str = message.text[7:].lower()
    await store_movies_from_text(input_str)

@Client.on_message(filters.command('del_cat') & filters.user(ADMINS))
async def deletes_catagory(bot, message):
    input_str = message.text[9:]
    deleted = await delete_category(input_str)
    await message.reply_text(f"Deleted: {deleted}")

@Client.on_message(filters.command('get_all') & filters.user(ADMINS))
async def cat_get_all(bot, message):
    input_str = message.text[9:]
    movies_list = await get_all_movies()
    await message.reply_text(f"Deleted: {movies_list}")

#WATCH FUNCTANLITY   
async def watch_movies_filter(client, msg,type=False,start_btn=False):
    btn = watch_btn(msg.from_user.id,start_btn)
    cap = f"<b>Hᴇʏ {msg.from_user.mention},\n\nCʜᴏᴏsᴇ Pʀᴇғᴇʀʀᴇᴅ Cᴀᴛᴇɢᴏʀʏ : </b>"
    if type:
        result_msg = await msg.edit_message_text(text=cap,reply_markup=InlineKeyboardMarkup(btn))
    else:
        result_msg = await msg.reply_photo(photo="https://telegra.ph/file/b9ed75fcef91d7edd629b.jpg", caption=cap,
        
                                        reply_markup=InlineKeyboardMarkup(btn))
    await asyncio.sleep(DLT)
    await result_msg.delete()    

def watch_btn(userid,start_btn):
    btn= []
    if start_btn:
        btn.insert(0,[
        InlineKeyboardButton("Aᴅᴜʟᴛ 🔞", callback_data=f"watch_movies#{userid}#18plus"),
        InlineKeyboardButton("ʙᴀᴄᴋ", callback_data=f"start_home_page")
    ])
    else:
        btn.insert(0,[
        InlineKeyboardButton("Aᴅᴜʟᴛ 🔞", callback_data=f"watch_movies#{userid}#18plus"),
        InlineKeyboardButton("Cʟᴏsᴇ ✘", callback_data=f"close_data#{userid}")
    ])
    btn2 = [[
        InlineKeyboardButton("Tʀᴇɴᴅɪɴɢ 🔥", callback_data=f"watch_movies#{userid}#trending"),
        InlineKeyboardButton("Nᴇᴡ Oᴛᴛ ⚡", callback_data=f"watch_movies#{userid}#ott")
    ],[
        InlineKeyboardButton("Iɴᴅɪᴀɴ 🚩", callback_data=f"watch_movies#{userid}#bollywood"),
        InlineKeyboardButton("Hᴏʟʟʏᴡᴏᴏᴅ 🍿", callback_data=f"watch_movies#{userid}#hollywood")
    ],[
        InlineKeyboardButton("Sᴄɪ-Fɪ 👽", callback_data=f"watch_movies#{userid}#scifi"),
        InlineKeyboardButton("Sᴇʀɪᴇs 🕵️‍♀️", callback_data=f"watch_movies#{userid}#series")
    ],[
        InlineKeyboardButton("Hᴏʀʀᴇʀ 💀", callback_data=f"watch_movies#{userid}#horror"),
        InlineKeyboardButton("Cᴏᴍᴇᴅʏ 😂", callback_data=f"watch_movies#{userid}#comedy")
    ],[
        InlineKeyboardButton("Mᴀʀᴠᴇʟ 🦸", callback_data=f"watch_movies#{userid}#marvel"),
        InlineKeyboardButton("ᴀɴɪᴍᴇ 🦊", callback_data=f"watch_movies#{userid}#anime")
    ]]
    return btn2+btn

@Client.on_callback_query(filters.regex(r"^watch_movies"))
async def watch_movies_lst(bot, query): 
    user_id = query.from_user.id
    _,userid,cat = query.data.split("#")
    if int(userid) != user_id:
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    
    results,total_results = await get_watch_movies(cat)
    btn = []

    for i, movie in enumerate(results):
        title = await process_text(movie.get('title', ''))
        rating = movie.get('rating', '')
        s_no = movie.get('popularity', '')
        trimmed_movie_name = title[:30]
        button_data = f"add_filter#{user_id}#mainpage#{trimmed_movie_name}"
        if cat == "trending":
            button_text = f"[ {s_no} ] {title.title()}"
        else:
            button_text = f"{s_no}. {title.title()} ( {rating} )"
        button = InlineKeyboardButton(text=button_text, callback_data=button_data)
        btn.append([button])
    total_pages = -(-int(total_results) // 10)

    if len(results) == 0:
         await query.answer(f"Sorry No Movies Found Here", show_alert=True)
         return
    
    if total_pages == 1:
        btn.append([
                InlineKeyboardButton(text="🏠",callback_data=f"back_watch"),
                InlineKeyboardButton(text=f"1 / {total_pages}",callback_data="pages")]
            )
    else:
        btn.append([
                InlineKeyboardButton(text=f"🏠 1 / {total_pages}",callback_data=f"back_watch"),
                InlineKeyboardButton(text="Nᴇxᴛ ⌦",callback_data=f"watch_nxt#{user_id}#2#{cat}") ]
            )
    cap = f"<b>Hey {query.from_user.mention},\n\nFᴏᴜɴᴅ Rᴇꜱᴜʟᴛꜱ Fᴏʀ </b>{cat.title()}!"
    await query.edit_message_text(
                text=cap,
                reply_markup=InlineKeyboardMarkup(btn)
            )
    return

@Client.on_callback_query(filters.regex(r"^watch_nxt"))
async def next_page_watch(bot, query):
    _, user_id, offset,cat = query.data.split("#")
    if int(user_id) not in [query.from_user.id, 0]:
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 1

    btn = []
    
    next_offset = offset+1
    prev_offset = offset -1

    results,total_results = await get_watch_movies(cat,offset)

    for i, movie in enumerate(results):
        title = await process_text(movie.get('title', ''))
        rating = movie.get('rating', '')
        s_no = movie.get('popularity', '')
        trimmed_movie_name = title[:30]
        button_data = f"add_filter#{user_id}#mainpage#{trimmed_movie_name}"
        if cat == "trending":
            button_text = f"[ {s_no} ] {title.title()}"
        else:
            button_text = f"{s_no}. {title.title()} ( {rating} )"
        button = InlineKeyboardButton(text=button_text, callback_data=button_data)
        btn.append([button])
    total_pages = -(-int(total_results) // 10)

    if total_pages == 0 or total_pages is None:
         await query.answer(f"Sorry No Movies Found Here", show_alert=True)
         return
    if total_pages == 1:
        btn.append([
                InlineKeyboardButton(text="🏠",callback_data=f"back_watch"),
                InlineKeyboardButton(text=f"{offset} / {total_pages}",callback_data="pages")]
            )
    elif offset ==1:
        btn.append([
                InlineKeyboardButton(text=f"🏠 {offset} / {total_pages}",callback_data="back_watch"),
                InlineKeyboardButton(text="Nᴇxᴛ ⌦",callback_data=f"watch_nxt#{user_id}#{next_offset}#{cat}") ]
            )
    elif offset ==  total_pages:
        btn.append([
                InlineKeyboardButton(text="❮ Bᴀᴄᴋ",callback_data=f"watch_nxt#{user_id}#{prev_offset}#{cat}"),
                InlineKeyboardButton(text=f"🏠 {offset} / {total_pages}",callback_data="back_watch")]
            )
    else:
        btn.append([
                InlineKeyboardButton(text="❮ Bᴀᴄᴋ",callback_data=f"watch_nxt#{user_id}#{prev_offset}#{cat}"),
                InlineKeyboardButton(text=f"🏠 {offset} / {total_pages}",callback_data="back_watch"),
                InlineKeyboardButton(text="Nᴇxᴛ ⌦",callback_data=f"watch_nxt#{user_id}#{next_offset}#{cat}") ]
            )
    cap = f"<b>Hey {query.from_user.mention},\n\nFᴏᴜɴᴅ Rᴇꜱᴜʟᴛꜱ Fᴏʀ : {cat.title()}!</b>"
    try:
        await query.edit_message_text(
                    text=cap,
                    reply_markup=InlineKeyboardMarkup(btn)
                )
    except:
        pass
    return

