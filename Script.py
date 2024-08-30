class script(object):

    START_TXT = """Hey <b{}</b>,
    
<B>{}</B> Is at your service!

Send the name of any movie, series, or anime to get the files. Use /watch for recommendations!"""

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

    STATUS_TXT = """
<b>BOT STATUS</b>

| Users Verified: {}
| Total Files: {}
| Total Users: {}
| Total Chats: {}
| Used Storage: {}
| Free Storage: {}
"""

    SYS_STATUS_TXT = """
<b>SYSTEM STATUS</b>

| CPU Usage: {}%
| RAM Usage: {}%
| Disk Usage: {}%
| Disk Free: {}Gb
| Uptime: {}
"""

    SYS_STATUS_TXT2 = """
<b>───[ sʏsᴛᴇᴍ sᴛᴀᴛs ]───</b>

<B>| CPU Usage:</b> {}%
<b>| RAM Usage:</b> {}%
<b>| Disk Usage:</b> {}%
<b>| Disk Free:</b> {}Gb
<b>| Uptime:</b> {}
"""

    LOG_TEXT_G = """#NewGroup
Gʀᴏᴜᴘ = {}(<code>{}</code>)
Tᴏᴛᴀʟ Mᴇᴍʙᴇʀs = <code>{}</code>
Aᴅᴅᴇᴅ Bʏ - {}"""

    LOG_TEXT_P = """#NewUser
ID - <code>{}</code>
Nᴀᴍᴇ - {}"""

    ALRT_TXT = """⚠️ Tʜɪs Is Nᴏᴛ Yᴏᴜʀ Rᴇϙᴜᴇsᴛ."""

    OLD_ALRT_TXT = """⚠️ Rᴇϙᴜᴇsᴛ Expired! Rᴇϙᴜᴇsᴛ Aɢᴀɪɴ."""

    MELCOW_ENG = """<b>Hᴇʟʟᴏ {} 😍, Aɴᴅ Wᴇʟᴄᴏᴍᴇ Tᴏ {} Gʀᴏᴜᴘ ❤️</b>"""

    CAPTION = """<i><b>{file_caption} ~ VegaMoviesX\n\nJOIN 💎 : @CiNEARCADE</i></b>"""

    RESTART_TXT = """<b>{} Is Now Online!</b>

<b>| Time : </b>{}
<b>| Date : </b>{}
<b>| Version : </b> V2.1 [ Stable ]
| #BotRebooted"""

    LOGO = """

██╗   ██╗███████╗ ██████╗  █████╗        ██████╗ ██████╗ ██████╗ ███████╗███████╗
██║   ██║██╔════╝██╔════╝ ██╔══██╗      ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝
██║   ██║█████╗  ██║  ███╗███████║█████╗██║     ██║   ██║██║  ██║█████╗  ███████╗
╚██╗ ██╔╝██╔══╝  ██║   ██║██╔══██║╚════╝██║     ██║   ██║██║  ██║██╔══╝  ╚════██║
 ╚████╔╝ ███████╗╚██████╔╝██║  ██║      ╚██████╗╚██████╔╝██████╔╝███████╗███████║
  ╚═══╝  ╚══════╝ ╚═════╝ ╚═╝  ╚═╝       ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝
                                                                                 """
