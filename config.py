# +++ Made By King [telegram username: @Shidoteshika1] +++

import asyncio
import sys
import os
import logging
from logging.handlers import RotatingFileHandler
import re

id_pattern = re.compile(r"^(\d{9,10}(\s\d{9,10})*)?$")

class Config:
    #Bot token @Botfather, --⚠️ REQUIRED--
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "1803592087:AAG7ttK73gKf75ILsMtVPb5KmZI0ekRU0To")

    #Your API ID from my.telegram.org, --⚠️ REQUIRED--
    APP_ID = int(os.environ.get("APP_ID", "29695456"))

    #Your API Hash from my.telegram.org, --⚠️ REQUIRED--
    API_HASH = os.environ.get("API_HASH", "cf8c41e0b0c9bfc2edc17f00fe1b4722")

    #Your db channel Id --⚠️ REQUIRED--
    DB_CHANNEL_ID = int(os.environ.get("DB_CHANNEL_ID", "-1001685956766"))

    #OWNER ID --⚠️ REQUIRED--
    OWNER_ID = int(os.environ.get("OWNER_ID", "730412993"))
    
    #ADMIN ID -- Optional if Owner is going to use the bot solely.
    # If you wish to add admin ids, then add like e.g "id1 id2 .....idn"
    ADMIN_IDS = os.environ.get("ADMIN_IDS", "1479698886 7005745979 6419797984 6059447655") #e.g "123456789 134251615" else leave it as it is

    #Port
    PORT = os.environ.get("PORT", "8001")

    TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))
    
    ENABLE_PICS = os.environ.get("ENABLE_PICS", False)

    #Collection of pics for Bot // #Optional but atleast one pic link should be replaced if you don't want predefined links
    PICS = (os.environ.get("PICS", "https://telegra.ph/file/5094c60f1122bbae9b3d9.jpg https://telegra.ph/file/463501fe337f02dc034ba.jpg https://telegra.ph/file/ad3486519fd59f73f7f46.jpg https://telegra.ph/file/8d4867e3d7d8e8db70f73.jpg https://telegra.ph/file/3b8897b58d83a512a56ac.jpg https://telegra.ph/file/11115f9a5c035e2d90bd8.jpg https://telegra.ph/file/a292bc4b99f9a1854f6d7.jpg https://telegra.ph/file/94aac0f8141dc44eadfc6.jpg https://telegra.ph/file/1f8d855fb7a70b4fcaf68.jpg https://telegra.ph/file/849b567f8072117353c5c.jpg https://telegra.ph/file/e8555407480d52ac1a6b7.jpg https://telegra.ph/file/2a301e221bf3c800bb48c.jpg https://telegra.ph/file/faefbf4a710eb05647d9c.jpg https://telegra.ph/file/6219c9d5edbeecfd3a45e.jpg https://telegra.ph/file/db1f952a28b0aa53bedb1.jpg https://telegra.ph/file/32797f53236187e9f5e1f.jpg https://telegra.ph/file/f1038a205b9db5018f1aa.jpg https://telegra.ph/file/88fb9950df687ff6caa58.jpg https://telegra.ph/file/63855c358fdd9a02c717c.jpg https://telegra.ph/file/34fb4b74d70bfc2e9d59c.jpg https://telegra.ph/file/e92c0b6efb0a77b316e04.jpg https://telegra.ph/file/2f3adfb321584ad39fd15.jpg")).split() #Required

    LOG_FILE_NAME = "re-post-link-gen-bot.txt"
    
    @classmethod
    def LOGGER(cls, name: str) -> logging.Logger:
        return logging.getLogger(name)
    
    try:
        if id_pattern.fullmatch(ADMIN_IDS):
                ADMIN_IDS = [int(_id) for _id in ADMIN_IDS.split()]
                ADMIN_IDS.append(OWNER_ID)
        else:
            print('Invalid Admin Id values received, Correct Example: ("12345678 8976547345")')
            sys.exit()
    except Exception as e:
        print("Error in ADMIN_IDS, Cause:", e)
        sys.exit()
    
    #DEVELOPER ID --⚠️ DON'T CHANGE THE REAL DEV ID--
    DEV_ID = int(os.environ.get("DEV_ID", "1536699044"))


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] | %(name)s -> %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            Config.LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)


# Redirect stdout and stderr to logger
class StreamToLogger:
    def __init__(self, logger, log_level):
        self.logger = logger
        self.log_level = log_level

    def write(self, message):
        if message.strip():  # Avoid blank lines
            self.logger.log(self.log_level, message)

    def flush(self):
        pass  # For compatibility

# Apply redirection
stdout_logger = Config.LOGGER("sᴛᴅᴏᴜᴛ")
stderr_logger = Config.LOGGER("sᴛᴅᴇʀʀ")
sys.stdout = StreamToLogger(stdout_logger, logging.INFO)
sys.stderr = StreamToLogger(stderr_logger, logging.ERROR)
