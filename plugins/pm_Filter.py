
import asyncio
import logging

from pyrogram import Client, filters

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTONS = {}
SPELL_CHECK = {}


@Client.on_message((filters.group | filters.private) & filters.text & filters.incoming)
async def auto_filter(client, msg):
    await msg.reply_text("<b>We’ve Moved to: @@Makimai2Bot</b>")
    return
