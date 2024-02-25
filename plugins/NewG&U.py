from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
from info import ADMINS, LOG_CHANNEL, GRP_LINK,DLT,WELCOW_NEW_USERS,WELCOME_PICS,SUP_LINK,UPDATES
from database.users_chats_db import db
from database.ia_filterdb import Media
from utils import temp
from Script import script
import asyncio 
import random


@Client.on_message(filters.new_chat_members & filters.group)
async def save_group(bot, message):
    r_j_check = [u.id for u in message.new_chat_members]
    if temp.ME in r_j_check:
        if not await db.get_chat(message.chat.id):
            total=await bot.get_chat_members_count(message.chat.id)
            r_j = message.from_user.mention if message.from_user else "Anonymous" 
            await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, r_j))       
            await db.add_chat(message.chat.id, message.chat.title)
        
        buttons = [[
                    InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=SUP_LINK),
                    InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=f"https://t.me/{UPDATES}")
                 ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        addmsg = await message.reply_text(
            text=f"<b>Thankyou For Adding Me In {message.chat.title} ❣️\n\nIf you have any questions & doubts about using me contact my support.</b>",
            reply_markup=reply_markup)
        await asyncio.sleep(600)
        await addmsg.delete(DLT)
        
    else:
        return
        # if WELCOW_NEW_USERS:
        #     user_wc = await message.reply_photo(
        #                                          photo=random.choice(WELCOME_PICS),
        #                                          caption=(script.MELCOW_ENG.format(message.from_user.mention, message.chat.title)),
        #                                          reply_markup=InlineKeyboardMarkup(
        #                                                                  [[
        #                                                                    InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=SUP_LINK),
        #                                                                    InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=f"https://t.me/{UPDATES}")
        #                                                                 ]]
        #                                          ),
        #                                          parse_mode=enums.ParseMode.HTML
        #         )
        # await asyncio.sleep(600)
        # await user_wc.delete()