# +++ Made By King [telegram username: @Shidoteshika1] +++


import random
import asyncio
from bot import Bot
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.enums import ParseMode, ChatAction
from config import Config as cfg
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, ReplyKeyboardMarkup, ReplyKeyboardRemove
from helper.message_operations import encode, decode, get_messages
import re

validate_link = re.compile(r"^https://t.me/(.+)\?start=(.+)$")

new_post_link = "https://t.me/{bot_username}?start={encode_msg}"

CANCEL_TXT = "ᴄᴀɴᴄᴇʟ"
STOP_TXT = "sᴛᴏᴘ"

CLOSE_BUTTON = InlineKeyboardButton("🔒 ᴄʟᴏsᴇ", "close")
CLOSE_MARKUP = InlineKeyboardMarkup([[CLOSE_BUTTON]])


#=========================================================================================================
#=========================================================================================================
#=========================================================================================================


async def create_replyMarkup(message: Message, text:str, keyboard_txt:str=CANCEL_TXT):
    return await message.reply(
        text=text,
        disable_web_page_preview=True,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[keyboard_txt]],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )


async def make_inline_buttons(text: str) -> ReplyKeyboardMarkup:
    inline_buttons = []
    button_lines = text.splitlines()

    for line in button_lines:
        tmp_buttons = []
        buttons_nums = line.split(' | ')

        for button in buttons_nums:
            try:
                button_txt,  button_link = button.split(' - ') 
            except Exception as e:
                print(f"! Exception in function (make_inline_button): {e}")
                return None
            
            tmp_buttons.append(InlineKeyboardButton(text=button_txt, url=button_link))

        inline_buttons.append(tmp_buttons)
    
    return InlineKeyboardMarkup(inline_buttons)


async def get_posted_messages(client:Client, encode_msg:str):
                
    if not len(encode_msg)>7:
        return
    

    string = await decode(encode_msg)
    argument = string.split("-")
    
    if len(argument) == 3:
        try:
            start = int(int(argument[1]) / abs(client.db_channel.id))
            end = int(int(argument[2]) / abs(client.db_channel.id))
        except Exception as e:
            print("error in start, end :", e)
            return
                
        if start <= end:
            ids = range(start,end+1)
        else:
            ids = []
            i = start
            while True:
                ids.append(i)
                i -= 1
                if i < end:
                    break
                        
    elif len(argument) == 2:
        try: ids = [int(int(argument[1]) / abs(client.db_channel.id))]
        except Exception as e: 
            print("error in ids : ", e)
            return

    try: 
        messages = await get_messages(client, ids)
    except Exception as e:
        print("Something went wrong :", e) 
        return 
    
    return messages



async def generate_link(client: Client, bot_username: str, first_msg_id:int, last_msg_id: int):
    if first_msg_id == last_msg_id:
        string = f"get-{first_msg_id * abs(client.db_channel.id)}"
    else:
        string = f"get-{first_msg_id * abs(client.db_channel.id)}-{last_msg_id * abs(client.db_channel.id)}"
        
    base64_string = await encode(string)
    
    return new_post_link.format(bot_username=bot_username, encode_msg=base64_string)


async def copy_message(client:Client, message:Message):
    """try:
        post_msg = await msg.copy(chat_id=client.db_channel.id, disable_notification=True)
        await asyncio.sleep(0.5)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_msg = await msg.copy(chat_id=client.db_channel.id, disable_notification=True)
        await asyncio.sleep(0.5)"""
    
    try:
        post_msg = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
        await asyncio.sleep(0.5)
        
    except FloodWait as e:
        await asyncio.sleep(e.value)
        post_msg = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
        await asyncio.sleep(0.5)
    
    return post_msg
        

async def re_post_messages(client: Client, message: Message, bot_username: str, posted_messages: list[Message], new_messages: list[Message]):
    
    tmp = await message.reply("**__Pʀᴏᴄᴇssɪɴɢ...__**")
    
    posted_first_msg_id = posted_last_msg_id = None
    new_first_msg_id = new_last_msg_id = None
    
    for idx, msg in enumerate(posted_messages[:-1]):
        post_msg = await copy_message(client, msg)

        if idx == 0:
            posted_first_msg_id = post_msg.id
    
    for idx, msg in enumerate(new_messages):
        post_msg = await copy_message(client, msg)
        
        if idx == 0:
            new_first_msg_id = post_msg.id
        
        if idx == len(new_messages) - 1:
            new_last_msg_id = post_msg.id
    
    try:
        post_msg = await copy_message(client, posted_messages[-1])
        posted_last_msg_id = post_msg.id
        
    except Exception as e:
        error = f"Eʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ sᴇɴᴅɪɴɢ ʟᴀsᴛ ᴍᴇssᴀɢᴇ, Cᴀᴜsᴇ: {e}"
        print(error)
        return await message.reply(f"**{error}**")


    all_files_link = await generate_link(client, bot_username, posted_first_msg_id, posted_last_msg_id)
    new_files_link = await generate_link(client, bot_username, new_first_msg_id, new_last_msg_id)
    
    season_txt, latest_episode_txt = "SEASON", "LATEST EPISODE ONLY"
    
    reply_msg = f"""{season_txt} - {all_files_link}\n{latest_episode_txt} - {new_files_link}"""

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(season_txt, url=all_files_link)],
        [InlineKeyboardButton(latest_episode_txt, url=new_files_link)]
    ])
    
    await tmp.delete()
    
    await message.reply(
        text=f"<code>{reply_msg}</code>", 
        disable_web_page_preview=True, 
        reply_markup=reply_markup
    )
    


# Dictionary to store user-specific file collection
active_users = {}

async def collect_user_files(client: Client, message: Message):
    user_id, chat_id = message.from_user.id, message.chat.id
    
    # Initialize empty file list
    active_users[user_id] = []

    # Prompt the user
    msg_reply = await create_replyMarkup(message, text="**Pʟᴇᴀsᴇ, sᴇɴᴅ ʏᴏᴜʀ ғɪʟᴇs**\n<blockquote>Sᴇɴᴅ sᴛᴏᴘ ᴛᴏ sᴛᴏᴘ ᴛʜᴇ ᴏᴘᴇʀᴀᴛɪᴏɴ</blockquote>", keyboard_txt=STOP_TXT)

    while True:
        try:
            # Wait for the next message (files or 'cancel')
            incoming_message = await client.listen(chat_id, timeout=300)  # Wait max 5 minutes

            # If the user sends 'cancel', stop collection
            if incoming_message.text and incoming_message.text == STOP_TXT:
                temp = await client.send_message(chat_id, "**Sᴛᴏᴘᴘᴇᴅ...**")
                
                await msg_reply.delete()
                await incoming_message.delete()
                
                await asyncio.sleep(1)
                await temp.delete()
                
                break

            # Handle media group (multiple files in one message)
            if incoming_message.media_group_id:
                media_messages = await client.get_media_group(chat_id, incoming_message.id)
                active_users[user_id].extend(media_messages)
                
            else:
                active_users[user_id].append(incoming_message)

        except asyncio.TimeoutError:
            temp = await client.send_message(chat_id, "Rᴇǫᴜᴇsᴛ ᴛɪᴍᴇᴅ ᴏᴜᴛ...")
            
            await msg_reply.delete()
            
            await asyncio.sleep(5)
            await temp.delete()
            
            break

    # Return collected messages
    return active_users.pop(user_id, [])


#=========================================================================================================
#=========================================================================================================
#=========================================================================================================



@Bot.on_message(filters.command("repost") & filters.private & filters.user(cfg.ADMIN_IDS))
async def re_post_command(client: Client, message: Message):

    msg_reply = await create_replyMarkup(message, text="**Sᴇɴᴅ Pʀᴇᴠɪᴏᴜs ᴘᴏsᴛ Lɪɴᴋ**")
    
    while True:
        
        response = await client.listen(chat_id=message.from_user.id, filters=filters.text)
        
        if response.text == CANCEL_TXT:
            await msg_reply.delete()
            await response.delete()
            
            temp = await message.reply("**Cᴀɴᴄᴇʟᴇᴅ...**")
            await asyncio.sleep(5)
            await temp.delete()

            return
        
        else:            
            link = validate_link.fullmatch(response.text)
            
            if link:
                await msg_reply.delete()
                await response.delete()
                
                bot_username, encode_msg = link.group(1), link.group(2)

                postd_msgs = await get_posted_messages(client, encode_msg)
                
                new_msgs = await collect_user_files(client, message)
                
                if not postd_msgs or not new_msgs:
                    temp = await message.reply("**Oᴘᴇʀᴀᴛɪᴏɴ ʜᴀʟᴛᴇᴅ...**")
                    await asyncio.sleep(5)
                    await temp.delete()
                    
                    return
                
                await re_post_messages(client, message, bot_username, postd_msgs, new_msgs)
                
                return
            
            else:
                await response.reply("**__Sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ᴘᴏsᴛ ʟɪɴᴋ__**", quote=True, reply_markup=CLOSE_MARKUP)
                
                continue
