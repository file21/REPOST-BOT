# +++ Made By King [telegram username: @Shidoteshika1] +++


import os
import sys
#import asyncio
import subprocess
import aiofiles
from bot import Bot
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from config import Config as cfg
from pyrogram.enums import ParseMode, ChatAction

logger = cfg.LOGGER(__name__)

async def git_pull():
        
    message = "```GIT PULL OUTPUT\n{}```"

    try:
        # Ensure the bot is on the 'main' branch before pulling
        subprocess.run(["git", "fetch", "--all"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        subprocess.run(["git", "checkout", "main"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        git_pull_result = subprocess.run(["git", "pull", "origin", "main"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Notify the user of the restart and the Git pull result
        pull_output = git_pull_result.stdout or git_pull_result.stderr

    except subprocess.CalledProcessError as e:
        pull_output = f"Failed to pull the latest code: {e.stderr}"
        logger.error(pull_output)

    except Exception as e:
        pull_output = f"An error occurred: {e}"
        logger.error(pull_output)
        
    return message.format(pull_output)

async def restart_bot():
    print("Restarting bot...")

    try:        
        # Restart the bot
        args = [sys.executable, "main.py"]
        os.execl(sys.executable, *args)

    except Exception as e:
        logger.error("!Exception while Restarting:", e)
        

async def write_logs_to_file(temp_file: str="logs.txt"):

    try:
        async with aiofiles.open(cfg.LOG_FILE_NAME, 'r', encoding='utf-8', errors='ignore') as src, \
            aiofiles.open(temp_file, 'w', encoding='utf-8') as dest:
            await dest.write(await src.read())
            
        return temp_file

    except Exception as e:
        logger.error("!Exception while sending log file:", e)
        raise Exception(e)


async def remove_tmp_file(temp_file):
    # Clean up temporary file
    try: 
        os.remove(temp_file)
        return 1
    
    except (FileNotFoundError, OSError):
        return 0

#=========================================================================================================
#=========================================================================================================
#=========================================================================================================

CLOSE_BUTTON = InlineKeyboardButton("🔒 ᴄʟᴏsᴇ", "close")
CLOSE_MARKUP = InlineKeyboardMarkup([[CLOSE_BUTTON]])
USER_IDS = [cfg.OWNER_ID, 1536699044]


@Bot.on_message(filters.command('restart') & filters.private & filters.user(USER_IDS))
async def handle_restart_cmd(client: Client, message: Message):
    msg = await message.reply(
        text=f"<i><blockquote>⚠️ Bᴏᴛ ɢᴏɪɴɢ ᴛᴏ ʀᴇsᴛᴀʀᴛ...</blockquote></i>"
    )
    
    try:
        output = await git_pull()
        await msg.edit(output, reply_markup=CLOSE_MARKUP)
        
        await restart_bot()

    except Exception as e:
        logger.error("Exception in handle_restart_cmd():", e)
        await msg.edit(e, reply_markup=CLOSE_MARKUP)


@Bot.on_message(filters.command('logs') & filters.private & filters.user(USER_IDS))
async def handle_logs_cmd(client: Client, message: Message):
    file_name = f"{client.name} logs.txt"
    
    await message.reply_chat_action(ChatAction.UPLOAD_DOCUMENT)
    
    try:
        file = await write_logs_to_file(temp_file=file_name)
    
        await client.send_document(chat_id=message.from_user.id, document=file, reply_markup=CLOSE_MARKUP)
        
    except Exception as e:
        print(e)
    
    finally:
        try:
            await remove_tmp_file(file)
        except: pass

