#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#

import asyncio
import os
import random
import sys
import re
import string
import time
from datetime import datetime, timedelta
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatInviteLink, ChatPrivileges
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant, MediaEmpty
from bot import Bot
from config import *
from helper_func import *
from database.database import *
from database.db_premium import *

# Define emoji reactions and sticker
EMOJI_MODE = True
REACTIONS = ["👍", "😍", "🔥", "🎉", "❤️", "⚡"]
STICKER_ID = "CAACAgUAAxkBAAJFeWd037UWP-vgb_dWo55DCPZS9zJzAAJpEgACqXaJVxBrhzahNnwSHgQ"

# List of message effect IDs for random selection (Converted to integers)
MESSAGE_MESSAGE_EFFECT_IDS = [
    5104841245755180586,  5107584321108051014,
    5044134455711629726,
    5046509860389126642,
    5104858069142078462,
    5046589136895476101
]

BAN_SUPPORT = f"{BAN_SUPPORT}"
TUT_VID = f"{TUT_VID}"

# Cache for chat data to improve performance
chat_data_cache = {}

async def short_url(client: Client, message: Message, base64_string):
    try:
        prem_link = f"https://t.me/{client.username}?start=yu3elk{base64_string}"
        short_link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, prem_link)
        buttons = [
            [InlineKeyboardButton(text="ᴅɪᴡɴʟɪᴀᴅ", url=short_link), InlineKeyboardButton(text="ᴛᴜᴛɪʀɪᴀʟ", url=TUT_VID)],
            [InlineKeyboardButton(text="ᴘʀᴇᴍɪᴜᴍ", callback_data="premium")]
        ]
        await message.reply_photo(
            photo=SHORTENER_PIC,
            caption=SHORT_MSG.format(),
            reply_markup=InlineKeyboardMarkup(buttons),
            message_effect_id=random.choice(MESSAGE_MESSAGE_EFFECT_IDS)
        )
    except IndexError:
        pass

@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    is_premium = await is_premium_user(user_id)
    if EMOJI_MODE:
        await message.react(emoji=random.choice(REACTIONS), big=True)
    banned_users = await db.get_ban_users()
    if user_id in banned_users:
        return await message.reply_text(
            "ʏɪᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ғʀɪᴍ ᴜsɪɴɢ ᴛʜɪs ʙɪᴛ.\n\nᴄɪɴᴛᴀᴄᴛ sᴜᴘᴘɪʀᴛ ɪғ ʏɪᴜ ᴛʜɪɴᴋ ᴛʜɪs ɪs ᴀ ᴍɪsᴛᴀᴋᴇ.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ᴄɪɴᴛᴀᴄᴛ sᴜᴘᴘɪʀᴛ", url=BAN_SUPPORT)]])
        )
    if not await is_subscribed(client, user_id):
        return await not_joined(client, message)
    FILE_AUTO_DELETE = await db.get_del_timer()
    if not await db.present_user(user_id):
        try:
            await db.add_user(user_id)
        except:
            pass

    text = message.text
    if len(text) > 7:
        try:
            basic = text.split(" ", 1)[1]
            base64_string = basic[6:-1] if basic.startswith("yu3elk") else basic
            if not is_premium and user_id != OWNER_ID and not basic.startswith("yu3elk"):
                await short_url(client, message, base64_string)
                return
        except Exception as e:
            print(f"ᴇʀʀɪʀ ᴘʀɪᴄᴇssɪɴɢ sᴛᴀʀᴛ ᴘᴀʏʟɪᴀᴅ: {e}")
        string = await decode(base64_string)
        argument = string.split("-")
        ids = []
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = range(start, end + 1) if start <= end else list(range(start, end - 1, -1))
            except Exception as e:
                print(f"ᴇʀʀɪʀ ᴅᴇᴄɪᴅɪɴɢ ɪᴅs: {e}")
                return
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except Exception as e:
                print(f"ᴇʀʀɪʀ ᴅᴇᴄɪᴅɪɴɢ ɪᴅ: {e}")
                return
        # New animation messages for file request
        m = await message.reply_text("<blockquote><b>Checking...</b></blockquote>")
        await asyncio.sleep(0.4)
        await m.edit_text("<blockquote><b>Getting your files...</b></blockquote>")
        await asyncio.sleep(0.5)
        await m.delete()
        try:
            messages = await get_messages(client, ids)
        except Exception as e:
            await message.reply_text("sɪᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀɪɴɢ!")
            print(f"ᴇʀʀɪʀ ɢᴇᴛᴛɪɴɢ ᴍᴇssᴀɢᴇs: {e}")
            return
        animelord_msgs = []
        # Load settings dynamically before copying messages
        settings = await db.get_settings()
        PROTECT_CONTENT = settings.get('PROTECT_CONTENT', False)
        HIDE_CAPTION = settings.get('HIDE_CAPTION', False)
        DISABLE_CHANNEL_BUTTON = settings.get('DISABLE_CHANNEL_BUTTON', False)
        BUTTON_NAME = settings.get('BUTTON_NAME', None)
        BUTTON_LINK = settings.get('BUTTON_LINK', None)
        print(f"Copying message with PROTECT_CONTENT={PROTECT_CONTENT}, HIDE_CAPTION={HIDE_CAPTION}, DISABLE_CHANNEL_BUTTON={DISABLE_CHANNEL_BUTTON}")
        for msg in messages:
            caption = "" if HIDE_CAPTION else (
                CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html,
                                      filename=msg.document.file_name) if bool(CUSTOM_CAPTION) and bool(msg.document)
                else ("" if not msg.caption else msg.caption.html))
            reply_markup = None if DISABLE_CHANNEL_BUTTON or not msg.reply_markup else msg.reply_markup
            # Add custom button if BUTTON_NAME and BUTTON_LINK are set
            if BUTTON_NAME and BUTTON_LINK and not DISABLE_CHANNEL_BUTTON:
                custom_button = InlineKeyboardMarkup([[InlineKeyboardButton(BUTTON_NAME, url=BUTTON_LINK)]])
                reply_markup = custom_button if not reply_markup else InlineKeyboardMarkup(
                    reply_markup.inline_keyboard + custom_button.inline_keyboard
                )
            try:
                copied_msg = await msg.copy(chat_id=user_id, caption=caption, parse_mode=ParseMode.HTML,
                                            reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                animelord_msgs.append(copied_msg)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                copied_msg = await msg.copy(chat_id=user_id, caption=caption, parse_mode=ParseMode.HTML,
                                            reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                animelord_msgs.append(copied_msg)
            except Exception as e:
                print(f"ғᴀɪʟᴇᴅ ᴛɪ sᴇɴᴅ ᴍᴇssᴀɢᴇ: {e}")
                pass
        auto_delete_mode = await db.get_auto_delete_mode()  # Check auto-delete mode
        if auto_delete_mode and FILE_AUTO_DELETE > 0:  # Only proceed if mode is enabled and timer is positive
            notification_msg = await message.reply(
                f"ᴛʜɪs ғɪʟᴇ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ɪɴ {get_exp_time(FILE_AUTO_DELETE).lower()}.\n ᴘʟᴇᴀsᴇ sᴀᴠᴇ ᴏʀ ғᴏʀᴡᴀʀᴅ ɪᴛ ᴛᴏ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs ʙᴇғᴏʀᴇ ɪᴛ ɢᴇᴛs ᴅᴇʟᴇᴛᴇᴅ.\n ᴜsᴇ @Tfifiletolinkbot ғᴏʀ sᴛʀᴇᴀᴍ ᴀɴᴅ ғᴀsᴛ ᴅᴏᴡɴʟᴏᴀᴅ.",
                message_effect_id=random.choice(MESSAGE_MESSAGE_EFFECT_IDS)
            )
            await asyncio.sleep(FILE_AUTO_DELETE)
            for snt_msg in animelord_msgs:
                if snt_msg:
                    try:
                        await snt_msg.delete()
                    except Exception as e:
                        print(f"ᴇʀʀɪʀ ᴅᴇʟᴇᴛɪɴɢ ᴍᴇssᴀɢᴇ {snt_msg.id}: {e}")
            try:
                reload_url = f"https://t.me/{client.username}?start={message.command[1]}" if message.command and len(message.command) > 1 else None
                keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("ɢᴇᴛ ғɪʟᴇ ᴀɢᴀɪɴ!", url=reload_url)]]) if reload_url else None
                await notification_msg.edit(
                    "ʏɪᴜʀ ᴠɪᴅᴇɪ/ғɪʟᴇ ɪs sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ!\n\nᴄʟɪᴄᴋ ʙᴇʟɪᴡ ʙᴜᴛᴛɪɴ ᴛɪ ɢᴇᴛ ʏɪᴜʀ ᴅᴇʟᴇᴛᴇᴅ ᴠɪᴅᴇɪ/ғɪʟᴇ.",
                    reply_markup=keyboard,
                    message_effect_id=random.choice(MESSAGE_MESSAGE_EFFECT_IDS)
                )
            except Exception as e:
                print(f"ᴇʀʀɪʀ ᴜᴪᴅᴀᴛɪɴɢ ɴɪᴛɪғɪᴄᴀᴛɪɪɴ: {e}")
        return

    # Original animation messages for /start command
    m = await message.reply_text("<blockquote><b>ᴡᴇʟᴄɪᴍᴇ ᴛɪ ᴍʏ ʙɪᴛ.\nʜɪᴪᴇ ʏɪᴜ'ʀᴇ ᴅɪɪɴɢ ᴡᴇʟʟ...</b></blockquote>")
    await asyncio.sleep(0.4)
    await m.edit_text("<blockquote><b>ᴄʜᴇᴄᴋɪɴɢ...</b></blockquote>")
    await asyncio.sleep(0.5)
    await m.edit_text("<blockquote>🎊</blockquote>")
    await asyncio.sleep(0.5)
    await m.edit_text("<blockquote>⚡</blockquote>")
    await asyncio.sleep(0.5)
    await m.edit_text("<blockquote><b>sᴛᴀʀᴛɪɴɢ...</b></blockquote>")
    await asyncio.sleep(0.4)
    await m.delete()

    # Send sticker
    if STICKER_ID:
        m = await message.reply_sticker(STICKER_ID)
        await asyncio.sleep(1)
        await m.delete()

    # Send start message
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("ᴍօʀᴇ ᴄʜᴀɴɴᴇʟs", url="https://t.me/CulturedTeluguweeb")],
        [InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about"), InlineKeyboardButton("ʜᴇʟᴪ", callback_data="help")]
    ])
    try:
        await asyncio.sleep(0.5)
        selected_image = random.choice(RANDOM_IMAGES) if RANDOM_IMAGES else START_PIC
        await message.reply_photo(
            photo=selected_image,
            caption=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name if message.from_user.last_name else "",
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            message_effect_id=random.choice(MESSAGE_MESSAGE_EFFECT_IDS)
        )
    except Exception as e:
        print(f"ᴇʀʀɪʀ sᴇɴᴅɪɴɢ sᴛᴀʀᴛ ᴪʜɪᴛɪ: {e}")
        await asyncio.sleep(0.5)
        await message.reply_photo(
            photo=START_PIC,
            caption=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name if message.from_user.last_name else "",
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            message_effect_id=random.choice(MESSAGE_MESSAGE_EFFECT_IDS)
        )

async def not_joined(client: Client, message: Message):
    temp = await message.reply("<blockquote><b>ᴄʜᴇᴄᴋɪɴɢ sᴜʙsᴄʀɪᴪᴛɪɪɴ...</b></blockquote>")
    user_id = message.from_user.id
    buttons = []
    settings = await db.get_settings()
    count = 0
    try:
        all_channels = await db.show_channels()
        if not settings.get('FORCE_SUB_ENABLED', True) or not all_channels:
            await temp.delete()
            return await start_command(client, message)  # Bypass if force-sub disabled or no channels

        for total, chat_id in enumerate(all_channels, start=1):
            if await db.get_channel_temp_off(chat_id):  # Skip channels with temp_off=True
                continue
            mode = await db.get_channel_mode(chat_id)
            await message.reply_chat_action(ChatAction.TYPING)
            if not await is_sub(client, user_id, chat_id):
                try:
                    # Cache chat info
                    if chat_id in chat_data_cache:
                        data = chat_data_cache[chat_id]
                    else:
                        try:
                            data = await client.get_chat(chat_id)
                            chat_data_cache[chat_id] = data
                        except Exception as e:
                            logger.error(f"Failed to fetch chat {chat_id}: {e}")
                            if "USERNAME_NOT_OCCUPIED" in str(e):
                                await db.rem_channel(chat_id)  # Remove invalid channel from database
                                logger.info(f"Removed invalid channel {chat_id} from database")
                                continue
                            else:
                                raise e

                    name = data.title

                    # Generate proper invite link based on the mode
                    if mode == "on":
                        invite = await client.create_chat_invite_link(
                            chat_id=chat_id,
                            creates_join_request=True,
                            expire_date=datetime.utcnow() + timedelta(seconds=FSUB_LINK_EXPIRY) if FSUB_LINK_EXPIRY else None
                        )
                        link = invite.invite_link
                    else:
                        if data.username:
                            link = f"https://t.me/{data.username}"
                        else:
                            invite = await client.create_chat_invite_link(
                                chat_id=chat_id,
                                expire_date=datetime.utcnow() + timedelta(seconds=FSUB_LINK_EXPIRY) if FSUB_LINK_EXPIRY else None
                            )
                            link = invite.invite_link

                    buttons.append([InlineKeyboardButton(text=f"{name}", url=link)])
                    count += 1
                    await temp.edit(f"<blockquote><b>ᴄʜᴇᴄᴋɪɴɢ {count}...</b></blockquote>")
                except Exception as e:
                    logger.error(f"Error with chat {chat_id}: {e}")
                    continue  # Skip invalid channels instead of stopping
        if count == 0:  # All required channels are subscribed
            await temp.delete()
            return await start_command(client, message)

        try:
            buttons.append([InlineKeyboardButton(text='ᴄʜᴇᴄᴋ ᴀɢᴀɪɴ', callback_data="check_sub")])
        except IndexError:
            pass
        await message.reply_photo(
            photo=FORCE_PIC,
            caption=FORCE_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name if message.from_user.last_name else "",
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        logger.error(f"Final error in not_joined: {e}")
        await temp.edit(f"<blockquote><b>ᴇʀʀɪʀ, ᴄɪɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟɪᴪᴇʀ @Raaaaavi\nʀᴇᴀsɪɴ: {e}</b></blockquote>")
        await asyncio.sleep(5)  # Show error for 5 seconds
        await temp.delete()
        return await start_command(client, message)  # Proceed to start_command even if error occurs
    finally:
        await temp.delete()

@Bot.on_callback_query(filters.regex(r"^check_sub"))
async def check_sub_callback(client: Client, callback: CallbackQuery):
    user_id = callback.from_user.id
    message = callback.message
    if await is_subscribed(client, user_id):
        await message.delete()
        await start_command(client, callback.message)
    else:
        await callback.answer("You still haven't joined all required channels. Please join and try again.")
        await not_joined(client, message)

@Bot.on_message(filters.command('myplan') & filters.private)
async def check_plan(client: Client, message: Message):
    user_id = message.from_user.id
    status_message = await check_user_plan(user_id)
    await message.reply_text(status_message, message_effect_id=random.choice(MESSAGE_MESSAGE_EFFECT_IDS))

@Bot.on_message(filters.command('addPremium') & filters.private & admin)
async def add_premium_user_command(client, msg):
    if len(msg.command) != 4:
        await msg.reply_text(
            "<blockquote><b>ᴜsᴀɢᴇ:</b></blockquote>\n /addpremium <user_id> <time_value> <time_unit>\n\n"
            "<blockquote><b>ᴛɪᴍᴇ ᴜɴɪᴛs:\n"
            "s - sᴇᴄɪɴᴅs\n"
            "m - ᴍɪɴᴜᴛᴇs\n"
            "h - ʜɪᴜʀs\n"
            "d - ᴅᴀʏs\n"
            "y - ʏᴇᴀʀs\n\n"
            "ᴇxᴀᴍᴪʟᴇs:\n"
            "/addpremium 123456789 30 m - 30 ᴍɪɴᴜᴛᴇs\n"
            "/addpremium 123456789 2 h - 2 ʜɪᴜʀs\n"
            "/addpremium 123456789 1 d - 1 ᴅᴀʏ\n"
            "/addpremium 123456789 1 y - 1 ʏᴇᴀʀ</b></blockquote>",
            message_effect_id=random.choice(MESSAGE_MESSAGE_EFFECT_IDS)
        )
        return
    try:
        usermega_id = int(msg.command[1])
        time_value = int(msg.command[2])
        time_unit = msg.command[3].lower()
        expiration_time = await add_premium(user_id, time_value, time_unit)
        await msg.reply_text(
            f"ᴜsᴇʀ {user_id} ᴀᴅᴅᴇᴅ ᴀs ᴀ ᴪʀᴇᴍɪᴜᴍ ᴜsᴇʀ ғɪʀ {time_value} {time_unit}.\n"
            f"ᴇxᴪɪʀᴀᴛɪɪɴ ᴛɪᴍᴇ: {expiration_time}.",
            message_effect_id=random.choice(MESSAGE_MESSAGE_EFFECT_IDS)
        )
        await client.send_message(
            chat_id=user_id,
            text=(
                f"<blockquote><b>ᴪʀᴇᴍɪᴜᴍ ᴀᴄᴛɪᴠᴀᴛᴇᴅ!</b></blockquote>\n\n"
                f"<b>Yɪᴜ ʜᴀᴠᴇ ʀᴇᴄᴇɪᴠᴇᴅ ᴪʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss ғɪʀ {time_value} {time_unit}.</b>\n"
                f"<b>ᴇxᴪɪʀᴇs ɪɴ: {expiration_time}</b>"
            ),
            message_effect_id=random.choice(MESSAGE_MESSAGE_EFFECT_IDS)
        )
    except ValueError:
        await msg.reply_text("<blockquote><b>ɪɴᴠᴀʟɪᴅ ɪɴᴪᴜᴛ. ᴪʟᴇᴀsᴇ ᴇɴsᴜʀᴇ ᴜsᴇʀ ɪᴅ ᴀɴᴅ ᴛɪᴍᴇ ᴠᴀʟᴜᴇ ᴀʀᴇ ɴᴜᴍʙᴇʀs</b></blockquote>.",
                            message_effect_id=random.choice(MESSAGE_MESSAGE_EFFECT_IDS))
    except Exception as e:
        await msg.reply_text(f"ᴀɴ ᴇʀʀɪʀ ɪᴄᴄᴜʀʀᴇᴅ: {str(e)}", message_effect_id=random.choice(MESSAGE_MESSAGE_EFFECT_IDS))

@Bot.on_message(filters.command('remove_premium') & filters.private & admin)
async def pre_remove_user(client: Client, msg: Message):
    if len(msg.command) != 2:
        await msg.reply_text("<blockquote><b>ᴜsᴀɢᴇ:</b></blockquote> /remove_premium user_id",
                             message_effect_id=random.choice(MESSAGE_MESSAGE_EFFECT_IDS))
        return
    try:
        user_id = int(msg.command[1])
        await remove_premium(user_id)
        await msg.reply_text(f"<blockquote><b>ᴜsᴇʀ {user_id} ʜᴀs ʙᴇᴇɴ ʀᴇᴍɪᴠᴇᴅ.</b></blockquote>",
                             message_effect_id=random.choice(MESSAGE_MESSAGE_EFFECT_IDS))
    except ValueError:
        await msg.reply_text("ᴜsᴇʀ ɪᴅ ᴍᴜsᴛ ʙᴇ ᴀɴ ɪɴᴛᴇɢᴇʀ ɪʀ ɴɪᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ.",
                             message_effect_id=random.choice(MESSAGE_MESSAGE_EFFECT_IDS))

@Bot.on_message(filters.command('premium_users') & filters.private & admin)
async def list_premium_users_command(client, message):
    from pytz import timezone
    ist = timezone("Asia/Dhaka")
    premium_users_cursor = collection.find({})
    premium_user_list = ['ᴀᴄᴛɪᴠᴇ ᴪʀᴇᴍɪᴜᴍ ᴜsᴇʀs ɪɴ ᴅᴀᴛᴀʙᴀsᴇ:']
    current_time = datetime.now(ist)
    async for user in premium_users_cursor:
        user_id = user["user_id"]
        expiration_timestamp = user["expiration_timestamp"]
        try:
            expiration_time = datetime.fromisoformat(expiration_timestamp).astimezone(ist)
            remaining_time = expiration_time - current_time
            if remaining_time.total_seconds() <= 0:
                await collection.delete_one({"user_id": user_id})
                continue
            user_info = await client.get_users(user_id)
            username = user_info.username if user_info.username else "no username"
            mention = user_info.mention
            days, hours, minutes, seconds = (
                remaining_time.days,
                remaining_time.seconds // 3600,
                (remaining_time.seconds // 60) % 60,
                remaining_time.seconds % 60,
            )
            expiry_info = f"{days}d {hours}h {minutes}m {seconds}s left"
            premium_user_list.append(
                f"ᴜsᴇʀ ɪᴅ: {user_id}\n"
                f"ᴜsᴇʀ: @{username}\n"
                f"ɴᴀᴍᴇ: {mention}\n"
                f"ᴇxᴪɪʀʏ: {expiry_info}"
            )
        except Exception as e:
            premium_user_list.append(
                f"ᴜsᴇʀ ɪᴅ: {user_id}\n"
                f"ᴇʀʀɪʀ: ᴜɴᴀʙʟᴇ ᴛɪ ғᴇᴛᴄʜ ᴜsᴇʀ ᴅᴇᴛᴀɪʟs ({str(e)})"
            )
    if len(premium_user_list) == 1:
        await message.reply_text("ɴɪ ᴀᴄᴛɪᴠᴇ ᴪʀᴇᴍɪᴜᴍ ᴜsᴇʀs ғɪᴜɴᴅ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ.",
                                 message_effect_id=random.choice(MESSAGE_MESSAGE_EFFECT_IDS))
    else:
        await message.reply_text("\n\n".join(premium_user_list), parse_mode=None,
                                 message_effect_id=random.choice(MESSAGE_MESSAGE_EFFECT_IDS))

@Bot.on_message(filters.command("count") & filters.private & admin)
async def total_verify_count_cmd(client, message: Message):
    total = await db.get_total_verify_count()
    await message.reply_text(f"<blockquote><b>ᴛɪᴛᴀʟ ᴠᴇʀɪғɪᴇᴅ ᴛɪᴋᴇɴs ᴛɪᴅᴀʏ: {total}</b></blockquote>",
                             message_effect_id=random.choice(MESSAGE_MESSAGE_EFFECT_IDS))

@Bot.on_message(filters.command('commands') & filters.private & admin)
async def bcmd(bot: Bot, message: Message):
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟɪsᴇ", callback_data="close")]])
    await message.reply_text(text=CMD_TXT, reply_markup=reply_markup, quote=True,
                             message_effect_id=random.choice(MESSAGE_MESSAGE_EFFECT_IDS))

@Bot.on_message(filters.command('premium_cmd') & filters.private & admin)
async def premium_cmd(bot: Bot, message: Message):
    reply_text = (
        "<blockquote><b>ᴜsᴇ ᴛʜᴇsᴇ ᴄɪᴍᴍᴀɴᴅs ᴛɪ ɢᴇᴛ ᴪʀᴇᴍɪᴜᴍ ᴜsᴇʀs ʀᴇʟᴀᴛᴇᴅ ᴄɪᴍᴍᴀɴᴅs.</b>\n\n"
        "<b>ɪᴛʜᴇʀ ᴄɪᴍᴍᴀɴᴅs:</b></blockquote>\n"
        "- /addpremium - <b>ɢʀᴀɴᴛ ᴪʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss [ᴀᴅᴍɪɴ]</b>\n"
        "- /remove_premium - <b>ʀᴇᴠɪᴋᴇ ᴪʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss [ᴀᴅᴍɪɴ]</b>\n"
        "- /premium_users - <b>ʟɪsᴛ ᴪʀᴇᴍɪᴜᴍ ᴜsᴇʀs [ᴀᴅᴘɪɴ]</b>"
    )
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ᴄʟɪsᴇ", callback_data="close")]])
    await message.reply_text(reply_text, reply_markup=reply_markup,
                             message_effect_id=random.choice(MESSAGE_MESSAGE_EFFECT_IDS))

#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#
