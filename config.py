#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#

import os
from os import environ, getenv
import logging
from logging.handlers import RotatingFileHandler
from pyrogram import filters
from database.database import db # Updated import

# MehediYT69
# --------------------------------------------
# Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "7598604465:AAEhQdgJslNACsF2NDkGVEjYZno-vWliEwk")
APP_ID = int(os.environ.get("APP_ID", "22922577"))
API_HASH = os.environ.get("API_HASH", "ff5513f0b7e10b92a940bd107e1ac32a")
#--------------------------------------------

CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002659351510"))  # Your db channel Id
OWNER = os.environ.get("OWNER", "Raaaaavi")  # Owner username without @
OWNER_ID = int(os.environ.get("OWNER_ID", "1047253913"))  # Owner id
#--------------------------------------------
PORT = os.environ.get("PORT", "8080")
#--------------------------------------------
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://erenyeagermikasa84:pkbOXb3ulzi9cEFd@cluster0.ingt8mt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DATABASE_NAME", "Cluster0")
# --------------------------------------------
FSUB_LINK_EXPIRY = int(getenv("FSUB_LINK_EXPIRY", "30"))  # 0 means no expiry
BAN_SUPPORT = os.environ.get("BAN_SUPPORT", "https://t.me/+IIgB6RgivTI2NzA1")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "200"))
# --------------------------------------------
START_PIC = os.environ.get("START_PIC", "https://telegra.ph/file/ec17880d61180d3312d6a.jpg")
FORCE_PIC = os.environ.get("FORCE_PIC", "https://telegra.ph/file/e292b12890b8b4b9dcbd1.jpg")

# --------------------------------------------
# List of images for random selection in /start, /help, /about
RANDOM_IMAGES = [
    "https://telegra.ph/file/4414fb4d9e5fc36b65dc3-226143890200f06482.jpg",
    "https://telegra.ph/file/5e8d5c2ffbca4b9fa8c55-2b761e82504f6d8775.jpg",
    "https://telegra.ph/file/66c4adb1cf48ad68f3e31-81b19189a88625a39d.jpg",
    "https://telegra.ph/file/917c9567c4bb6da7c6db8-f7339d7b2e93398c8d.jpg",
    "https://telegra.ph/file/e7d8001a5813aa0bf8cef-f1ea2f9acd19c8c33b.jpg",
    "https://telegra.ph/file/415824c578ecf968a0c97-415f6bd1d2f2288c37.jpg",
    "https://telegra.ph/file/145eb941c14244ba7d25d-8cc9e293f41a01e04a.jpg",
    "https://telegra.ph/file/7388e3b2d3578ca9b596b-ae32749fd31e3f5bc0.jpg",
    "https://telegra.ph/file/0b7be04643304a2ebcc6c-0587c187997cf914a7.jpg",
    "https://telegra.ph/file/3f5e586ea5bbec365d779-0dedabf922fe53e191.jpg",
    "https://telegra.ph/file/c94cffc02557fb0f11098-69ea5789dd37e12834.jpg",
    "https://telegra.ph/file/5d79104e8468436552663-2bcd118f9816175500.jpg",
    "https://telegra.ph/file/479b4d3467abf19b6b7a8-79e46663286d728dbc.jpg",
    "https://telegra.ph/file/69e42d76add43f00c55ab-e7276303644245a02b.jpg",
    "https://telegra.ph/file/5cd3f2dd31d0c104d738f-b5176fcaaf1d27c86b.jpg",
    "https://telegra.ph/file/8aea25f56068077fb9a6e-7c3196d90da6c4c137.jpg",
    "https://telegra.ph/file/e91f8620c6042c521b624-5c66a3ccffd8b58b35.jpg",
    "https://telegra.ph/file/59e48aaffa4f757f9c91d-266c89b777ae2c1f9c.jpg",
    "https://telegra.ph/file/0bed23372a01242cc4bd5-119156af63830625cf.jpg",
    "https://telegra.ph/file/7baf42b4bf222dfa8397f-8539ff06db4ae8af3f.jpg",
    "https://telegra.ph/file/a43b2e1935d6c3afadb05-3efb6228df4c8adfaa.jpg",
    "https://telegra.ph/file/703cac9dc03549c0e86d5-6975e10193fbe45a01.jpg",
    "https://telegra.ph/file/e8effd37463cac5087133-4ed8bde82c6537edfa.jpg",
    "https://telegra.ph/file/617b82cf932512af1c418-c82535ace2753cb4c6.jpg",
    "https://telegra.ph/file/bf050a785e9777c7b999b-80b87ca2b0b9af4591.jpg",
    "https://telegra.ph/file/a9916e4561bb1ade528bd-fef1aaa186f0714005.jpg",
    "https://telegra.ph/file/0c807d34c9f3ef5cd5e3e-0830fca9a852b068f5.jpg",
    "https://telegra.ph/file/f8eefbda1f3d3e87d8565-3679d05921b1cbfd65.jpg",
    "https://telegra.ph/file/7a5c115fae6a6bcd1a681-c1d20a8d1ecc737d34.jpg",
    "https://telegra.ph/file/a92688b73fc89de2fc153-0883dcd1a567ec166e.jpg",
    "https://telegra.ph/file/7245907ecd1d5e32863cb-b99b8c5e963cc68324.jpg",
    "https://telegra.ph/file/8396534567bfaee71574f-bf7a419d673fe97bb2.jpg",
    "https://telegra.ph/file/63f8c0e0cd763be4dc204-cff77323f000112b96.jpg",
    "https://telegra.ph/file/8f65f3de13499c07e83bb-e854395ff12cb99fde.jpg",
    "https://telegra.ph/file/e56d10f3a526cd74a5d9d-90c76937bfbdf72c97.jpg",
    "https://telegra.ph/file/f4603e9c4266640e79678-7af3ebbabc913c7a02.jpg",
    "https://telegra.ph/file/aeb6851cf9cd86017d861-3ce10b0c32acd81045.jpg",
    "https://telegra.ph/file/2fc3974226c01fa438f4b-9b046d82bf8cd60efe.jpg",
    "https://telegra.ph/file/d5f3de3ec8f2bf7e06eaf-711b48e815e351ab1e.jpg",
    "https://telegra.ph/file/de276b83a9db197110b01-e8fd8829ec4af1b590.jpg",
    "https://telegra.ph/file/cce259cca9ffdef0695b0-75ca0212bb82496e30.jpg",
    "https://telegra.ph/file/de2a020446f873f451131-ac9f9e028b637a3c68.jpg",
    "https://telegra.ph/file/7595bc5e1c8cf57c9abd8-8ec90dd444fcf370c9.jpg",
    "https://telegra.ph/file/b0225917b1986dcc1dee2-da7a59f81124cd6e7a.jpg",
    "https://telegra.ph/file/88c8a15550365a7666aff-0cec62df3b958efd2a.jpg",
    "https://telegra.ph/file/bb0cec3364900a5d19fe3-9b52048d73468da45b.jpg",
    "https://telegra.ph/file/ab8c5167306854885712a-4699a010e442672ef0.jpg",
    "https://telegra.ph/file/0e1d1fb09336ce4472e94-c3232af883ea4b05c7.jpg",
    "https://telegra.ph/file/5e26db36ad034591914e1-196f8e52b1095f9eef.jpg",
    "https://telegra.ph/file/7e6e5f45dc78eca2d7ed2-badb68be7337c3082a.jpg",
    "https://telegra.ph/file/7441eb83ed69c2cc7299c-9dcada3341f57087b7.jpg",
    "https://telegra.ph/file/11e041620b9da13b94298-af0d1aae75c15f8517.jpg",
    "https://telegra.ph/file/8f5fb15110c8f4671e541-5999f0ad11af309726.jpg",
    "https://telegra.ph/file/895acbe821a7511ce323f-8f688f28f93e108cb3.jpg",
    "https://telegra.ph/file/313e4bbdbe6d8824dc722-e3520e8b91b70b6b6c.jpg",
    "https://telegra.ph/file/2709c5177c28477534bd7-1a64cf7d2c5196129a.jpg",
    "https://telegra.ph/file/edfc82724b2f0912a93b7-9a4c4c3ebc4f3763a6.jpg",
    "https://telegra.ph/file/47b9697c4ea307838adc1-8107ab2ffcc99e2e0c.jpg",
    "https://telegra.ph/file/5e7bec9860f32de495359-7e1349358df4e424ec.jpg",
    "https://telegra.ph/file/6ead9daabe54b91eab70a-5b3efb4222f8b6f747.jpg",
    "https://telegra.ph/file/466843b5cc6f5b85bd11e-6a306998514b84cb50.jpg",
    "https://telegra.ph/file/56dd0e678321b52d06a30-7e318251ff5a360fe8.jpg",
    "https://telegra.ph/file/627cd31179d8d02386e91-ef43b6f461362cbf8c.jpg",
    "https://telegra.ph/file/657602b7674627b13fa84-c1ba88aca3f1a3b2c9.jpg",
    "https://telegra.ph/file/5f427fddfa0b02d266f49-b66f03a52b605fd06c.jpg",
    "https://files.catbox.moe/3mtgb2.jpg",
    "https://files.catbox.moe/yly8lj.jpg",
    "https://i.ibb.co/N6rTvZXG/x.jpg",
    "https://i.ibb.co/pB8SMVfz/x.png",
    "https://i.ibb.co/F4ytZfyG/x.jpg",
    "https://files.catbox.moe/12x54p.jpg",
    "https://files.catbox.moe/gknros.jpg",
    "https://files.catbox.moe/hbxlc5.jpg",
    "https://files.catbox.moe/vyro5k.jpg",
    "https://files.catbox.moe/amw0s9.jpg",
    "https://files.catbox.moe/grdfu6.jpg",
    "https://files.catbox.moe/0c3vdv.jpg",
    "https://files.catbox.moe/j5jj97.jpg",
    "https://files.catbox.moe/dp11qk.jpg",
    "https://files.catbox.moe/6xvysm.jpg",
    "https://files.catbox.moe/naahka.jpg",
    "https://files.catbox.moe/k3gmp4.jpg",
    "https://files.catbox.moe/wwvshg.jpg",
    "https://files.catbox.moe/roj8a1.jpg",
    "https://files.catbox.moe/0z4rcb.jpg",
    "https://files.catbox.moe/0hvbzu.jpg",
    "https://files.catbox.moe/ooziqn.jpg",
    "https://files.catbox.moe/oglgps.jpg"
    
]

MESSAGE_EFFECT_IDS = [
    5104841245755180586,  # 🔥
    5107584321108051014,  # 👍
    5044134455711629726,  # ❤️
    5046509860389126442,  # 🎉
    5104858069142078462,  # 👎
    5046589136895476101,  # 💩
]


SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "linkshortify.com")
SHORTLINK_API = os.environ.get("SHORTLINK_API", "")
TUT_VID = os.environ.get("TUT_VID", "https://t.me/hwdownload/3")
SHORT_MSG = "<b>⌯ Here is Your Download Link, Must Watch Tutorial Before Clicking On Download...</b>"

SHORTENER_PIC = os.environ.get("SHORTENER_PIC", "https://telegra.ph/file/ec17880d61180d3312d6a.jpg")
# --------------------------------------------

# --------------------------------------------
HELP_TXT = os.environ.get("HELP_TXT","<b><blockquote>ᴛʜɪs ɪs ᴀɴ ғɪʟᴇ ᴛᴏ ʟɪɴᴋ ʙᴏᴛ ᴡᴏʀᴋ ғᴏʀ @Culturedteluguweeb\n\n❏ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs\n├/start : sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ\n├/about : ᴏᴜʀ Iɴғᴏʀᴍᴀᴛɪᴏɴ\n└/help : ʜᴇʟᴘ ʀᴇʟᴀᴛᴇᴅ ʙᴏᴛ\n\n sɪᴍᴘʟʏ ᴄʟɪᴄᴋ ᴏɴ ʟɪɴᴋ ᴀɴᴅ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ᴊᴏɪɴ ʙᴏᴛʜ ᴄʜᴀɴɴᴇʟs ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ᴛʜᴀᴛs ɪᴛ.....!</blockquote></b>")

ABOUT_TXT = os.environ.get("ABOUT_TXT","<b><blockquote>◈ ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ : <a href=https://t.me/CulturedTeluguweeb> ᴄᴜʟᴛᴜʀᴇᴅ ᴡᴇᴇʙ </a>\n◈ ᴏɴɢᴏɪɴɢ ᴄʜᴀɴɴᴇʟ : <a href=https://t.me/+BiVvkpD5ieIxZTNl>ᴏɴɢᴏɪɴɢ ᴄᴛᴡ </a>\n◈ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ᴀɴɪᴍᴇꜱ : <a href=https://t.me/+uCZlBWrgKCMyYmI1>ᴄᴛᴡ ᴀɴɪᴅᴇx</a></blockquote></b>")

# --------------------------------------------
START_MSG = os.environ.get("START_MESSAGE", "<blockquote><b> 𝐇𝐈 {first}✨ Cᴏᴍᴇ ғᴏʀ ᴛʜᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ, ᴅᴏɴ'ᴛ ᴍɪss ᴍʏ ꜰɪʟᴇꜱ! <blockquote></b>\n<blockquote> I'ᴍ 𝐓ʜᴇ Uʟᴛɪᴍᴀᴛᴇ Fɪʟᴇ Sʜᴀʀɪɴɢ Bᴏᴛ! .</blockquote></b>")

FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "<blockquote><b>ʜᴇʟʟᴏ {first}</b></blockquote>\n\n<blockquote><b>ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ᴀɴᴅ ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ʀᴇʟᴏᴀᴅ button ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛᴇᴅ ꜰɪʟᴇ.</b></blockquote>")

CMD_TXT = """<blockquote><b>» ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs:</b></blockquote>

<b>›› /start :</b> sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ & ɢᴇᴛ ᴘᴏsᴛs
<b>›› /batch :</b> ᴄʀᴇᴀᴛᴇ ʟɪɴᴋs ғᴏʀ ᴍᴜʟᴛɪᴘʟᴇ ᴘᴏsᴛs
<b>›› /custom_batch :</b> ᴄʀᴇᴀᴛᴇ ᴄᴜsᴛᴏᴍ ʙᴀᴛᴄʜ ғʀᴏᴍ ᴄʜᴀɴɴᴇʟ/ɢʀᴏᴜᴘ
<b>›› /genlink :</b> ᴄʀᴇᴀᴛᴇ ʟɪɴᴋ ғᴏʀ ᴀ sɪɴɢʟᴇ ᴘᴏsᴛ
<b>›› /flink :</b> ꜱᴇᴛ ᴀᴜᴛᴏ ʙᴀᴛᴄʜ ꜰᴏʀᴍᴀᴛ
<b>›› /forcesub :</b> ɢᴇᴛ ᴀʟʟ ғᴏʀᴄᴇ sᴜʙ sᴇᴛᴛɪɴɢs
<b>›› /admin :</b> ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴍᴀɴᴀɢᴇ ᴀᴅᴍɪɴs (ᴀᴅᴅ/ʀᴇᴍᴏᴠᴇ/ʟɪsᴛ)
<b>›› /user :</b> ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ɢᴇᴛ ᴜsᴇʀ-ʀᴇʟᴀᴛᴇᴅ ᴛᴏᴏʟs
<b>›› /auto_delete :</b> ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ sᴇᴛ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇʀ
<b>›› /fsettings :</b> ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴍᴀɴᴀɢᴇ ғᴏʀᴄᴇ sᴜʙsᴄʀɪᴘᴛɪᴏɴs
<b>›› /premium_cmd :</b> ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴍᴀɴᴀɢᴇ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs
<b>›› /broadcast_cmd :</b> ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ ᴍᴇssᴀɢᴇs
<b>›› /myplan :</b> ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ sᴛᴀᴛᴜs & ᴅᴇᴛᴀɪʟs
<b>›› /count :</b> ᴛʀᴀᴄᴋ sʜᴏʀᴛɴᴇʀ ᴄʟɪᴄᴋs & ᴀɴᴀʟʏᴛɪᴄs"""

CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION","<b><blockquote>• ᴘᴏᴡᴇʀᴇᴅ ʙʏ @Culturedteluguweeb</blockquote></b>")
# --------------------------------------------
# Set true if you want Disable your Channel Posts Share button
# --------------------------------------------
BOT_STATS_TEXT = "<b>BOT FUCKTIME</b>\n{uptime}"
USER_REPLY_TEXT = "ʙᴀᴋᴋᴀ ! ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ꜱᴇɴᴘᴀɪ!!"

# ==========================(BUY PREMIUM)====================#
OWNER_TAG = os.environ.get("OWNER_TAG", "")
UPI_ID = os.environ.get("UPI_ID", "yourname@upi")  # Replace with your valid UPI ID
QR_PIC = os.environ.get("QR_PIC", "")
SCREENSHOT_URL = os.environ.get("SCREENSHOT_URL", "")
# --------------------------------------------
# Time and its price
# 7 Days
PRICE1 = os.environ.get("PRICE1", "0 rs")
# 1 Month
PRICE2 = os.environ.get("PRICE2", "60 rs")
# 3 Month
PRICE3 = os.environ.get("PRICE3", "150 rs")
# 6 Month
PRICE4 = os.environ.get("PRICE4", "280 rs")
# 1 Year
PRICE5 = os.environ.get("PRICE5", "550 rs")

# ====================(END)========================#

# Default settings (loaded dynamically in bot.py)
PROTECT_CONTENT = False
HIDE_CAPTION = False
DISABLE_CHANNEL_BUTTON = True
BUTTON_NAME = None
BUTTON_LINK = None

# Function to update settings (used by file_settings.py)
async def update_setting(setting_name, value):
    await db.update_setting(setting_name, value)
    # Update local variables (optional, for immediate use)
    global PROTECT_CONTENT, HIDE_CAPTION, DISABLE_CHANNEL_BUTTON, BUTTON_NAME, BUTTON_LINK
    if setting_name == "PROTECT_CONTENT":
        PROTECT_CONTENT = value
    elif setting_name == "HIDE_CAPTION":
        HIDE_CAPTION = value
    elif setting_name == "DISABLE_CHANNEL_BUTTON":
        DISABLE_CHANNEL_BUTTON = value
    elif setting_name == "BUTTON_NAME":
        BUTTON_NAME = value
    elif setting_name == "BUTTON_LINK":
        BUTTON_LINK = value

# Function to get all settings (used to display in /fsettings)
def get_settings():
    return {
        "PROTECT_CONTENT": PROTECT_CONTENT,
        "HIDE_CAPTION": HIDE_CAPTION,
        "DISABLE_CHANNEL_BUTTON": DISABLE_CHANNEL_BUTTON,
        "BUTTON_NAME": BUTTON_NAME,
        "BUTTON_LINK": BUTTON_LINK
    }

LOG_FILE_NAME = "animelordbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)

# Admin filter to check if user is an admin or owner
async def admin_filter(_, __, message):
    admin_ids = await db.get_all_admins()
    return message.from_user.id in admin_ids or message.from_user.id == OWNER_ID

admin = filters.create(admin_filter)

#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#
