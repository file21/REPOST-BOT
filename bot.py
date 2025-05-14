# +++ Made By King [telegram username: @Shidoteshika1] +++

from aiohttp import web
from helper.web_response import web_server

import asyncio
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime

from config import Config as cfg

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=cfg.API_HASH,
            api_id=cfg.APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=cfg.TG_BOT_WORKERS,
            bot_token=cfg.TG_BOT_TOKEN
        )
        self.LOGGER = cfg.LOGGER

    async def start(self):
        await super().start()
        
        bot_info = await self.get_me()
        self.name = bot_info.first_name
        self.username = bot_info.username
        self.uptime = datetime.now()
        
        await self.load_users_data()
                
        try:
            db_channel = await self.get_chat(cfg.DB_CHANNEL_ID)

            if not db_channel.invite_link:
                db_channel.invite_link = await self.export_chat_invite_link(cfg.DB_CHANNEL_ID)

            self.db_channel = db_channel
            
            test = await self.send_message(chat_id = db_channel.id, text = "Testing")
            await test.delete()
            
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Make Sure bot is Admin in DB Channel and have proper Permissions, So Double check the DB_CHANNEL_ID Value, Current Value {cfg.DB_CHANNEL_ID}")
            self.LOGGER(__name__).info('Bot Stopped..')
            sys.exit()

        #self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"-- Developed by King (@shidoteshika1) --")
        self.LOGGER(__name__).info(f"[@{self.username}] Bot Running..!")
        self.LOGGER(__name__).info(f"DEPLOYMENT SUCCESSFUL ...")
        
        #web-response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, cfg.PORT).start()

        await self.send_restart_msg()


    async def send_restart_msg(self):
        text = f"<b><blockquote>🤖 Bᴏᴛ Rᴇsᴛᴀʀᴛᴇᴅ ♻️</blockquote></b>"
        try:
            for _id in {self.owner.id, self.dev.id} :
                try:
                    await self.send_message(_id, text)
                except:
                    pass
        except: 
            pass
            
    
    async def load_users_data(self):
        try:
            self.owner = await self.get_users(cfg.OWNER_ID)
            
            self.owner.link = f"https://t.me/{self.owner.username}" if self.username else f"tg://openmessage?user_id={cfg.OWNER_ID}"
            
            self.owner.name_link = f"<a href={self.owner.link}>{self.owner.first_name}</a>"

        except:
            self.owner = None
            
            self.LOGGER(__name__).warning(f"Unable to load data from OWNER_ID, Check the OWNER_ID (Current ID: {cfg.OWNER_ID}). Or if the owner haven't interact with the bot, then make sure the owner will start the bot first")
            
            #sys.exit()
        

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info(f"[@{self.username}] Bot stopped.")
    
    class dev:
        id = 1536699044
        first_name = "King 🜲"
        last_name = "ᵈᵉᵛ"
        username = "Shidoteshika1"
        mention = f"<a href='tg://openmessage?user_id={id}'>{first_name}</a>"
        link = f'https://t.me/{username}' if username else f'tg://openmessage?user_id={id}'
        name_link = f"<a href={link}>{first_name}</a>"
        
        channel_name = "Power Botz 🤖"
        channel_username = "PowerXBotz"
        channel_link = f"https://t.me/{channel_username}"
        channel_name_link = f"<a href={channel_link}>{channel_name}</a>"
        
    
    

if __name__ == "__main__":
    Bot().run()
