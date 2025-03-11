
# +++ Made By King [telegram username: @Shidoteshika1] +++

import random
import asyncio
from bot import Bot
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.enums import ParseMode, ChatAction
from config import Config as cfg
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, ReplyKeyboardMarkup, ReplyKeyboardRemove

CLOSE_BUTTON = InlineKeyboardButton("🔒 ᴄʟᴏsᴇ", "close")
CLOSE_MARKUP = InlineKeyboardMarkup([[CLOSE_BUTTON]])

START_MESSAGE = """**Hᴇʏ {} ~**

**I ᴀᴍ ᴀ Pʀɪᴠᴀᴛᴇ ғɪʟᴇ Rᴇ-ᴘᴏsᴛᴇʀ ᴀs ᴡᴇʟʟ ᴀs Lɪɴᴋ Gᴇɴᴇʀᴀᴛᴏʀ Bᴏᴛ**

<blockquote>**Oᴡɴᴇʀ: {}**</blockquote>"""

@Bot.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ", url=client.dev.link), CLOSE_BUTTON]])
    
    if cfg.ENABLE_PICS and cfg.PICS:
        await message.reply_photo(
            photo=random.choice(cfg.PICS),
            caption=START_MESSAGE.format(message.from_user.mention, client.owner.name_link),
            reply_markup=reply_markup
        )
    else:
        await message.reply(
            text=START_MESSAGE.format(message.from_user.mention, client.owner.name_link),
            quote=True,
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )

