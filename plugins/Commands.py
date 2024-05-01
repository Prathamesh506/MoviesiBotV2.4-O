import os
import re
import base64
import random
import psutil
import logging
import asyncio
import time, sys
from Script import script
from datetime import datetime,timedelta
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.ia_filterdb import Media, get_file_details, unpack_new_file_id
from database.users_chats_db import db
from info import CHANNELS,DLT, ADMINS,GRP_LINK,REQST_CHANNEL,AUTH_CHANNEL, LOG_CHANNEL, PICS, CUSTOM_FILE_CAPTION, PROTECT_CONTENT, IS_VERIFY, HOW_TO_VERIFY
from utils import  get_size, is_subscribed, temp, verify_user, check_token, check_verification, get_token,verify_VIP,verify_new
from  plugins.pm_Filter import send_eps_files

logger = logging.getLogger(__name__)
BATCH_FILES = {}

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    
    #NEW GRP
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        if not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown"))       
            await db.add_chat(message.chat.id, message.chat.title)
        alive = await message.reply_text("⚡")
        await asyncio.sleep(1)
        alive = await alive.edit_text("Yep, i'm Alive")
        await asyncio.sleep(1)
        await alive.delete()
        return
    
    #NEW USER
    if not await db.is_user_exist(message.from_user.id):
        await verify_new(client,message.from_user.id)
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
    
    #Only Start
    if len(message.command) != 2:
        buttons = [[
            InlineKeyboardButton('〆   ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ   〆', url=f"http://t.me/{temp.U_NAME}?startgroup=true")
            ],[
                    InlineKeyboardButton('⍟ ᴀʙᴏᴜᴛ', callback_data="about_bot"),
                    InlineKeyboardButton('⚡ ᴡᴀᴛᴄʜ', callback_data="back_watch_start")
            ],[      
                    InlineKeyboardButton('⎚ ᴜᴘᴅᴀᴛᴇs', url="https://t.me/VegaLatest"),
                    InlineKeyboardButton('♨ ɢʀᴏᴜᴘ', url=GRP_LINK)
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
    
    #force Sub
    if AUTH_CHANNEL and not await is_subscribed(client, message):
        try:
            invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        except ChatAdminRequired:
            logger.error("Mᴀᴋᴇ sᴜʀᴇ Bᴏᴛ ɪs ᴀᴅᴍɪɴ ɪɴ Fᴏʀᴄᴇsᴜʙ ᴄʜᴀɴɴᴇʟ")
            return
        btn = [
            [
                InlineKeyboardButton(
                    "Join My Channel", url=invite_link.invite_link
                )
            ]
        ]

        if message.command[1] != "subscribe":
            try:
                kk, file_id = message.command[1].split("_", 1)
                pre = 'checksubp' if kk == 'filep' else 'checksub' 
                btn.append([InlineKeyboardButton("Try Again", callback_data=f"{pre}#{file_id}")])
            except (IndexError, ValueError):
                btn.append([InlineKeyboardButton("Try Again", url=f"https://t.me/{temp.U_NAME}?start={message.command[1]}")])
        await client.send_message(
            chat_id=message.from_user.id,
            text=f"<b>Hey {message.from_user.mention},\n\nPlease Join My Channel To Use Me!</b>\nonce you are joined click on try again you will get files.",
            reply_markup=InlineKeyboardMarkup(btn)
            )
        return
    
    #other ultility cmds
    if len(message.command) == 2 and message.command[1] in ["subscribe", "error", "okay", "help"]:
        buttons = buttons = [[
            InlineKeyboardButton('〆   ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ   〆', url=f"http://t.me/{temp.U_NAME}?startgroup=true")
            ],[
                    InlineKeyboardButton('⍟ ᴀʙᴏᴜᴛ', callback_data="about_bot"),
                    InlineKeyboardButton('⚡ ᴡᴀᴛᴄʜ', callback_data="back_watch_start")
            ],[      
                    InlineKeyboardButton('⎚ ᴜᴘᴅᴀᴛᴇs', url="https://t.me/VegaLatest"),
                    InlineKeyboardButton('♨ ɢʀᴏᴜᴘ', url=GRP_LINK)
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
    
    data = message.command[1]
    try:
        pre, file_id = data.split('_', 1)
    except:
        file_id = data
        pre = ""

    if data.split("-", 1)[0] == "all_eps_files":
        userid = data.split("all_eps_files-")[1]
        if str(message.from_user.id) != str(userid):
            alert_msg = await message.reply_text("<i>This is not your batch Request</i>")
            await asyncio.sleep(5)
            await alert_msg.delete()
            return
        
        if IS_VERIFY and not await check_verification(client, message.from_user.id):
                pw_msg = await message.reply_text("Please Wait..")
                btn = [[
                    InlineKeyboardButton("Vᴇʀɪғʏ", url=await get_token(client, message.from_user.id, f"https://telegram.me/{temp.U_NAME}?start=", "all_eps")),
                    InlineKeyboardButton("Hᴏᴡ Tᴏ Vᴇʀɪғʏ", url=HOW_TO_VERIFY)
                ]]
                await pw_msg.delete()
                verify_btn = await message.reply_text(
                    text="<b>Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴠᴇʀɪғɪᴇᴅ!\nKɪɴᴅʟʏ ᴠᴇʀɪғʏ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ Sᴏ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ ɢᴇᴛ ᴀᴄᴄᴇss ᴛᴏ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇs ᴜɴᴛɪʟ 16 ʜᴏᴜʀs ғʀᴏᴍ ɴᴏᴡ !</b>\n<i>or just buy /premium Membership</i>",
                    protect_content=True if PROTECT_CONTENT else False,
                    reply_markup=InlineKeyboardMarkup(btn)
                )
                await asyncio.sleep(DLT)
                await verify_btn.delete()
                return

        search = await db.retrieve_latest_search(int(userid))
        await send_eps_files(userid,search,client,message)
        return
     
    if data.split("-", 1)[0] == "verify":
        userid = data.split("-", 2)[1]
        token = data.split("-", 3)[2]
        fileid = data.split("-", 3)[3]
        if str(message.from_user.id) != str(userid):
            return await message.reply_text(
                text="<b>Iɴᴠᴀʟɪᴅ ʟɪɴᴋ ᴏʀ Exᴘɪʀᴇᴅ ʟɪɴᴋ !</b>",
                protect_content=True if PROTECT_CONTENT else False
            )
        
        is_valid = await check_token(client, userid, token)
        if is_valid == True:
            await verify_user(client, userid, token)
            if fileid == "all_eps":
                link =  f"https://telegram.me/{temp.U_NAME}?start="
                url = f"{link}all_eps_files-{message.from_user.id}"
                btn = [[
                    InlineKeyboardButton("Gᴇᴛ Fɪʟᴇ",url=url)
                ]]
                await verify_user(client, userid, token)
                await message.reply_text(
                    text=f"<b>Hᴇʏ {message.from_user.mention}, Yᴏᴜ ᴀʀᴇ sᴜᴄᴄᴇssғᴜʟʟʏ ᴠᴇʀɪғɪᴇᴅ !\nNᴏᴡ ʏᴏᴜ ʜᴀᴠᴇ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ғᴏʀ ᴀʟʟ ᴍᴏᴠɪᴇs ᴛɪʟʟ ᴛʜᴇ ɴᴇxᴛ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴡʜɪᴄʜ ɪs ᴀғᴛᴇʀ 16 ʜᴏᴜʀs ғʀᴏᴍ ɴᴏᴡ.</b><i>\nuse /plan for more info</i>",
                    protect_content=True if PROTECT_CONTENT else False,
                    reply_markup=InlineKeyboardMarkup(btn)
                )
                return
            else:
                btn = [[
                    InlineKeyboardButton("Get File", url=f"https://telegram.me/{temp.U_NAME}?start=files_{fileid}")
                ]]
                await message.reply_text(
                    text=f"<b>Hᴇʏ {message.from_user.mention}, Yᴏᴜ ᴀʀᴇ sᴜᴄᴄᴇssғᴜʟʟʏ ᴠᴇʀɪғɪᴇᴅ !\nNᴏᴡ ʏᴏᴜ ʜᴀᴠᴇ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ғᴏʀ ᴀʟʟ ᴍᴏᴠɪᴇs ᴛɪʟʟ ᴛʜᴇ ɴᴇxᴛ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴡʜɪᴄʜ ɪs ᴀғᴛᴇʀ 16 ʜᴏᴜʀs ғʀᴏᴍ ɴᴏᴡ.</b><i>\nuse /plan for more info</i>",
                    protect_content=True if PROTECT_CONTENT else False,
                    reply_markup=InlineKeyboardMarkup(btn)
                )
                return   
        else:
            return await message.reply_text(
                text="<b>Iɴᴠᴀʟɪᴅ ʟɪɴᴋ ᴏʀ Exᴘɪʀᴇᴅ ʟɪɴᴋ !</b>",
                protect_content=True if PROTECT_CONTENT else False
            )

    files_ = await get_file_details(file_id)           
    if not files_:
        try:
            pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)
        except:
            pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("utf-8")).split("_", 1)

        try:
            if IS_VERIFY and not await check_verification(client, message.from_user.id):
                pw_msg = await message.reply_text("Please Wait..")
                btn = [[
                    InlineKeyboardButton("Vᴇʀɪғʏ", url=await get_token(client, message.from_user.id, f"https://telegram.me/{temp.U_NAME}?start=", file_id)),
                    InlineKeyboardButton("Hᴏᴡ Tᴏ Vᴇʀɪғʏ", url=HOW_TO_VERIFY)
                ]]
                await pw_msg.delete()
                verify_btn = await message.reply_text(
                    text="<b>Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴠᴇʀɪғɪᴇᴅ!\nKɪɴᴅʟʏ ᴠᴇʀɪғʏ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ Sᴏ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ ɢᴇᴛ ᴀᴄᴄᴇss ᴛᴏ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇs ᴜɴᴛɪʟ 16 ʜᴏᴜʀs ғʀᴏᴍ ɴᴏᴡ !</b>\n<i>or just buy /premium Membership</i>",
                    protect_content=True if PROTECT_CONTENT else False,
                    reply_markup=InlineKeyboardMarkup(btn)
                )
                await asyncio.sleep(DLT)
                await verify_btn.delete()
                return
            
            msg = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file_id,
                protect_content=True if pre == 'filep' else False
            )
            filetype = msg.media
            file = getattr(msg, filetype.value)
            title = file.file_name
            size=get_size(file.file_size)
            f_caption = f"<code>{title}</code>"
            if CUSTOM_FILE_CAPTION:
                try:
                    f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='')
                except:
                    return
            await msg.edit_caption(f_caption)
            return
        except:
            pass
        return await message.reply('Nᴏ sᴜᴄʜ ғɪʟᴇ ᴇxɪsᴛ.')
    
    files = files_[0]
    title = files.file_name
    size=get_size(files.file_size)
    f_caption=files.caption
    if CUSTOM_FILE_CAPTION:
        try:
            f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
        except Exception as e:
            logger.exception(e)
            f_caption=f_caption
    if f_caption is None:
        f_caption = f"{files.file_name}"
    if IS_VERIFY and not await check_verification(client, message.from_user.id):
        pw_msg = await message.reply_text("Please Wait..")
        btn = [[
            InlineKeyboardButton("Vᴇʀɪғʏ", url=await get_token(client, message.from_user.id, f"https://telegram.me/{temp.U_NAME}?start=", file_id)),
            InlineKeyboardButton("Hᴏᴡ Tᴏ Vᴇʀɪғʏ", url=HOW_TO_VERIFY)
        ]]
        await pw_msg.delete()
        verify_btn=await message.reply_text(
            text="<b>Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴠᴇʀɪғɪᴇᴅ!\nKɪɴᴅʟʏ ᴠᴇʀɪғʏ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ Sᴏ ᴛʜᴀᴛ ʏᴏᴜ ᴄᴀɴ ɢᴇᴛ ᴀᴄᴄᴇss ᴛᴏ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇs ᴜɴᴛɪʟ 16 ʜᴏᴜʀs ғʀᴏᴍ ɴᴏᴡ !</b>\n<i>or just buy /premium Membership</i>",
            protect_content=True if PROTECT_CONTENT else False,
            reply_markup=InlineKeyboardMarkup(btn)
        )
        await asyncio.sleep(DLT)
        await verify_btn.delete()
        return
    
    await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,
        protect_content=True if pre == 'filep' else False
    )

@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
           
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Uɴᴇxᴘᴇᴄᴛᴇᴅ ᴛʏᴘᴇ ᴏғ CHANNELS")

    text = '📑 **Iɴᴅᴇxᴇᴅ ᴄʜᴀɴɴᴇʟs/ɢʀᴏᴜᴘs**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total:** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)

@Client.on_message(filters.command("verify") & filters.user(ADMINS))
async def verifying_vip(client, message):
    try:
        msg = message.text
        vipsid = message.command[1]
        timd = message.command[2]
        
        if timd not in ('0','1', '7', '30', '90', '180', '365', '1000'):
            raise ValueError("Invalid Plan!")

        type_map = {'1': "Free", '7': "Basics", '30': "Standard", '90': "Elite", '180': "Premium", '365': "Premium", '1000': "Ultimate",'0':"Zero"}
        type = type_map[timd]

        plan = int(timd)

        if vipsid and vipsid.isdigit() and len(vipsid) in (9, 10):
            await verify_VIP(client, vipsid, plan)
            username = await db.get_username_by_id(vipsid)

            s_m = any(admin == int(vipsid) for admin in ADMINS)

            msg = f"<b>{type} Plan Activated!</b>\n\n<b>Name : </b>{username}\n<b>User id :</b> {vipsid}\n<b>Verified For:</b> {timd} Days \n\n<i>for more info use /plan command.</i>"
            
            await message.reply(msg)

            vipsid = int(vipsid)
            if not s_m:
                await client.send_message(vipsid, msg)
        else:
            raise ValueError("Invalid command!")

    except Exception as e:
        await message.reply(f"{str(e)}")

@Client.on_message(filters.command("send") & filters.user(ADMINS))
async def send_msg(bot, message):
    if message.reply_to_message:
        target_id = message.text.split(" ", 1)[1]
        out = "Usᴇʀs Sᴀᴠᴇᴅ Iɴ DB Aʀᴇ:\n\n"
        success = False
        try:
            user = await bot.get_users(target_id)
            users = await db.get_all_users()
            async for usr in users:
                out += f"{usr['id']}"
                out += '\n'
            if str(user.id) in str(out):
                await message.reply_to_message.copy(int(user.id))
                success = True
            else:
                success = False
            if success:
                await message.reply_text(f"<b>Yᴏᴜʀ ᴍᴇssᴀɢᴇ ʜᴀs ʙᴇᴇɴ sᴜᴄᴄᴇssғᴜʟʟʏ sᴇɴᴅ ᴛᴏ {user.mention}.</b>")
            else:
                await message.reply_text("<b>Tʜɪs ᴜsᴇʀ ᴅɪᴅɴ'ᴛ sᴛᴀʀᴛᴇᴅ ᴛʜɪs ʙᴏᴛ ʏᴇᴛ!</b>")
        except Exception as e:
            await message.reply_text(f"<b>Eʀʀᴏʀ: {e}</b>")
    else:
        await message.reply_text("<b>Usᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴀs ᴀ ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴍᴇssᴀɢᴇ ᴜsɪɴɢ ᴛʜᴇ ᴛᴀʀɢᴇᴛ ᴄʜᴀᴛ ɪᴅ. Fᴏʀ ᴇɢ: /send ᴜsᴇʀɪᴅ</b>")

@Client.on_message(filters.command('verification') & filters.user(ADMINS))
async def verify_settings(client, message):
    global IS_VERIFY
    IS_VERIFY = not IS_VERIFY
    with open("info.py", "a") as file:
        file.write(f"\nIS_VERIFY = {IS_VERIFY}\n")
    await message.reply(f"Verification is {'enabled' if IS_VERIFY else 'disabled'}")
   
@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('Logs.txt')
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Pʀᴏᴄᴇssɪɴɢ...⏳", quote=True)
    else:
        await message.reply('Rᴇᴘʟʏ ᴛᴏ ғɪʟᴇ ᴡɪᴛʜ /delete ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇ', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('Tʜɪs ɪs ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ ғɪʟᴇ ғᴏʀᴍᴀᴛ')
        return
    
    file_id, file_ref = unpack_new_file_id(media.file_id)

    result = await Media.collection.delete_one({
        '_id': file_id,
    })
    if result.deleted_count:
        await msg.edit('Fɪʟᴇ ɪs sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ғʀᴏᴍ ᴅᴀᴛᴀʙᴀsᴇ')
    else:
        file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
        result = await Media.collection.delete_many({
            'file_name': file_name,
            'file_size': media.file_size,
            'mime_type': media.mime_type
            })
        if result.deleted_count:
            await msg.edit('Fɪʟᴇ ɪs sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ғʀᴏᴍ ᴅᴀᴛᴀʙᴀsᴇ')
        else:
            result = await Media.collection.delete_many({
                'file_name': media.file_name,
                'file_size': media.file_size,
                'mime_type': media.mime_type
            })
            if result.deleted_count:
                await msg.edit('Fɪʟᴇ ɪs sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ғʀᴏᴍ ᴅᴀᴛᴀʙᴀsᴇ')
            else:
                await msg.edit('Fɪʟᴇ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ')

@Client.on_message(filters.command('stats') & filters.user(ADMINS))
async def get_ststs(bot, message):
    Stats_msg = await message.reply('Fetching stats..')
    total_users = await db.total_users_count()
    totl_chats = await db.total_chat_count()
    files = await Media.count_documents()
    size = await db.get_db_size()
    free = 536870912 - size
    size = get_size(size)
    free = get_size(free)
    total_count = await db.get_verify_count()
    await Stats_msg.edit(script.STATUS_TXT.format(total_count,files, total_users, totl_chats, size, free))

@Client.on_message(filters.command("kill") & filters.user(ADMINS))
async def deletemultiplefiles(bot, message):
    chat_type = message.chat.type
    if chat_type != enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>Hᴇʏ {message.from_user.mention}, Tʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏɴ'ᴛ ᴡᴏʀᴋ ɪɴ ɢʀᴏᴜᴘs. Iᴛ ᴏɴʟʏ ᴡᴏʀᴋs ᴏɴ ᴍʏ PM!</b>")
    else:
        pass
    try:
        keyword = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text(f"<b>Hᴇʏ {message.from_user.mention}, Gɪᴠᴇ ᴍᴇ ᴀ ᴋᴇʏᴡᴏʀᴅ ᴀʟᴏɴɢ ᴡɪᴛʜ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴅᴇʟᴇᴛᴇ ғɪʟᴇs.</b>")
    btn = [[
       InlineKeyboardButton("Yᴇs, Cᴏɴᴛɪɴᴜᴇ !", callback_data=f"killfilesdq#{keyword}")
       ],[
       InlineKeyboardButton("Nᴏ, Aʙᴏʀᴛ ᴏᴘᴇʀᴀᴛɪᴏɴ !", callback_data="close")
    ]]
    await message.reply_text(
        text="<b>Aʀᴇ ʏᴏᴜ sᴜʀᴇ? Dᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ?\n\nNᴏᴛᴇ:- Tʜɪs ᴄᴏᴜʟᴅ ʙᴇ ᴀ ᴅᴇsᴛʀᴜᴄᴛɪᴠᴇ ᴀᴄᴛɪᴏɴ!</b>",
        reply_markup=InlineKeyboardMarkup(btn),
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message((filters.command(["request", "Request"]) | filters.regex("#request") | filters.regex("#Request")))
async def requests(bot, message):
    if REQST_CHANNEL:
        reporter = str(message.from_user.id)
        mention = message.from_user.mention
        content = message.text[9:].title()
        if len(content) < 3: 
            await message.reply_text("<b>Follow the proper Format</b> \n\nEg: #request Fighter 2024")
            return
        btn = []
        #development
        btn.insert(0, [
                            InlineKeyboardButton('✅',callback_data=f'req_oprt#req_pstd#{reporter}#{content}'),
                            InlineKeyboardButton("❌", callback_data=f'req_oprt#req_noprt#{reporter}#{content}')
                        ])
        rp = await bot.send_message(chat_id=REQST_CHANNEL, text=f"<b>Requested By :</b> {mention} \n\n<b>Request :</b><code> {content}</code>\n\n<i>Your request will be fulfilled shortly.</i>", reply_markup=InlineKeyboardMarkup(btn))
        btn2 = [[
                            InlineKeyboardButton('Vɪᴇᴡ Rᴇᴏ̨ᴜᴇsᴛ 📃', url=f"{rp.link}")
                        ]]
        await message.reply_text("<b>Yᴏᴜʀ ʀᴇᴏ̨ᴜᴇsᴛ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ! Pʟᴇᴀsᴇ ᴡᴀɪᴛ ғᴏʀ sᴏᴍᴇ ᴛɪᴍᴇ.</b>", reply_markup=InlineKeyboardMarkup(btn2))
    else:
        return

#RESTART 
@Client.on_message(filters.command("restart") & filters.user(ADMINS))
async def stop_button(bot, message):
    msg = await bot.send_message(text="**Rebooting**", chat_id=message.chat.id)       
    await asyncio.sleep(3)
    await msg.edit("**𝙱ot Restarted ✅ **")
    os.execl(sys.executable, sys.executable, *sys.argv)

#VERIFY COUNT
@Client.on_message(filters.command('report') & filters.user(ADMINS))
async def verify_month(bot, message):
    try:
        month = int(message.command[1])
    except: 
        month = None
    month_data = await db.get_month_verify_count(month=month)

    if month:
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        if month < 1 or month > 12:
            return await message.reply_text("Invalid Month")
        month_name = months[month - 1]
    else:
        month_name = "Month"

    # Calculate total count for the month
    total_count_month = sum(month_data.values())

    # Format the month data
    formatted_month_data = "\n".join([f"{date}: {count}" for date, count in month_data.items()])

    response_message = f"<b>{month_name} Report!</b>\n\n<b> Total : </b><code>{total_count_month}<code>\n\n{formatted_month_data}"

    await message.reply_text(response_message)

# @Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
# async def delete_all_index(bot, message):
#     await message.reply_text(
#         'Tʜɪs ᴡɪʟʟ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ɪɴᴅᴇxᴇᴅ ғɪʟᴇs.\nDᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ ?',
#         reply_markup=InlineKeyboardMarkup(
#             [
#                 [
#                     InlineKeyboardButton(
#                         text="Yᴇs", callback_data="autofilter_delete_all"
#                     )
#                 ],
#                 [
#                     InlineKeyboardButton(
#                         text="Cᴀɴᴄᴇʟ", callback_data=f"close_data#{message.from_user.id}"
#                     )
#                 ],
#             ]
#         ),
#         quote=True,
#     )
    
# @Client.on_callback_query(filters.regex(r'^autofilter_delete_all'))
# async def delete_all_index_confirm(bot, message):
#     await Media.collection.drop()
#     await message.answer("Eᴠᴇʀʏᴛʜɪɴɢ's Gᴏɴᴇ")
#     await message.message.edit('Sᴜᴄᴄᴇsғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ Aʟʟ Tʜᴇ Iɴᴅᴇxᴇᴅ Fɪʟᴇs.')    

#SYSTEM RESOURCES STATUS
@Client.on_message(filters.command('rstats') & filters.user(ADMINS))
async def get_system_info(bot, message):
    rju = await message.reply('Fetching stats..')
    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/')
    disk_usage_percent = disk_usage.percent
    disk_free_gb = round(disk_usage.free / (1024**3), 2)
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    uptime_str = str(timedelta(seconds=uptime.total_seconds()))
    uptime_str = uptime_str.split('.')[0]
    status_message = script.SYS_STATUS_TXT.format(cpu_percent, ram_percent, disk_usage_percent, disk_free_gb, uptime_str)
    await rju.edit(status_message)
