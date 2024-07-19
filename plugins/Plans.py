# import pyrogram
# from pyrogram import Client
# from utils import get_verify_status
# import datetime
# import pytz  
# from info import UPI_ID,OWNER_USERNAME

# prestats = """<b>PLAN DETAILS !

# User id: </b><code>{}</code>
# <b>Name: </b>{}

# <b>Plan: {}</b>

# <b>Verification Ends In:</b>
# <code>{}</code>

# <i></i>

# """
# pay_msg = f"""<b>PREMIUM PLANS ✨</b>

# ₹99 - Get Verified for <b>3 months</b>
# ₹199 - Get Verified for <b>6 months</b>
# ₹299 - Get Verified for <b>1 Year</b>

# <b>To Buy Dm: @AizeniBot</b>"""

# @Client.on_message(pyrogram.filters.private & pyrogram.filters.command(["premium"]))
# def premium_Plans(bot, update):
#     update.reply(pay_msg.format(), reply_markup=pay_btn2(bot, update), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)


# @Client.on_callback_query(pyrogram.filters.regex("buy_prm"))
# def strat_callback(bot, update):
#   update.message.edit(pay_msg.format(), reply_markup=pay_btn(bot, update.message), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)

# @Client.on_callback_query(pyrogram.filters.regex("bckpre"))
# async def back_org(bot, update):
#     status = await get_verify_status(update.from_user.id)
#     try:
#         if "date" in status and "time" in status:
#             status_date = datetime.datetime.strptime(status["date"], "%Y-%m-%d")
#             status_datetime = datetime.datetime.combine(status_date, datetime.datetime.strptime(status["time"], "%H:%M:%S").time())

#             asia_kolkata = pytz.timezone('Asia/Kolkata')
#             status_datetime = asia_kolkata.localize(status_datetime)

#             current_time = datetime.datetime.now(asia_kolkata)
#             time_difference = status_datetime - current_time
#             days, seconds = divmod(time_difference.seconds + time_difference.days * 86400, 86400)
#             hours, seconds = divmod(seconds, 3600)
#             minutes, seconds = divmod(seconds, 60)

#             if days > 1 or (days == 1 and (hours > 0 or minutes > 0 or seconds > 0)):
#                 user_type = "Premium ✨"
#             else:
#                 user_type = "Free User"

#             if status_datetime < current_time:
#                 formatted_difference = "0D : 00H : 00M : 00S"
#             else:
#                 formatted_difference = f"{days}D : {str(hours).zfill(2)}H : {str(minutes).zfill(2)}M : {str(seconds).zfill(2)}S"
#             reply_markup = await user_stas(bot, update)
#             await update.message.edit(prestats.format(update.from_user.id, update.from_user.mention, user_type, formatted_difference),
#                                       reply_markup=reply_markup, parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)
#         else:
#             as_msg = await update.reply_text("Date or time not found in status.")
#     except:
#         await update.answer() 

# @Client.on_message(pyrogram.filters.private & pyrogram.filters.command(["plan"]))
# async def started_command(bot, update):
#     status = await get_verify_status(update.from_user.id)

#     # Check if the key "date" and "time" exist in the dictionary
#     if "date" in status and "time" in status:
#         status_date = datetime.datetime.strptime(status["date"], "%Y-%m-%d")
#         status_datetime = datetime.datetime.combine(status_date, datetime.datetime.strptime(status["time"], "%H:%M:%S").time())

#         # Convert status_datetime to Asia/Kolkata timezone
#         asia_kolkata = pytz.timezone('Asia/Kolkata')
#         status_datetime = asia_kolkata.localize(status_datetime)

#         current_time = datetime.datetime.now(asia_kolkata)  # Get the current time in Asia/Kolkata timezone
#         time_difference = status_datetime - current_time
#         days, seconds = divmod(time_difference.seconds + time_difference.days * 86400, 86400)
#         hours, seconds = divmod(seconds, 3600)
#         minutes, seconds = divmod(seconds, 60)

#         if days > 1 or (days == 1 and (hours > 0 or minutes > 0 or seconds > 0)):
#             user_type = "Premium ✨"
#         else:
#             user_type = "Free User"

#         if status_datetime < current_time:
#             formatted_difference = "0D : 00H : 00M : 00S"
#         else:
#             formatted_difference = f"{days}D : {str(hours).zfill(2)}H : {str(minutes).zfill(2)}M : {str(seconds).zfill(2)}S"
#         reply_markup = await user_stas(bot, update)
#         await update.reply(prestats.format(update.from_user.id, update.from_user.mention, user_type, formatted_difference),
#                            reply_markup=reply_markup, parse_mode=pyrogram.enums.ParseMode.HTML,
#                            disable_web_page_preview=True)
#     else:
#         as_msg = await update.reply_text("Date or time not found in status.")

# async def user_stas(bot, update):
#   bot = await bot.get_me()
#   userid= update.from_user.id
#   buttons = [[
#     pyrogram.types.InlineKeyboardButton("Refresh Data 💫", callback_data="bckpre")
#    ],[
#    pyrogram.types.InlineKeyboardButton("Premium", callback_data="buy_prm"),
#    pyrogram.types.InlineKeyboardButton("Close", callback_data=f"close_data#{userid}")]]
#   return pyrogram.types.InlineKeyboardMarkup(buttons)

# def pay_btn(bot, update):
#   bot = bot.get_me()
#   buttons = [[
#    # pyrogram.types.InlineKeyboardButton("ϙʀ ᴄᴏᴅᴇ ▣", callback_data="sendqrcode"),
#    pyrogram.types.InlineKeyboardButton("Back ",callback_data="bckpre" ),
#    ]]
#   return pyrogram.types.InlineKeyboardMarkup(buttons)

# def pay_btn2(bot, update):
#   bot = bot.get_me()
#   userid= update.from_user.id
#   buttons = [[
#    # pyrogram.types.InlineKeyboardButton("ϙʀ ᴄᴏᴅᴇ ▣", callback_data="sendqrcode"),
#    pyrogram.types.InlineKeyboardButton("Close ",callback_data=f"close_data#{userid}" ),
#    ]]
#   return pyrogram.types.InlineKeyboardMarkup(buttons)
