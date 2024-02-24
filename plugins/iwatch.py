from pyrogram import Client, filters, enums
from  plugins.pm_Filter import watch_movies_filter
from database.watch import store_movies_from_text,delete_category,get_all_movies
from info import ADMINS

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