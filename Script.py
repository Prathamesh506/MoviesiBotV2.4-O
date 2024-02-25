class script(object):
    START_TXT = """𝚑𝚎𝚢👋, <b>{}

{}, ɪs ᴀᴛ ʏᴏᴜʀ sᴇʀᴠɪᴄᴇ!

ғᴇᴇʟ ғʀᴇᴇ ᴛᴏ ʀᴇϙᴜᴇsᴛ ᴀɴʏ ᴍᴏᴠɪᴇs, ɪ'ʟʟ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇᴍ. ʏᴏᴜ ᴄᴀɴ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴏʀ ᴊᴏɪɴ ᴏᴜʀs.‌</b>"""


    COMD_TXT = """ʜᴇʟᴘ: Aᴅᴍɪɴ Mᴏᴅs
<b>ɴᴏᴛᴇ:</b>
Tʜɪs Mᴏᴅᴜʟᴇ Oɴʟʏ Wᴏʀᴋs Fᴏʀ Mʏ Aᴅᴍɪɴs
Cᴏᴍᴍᴀɴᴅs Aɴᴅ Usᴀɢᴇ:
• /logs - <code>ᴛᴏ ɢᴇᴛ ᴛʜᴇ ʀᴇᴄᴇɴᴛ ᴇʀʀᴏʀꜱ</code>
• /stats - <code>ᴛᴏ ɢᴇᴛ ꜱᴛᴀᴛᴜꜱ ᴏꜰ ꜰɪʟᴇꜱ ɪɴ ᴅʙ.</code>
• /rstats - <code>ᴛᴏ ɢᴇᴛ rꜱᴛᴀᴛᴜꜱ ᴏꜰ ꜰɪʟᴇꜱ ɪɴ ᴅʙ.</code>
• /delete - <code>ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀ ꜱᴘᴇᴄɪꜰɪᴄ ꜰɪʟᴇ ꜰʀᴏᴍ ᴅʙ.</code>
• /channel - <code>ᴛᴏ ɢᴇᴛ ʟɪꜱᴛ ᴏꜰ ᴛᴏᴛᴀʟ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴄʜᴀɴɴᴇʟꜱ</code>
• /broadcast - <code>ᴛᴏ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴀʟʟ ᴜꜱᴇʀꜱ</code>
• /gbroadcast - <code>Tᴏ ʙʀᴏᴀᴅᴄᴀsᴛ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴀʟʟ ᴄᴏɴɴᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘs.</code>
• /request - <code>Tᴏ sᴇɴᴅ ᴀ Mᴏᴠɪᴇ/Sᴇʀɪᴇs ʀᴇᴏ̨ᴜᴇsᴛ ᴛᴏ ʙᴏᴛ ᴀᴅᴍɪɴs. Oɴʟʏ ᴡᴏʀᴋs ᴏɴ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ.</code>
• /kill - <code>Tᴏ ᴅᴇʟᴇᴛᴇ CᴀᴍRɪᴘ ᴀɴᴅ PʀᴇDVD Fɪʟᴇs ғʀᴏᴍ ᴛʜᴇ ʙᴏᴛ's ᴅᴀᴛᴀʙᴀsᴇ.</code>"""


    STATUS_TXT = """<b>BOT STATUS</b>\n\n| Users Verified:  {}\n| Total Files:  {}\n| Total Users:  {}\n| Total Chats:  {}\n| Used Storage:  {}\n| Free Storage:  {}\n"""

    
    SYS_STATUS_TXT = """
<b>SYSTEM STATUS</b>

| CPU Usage:  {}%
| RAM Usage:  {}%
| Disk Usage:  {}%
| Disk Free:  {}Gb
| Uptime:  {}
"""

    LOG_TEXT_G = """#NewGroup
Gʀᴏᴜᴘ = {}(<code>{}</code>)
Tᴏᴛᴀʟ Mᴇᴍʙᴇʀs = <code>{}</code>
Aᴅᴅᴇᴅ Bʏ - {}"""

    LOG_TEXT_P = """#NewUser
ID - <code>{}</code>
Nᴀᴍᴇ - {}"""

    ALRT_TXT = """This Isn't Your Request"""

    OLD_ALRT_TXT = """You Are Using One Of My Old Messages, Please Make A New Request"""

    MELCOW_ENG = """<b>Hᴇʟʟᴏ {} 😍, Aɴᴅ Wᴇʟᴄᴏᴍᴇ Tᴏ {} Gʀᴏᴜᴘ ❤️</b>"""

    CAPTION = """<i><b>{file_caption} ~ VegaMoviesX\n\nJOIN 💎 : @CiNEARCADE</i></b>"""


    RESTART_TXT = """<b>{} Is Now Online!</b>

<b>| Time : </b>{}
<b>| Date : </b>{}
<b>| Version : </b> V1.9 [ Stable ]
| #BotRebooted"""

    LOGO = """

██╗   ██╗███████╗ ██████╗  █████╗        ██████╗ ██████╗ ██████╗ ███████╗███████╗
██║   ██║██╔════╝██╔════╝ ██╔══██╗      ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝
██║   ██║█████╗  ██║  ███╗███████║█████╗██║     ██║   ██║██║  ██║█████╗  ███████╗
╚██╗ ██╔╝██╔══╝  ██║   ██║██╔══██║╚════╝██║     ██║   ██║██║  ██║██╔══╝  ╚════██║
 ╚████╔╝ ███████╗╚██████╔╝██║  ██║      ╚██████╗╚██████╔╝██████╔╝███████╗███████║
  ╚═══╝  ╚══════╝ ╚═════╝ ╚═╝  ╚═╝       ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝
                                                                                 """
