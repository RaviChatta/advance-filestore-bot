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
import time
import logging
from datetime import datetime, timedelta
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatInviteLink, ChatPrivileges
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant
from bot import Bot
from config import *
from helper_func import *
from database.database import *

# Set up logging for this module
logger = logging.getLogger(__name__)

#=====================================================================================##

REPLY_ERROR = "<code>Uꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴀꜱ ᴀ ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇꜱꜱᴀɢᴇ ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ ꜱᴘᴀᴄᴇꜱ.</code>"

# Custom filter for cast input
async def cast_input_filter(_, __, message: Message):
    chat_id = message.chat.id
    state = await db.get_temp_state(chat_id)
    logger.info(f"Checking cast_input_filter for chat {chat_id}: state={state}")
    return state in ["awaiting_broadcast_input", "awaiting_pin_input", "awaiting_delete_message"]

# Custom filter for delete duration input
async def delete_duration_filter(_, __, message: Message):
    chat_id = message.chat.id
    state = await db.get_temp_state(chat_id)
    logger.info(f"Checking delete_duration_filter for chat {chat_id}: state={state}")
    return state == "awaiting_delete_duration" and message.text and message.text.isdigit()

#=====================================================================================##

@Bot.on_message(filters.private & filters.command('cast') & admin)
async def cast_settings(client: Bot, message: Message):
    """Show cast settings with broadcast options."""
    # Reset state to avoid conflicts
    await db.set_temp_state(message.chat.id, "")
    logger.info(f"Reset state for chat {message.chat.id} before showing cast settings")

    settings_text = "<b>›› Cᴀꜱᴛ Sᴇᴛᴛɪɴɢꜱ:</b>\n\n" \
                    "<blockquote><b>⚡ Sᴇʟᴇᴄᴛ ᴀ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴏᴘᴛɪᴏɴ:</b></blockquote>\n\n" \
                    "<b>📢 Bʀᴏᴀᴅᴄᴀꜱᴛ:</b> Sᴇɴᴅ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴀʟʟ ᴜꜱᴇʀꜱ.\n" \
                    "<b>📌 Pɪɴ:</b> Sᴇɴᴅ ᴀɴᴅ ᴘɪɴ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ ɪɴ ᴀʟʟ ᴜꜱᴇʀ ᴄʜᴀᴛꜱ.\n" \
                    "<b>🗑 Dᴇʟᴇᴛᴇ:</b> Sᴇɴᴅ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴡɪᴛʜ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ᴀꜰᴛᴇʀ ᴀ ꜱᴘᴇᴄɪꜰɪᴇᴅ ᴅᴜʀᴀᴛɪᴏɴ."

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📢 Bʀᴏᴀᴅᴄᴀꜱᴛ", callback_data="cast_broadcast")],
            [
                InlineKeyboardButton("📌 Pɪɴ", callback_data="cast_pin"),
                InlineKeyboardButton("🗑 Dᴇdelete", callback_data="cast_delete")
            ],
            [InlineKeyboardButton("• Cʟᴏꜱᴇ •", callback_data="cast_close")]
        ]
    )

    selected_image = random.choice(RANDOM_IMAGES) if RANDOM_IMAGES else START_PIC
    selected_effect = random.choice(MESSAGE_EFFECT_IDS) if MESSAGE_EFFECT_IDS else None

    try:
        await client.send_photo(
            chat_id=message.chat.id,
            photo=selected_image,
            caption=settings_text,
            reply_markup=buttons,
            parse_mode=ParseMode.HTML,
            message_effect_id=selected_effect
        )
        logger.info(f"Sent cast settings with image {selected_image} for chat {message.chat.id}")
    except Exception as e:
        logger.error(f"Failed to send photo for cast settings: {e}")
        await client.send_message(
            chat_id=message.chat.id,
            text=settings_text,
            reply_markup=buttons,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            message_effect_id=selected_effect
        )
        logger.info(f"Sent text-only cast settings as fallback for chat {message.chat.id}")

#=====================================================================================##

@Bot.on_callback_query(filters.regex(r"^cast_"))
async def cast_callback(client: Bot, callback: CallbackQuery):
    """Handle callback queries for cast settings."""
    data = callback.data
    chat_id = callback.message.chat.id
    message_id = callback.message.id
    selected_image = random.choice(RANDOM_IMAGES) if RANDOM_IMAGES else START_PIC
    selected_effect = random.choice(MESSAGE_EFFECT_IDS) if MESSAGE_EFFECT_IDS else None

    logger.info(f"Received cast callback query with data: {data} in chat {chat_id}")

    if data == "cast_broadcast":
        await db.set_temp_state(chat_id, "awaiting_broadcast_input")
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="<blockquote><b>Pʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀꜱᴛ (ᴛᴇxᴛ, ɪᴍᴀɢᴇ, ᴏʀ ᴀɴʏ ᴍᴇᴅɪᴀ).</b></blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("• Cᴀɴᴄᴇʟ •", callback_data="cast_cancel")
                ]
            ]),
            parse_mode=ParseMode.HTML
        )
        await callback.answer("Pʟᴇᴀꜱᴇ ꜱᴇɴᴅ ᴛʜᴇ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴍᴇꜱꜱᴀɢᴇ.")

    elif data == "cast_pin":
        await db.set_temp_state(chat_id, "awaiting_pin_input")
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="<blockquote><b>Pʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴀɴᴅ ᴘɪɴ (ᴛᴇxᴛ, ɪᴍᴀɢᴇ, ᴏʀ ᴀɴʏ ᴍᴇᴅɪᴀ).</b></blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("• Cᴀɴᴄᴇʟ •", callback_data="cast_cancel")
                ]
            ]),
            parse_mode=ParseMode.HTML
        )
        await callback.answer("Pʟᴇᴀꜱᴇ ꜱᴇɴᴅ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴘɪɴ.")

    elif data == "cast_delete":
        await db.set_temp_state(chat_id, "awaiting_delete_duration")
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="<blockquote><b>Pʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ᴅᴜʀᴀᴛɪᴏɴ ɪɴ ꜱᴇᴄᴏɴᴅꜱ ꜰᴏʀ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ (ᴇ.ɢ., '300' ꜰᴏʀ 5 ᴍɪɴᴜᴛᴇꜱ).</b></blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("• Cᴀɴᴄᴇʟ •", callback_data="cast_cancel")
                ]
            ]),
            parse_mode=ParseMode.HTML
        )
        await callback.answer("Pʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ᴅᴜʀᴀᴛɪᴏɴ.")

    elif data == "cast_close":
        await db.set_temp_state(chat_id, "")
        await callback.message.delete()
        await callback.answer("Cᴀꜱᴛ ꜱᴇᴛᴛɪɴɢꜱ ᴄʟᴏꜱᴇᴅ!")

    elif data == "cast_cancel":
        await db.set_temp_state(chat_id, "")
        await cast_settings(client, callback.message)
        await callback.answer("Aᴄᴛɪᴏɴ ᴄᴀɴᴄᴇʟʟᴇᴅ!")

#=====================================================================================##

@Bot.on_message(filters.private & admin & filters.create(delete_duration_filter))
async def handle_delete_duration(client: Bot, message: Message):
    """Handle the duration input for delete broadcast."""
    chat_id = message.chat.id
    try:
        duration = int(message.text)
        if duration <= 0:
            raise ValueError("Duration must be positive")
    except ValueError:
        await message.reply("<b>❌ Iɴᴠᴀʟɪᴅ ᴅᴜʀᴀᴛɪᴏɴ. Pʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ ᴏꜰ ꜱᴇᴄᴏɴᴅꜱ.</b>")
        return

    # Store duration in temp data
    await db.set_temp_data(chat_id, "delete_duration", duration)
    await db.set_temp_state(chat_id, "awaiting_delete_message")

    await message.reply(
        "<blockquote><b>Pʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴡɪᴛʜ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ (ᴛᴇxᴛ, ɪᴍᴀɢᴇ, ᴏʀ ᴀɴʯ ᴍᴇᴅɪᴀ).</b></blockquote>",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("• Cᴀɴᴄᴇʟ •", callback_data="cast_cancel")
            ]
        ]),
        parse_mode=ParseMode.HTML
    )
    logger.info(f"Stored duration {duration} for chat {chat_id} and set state to awaiting_delete_message")

#=====================================================================================##

@Bot.on_message(filters.private & admin & filters.create(cast_input_filter), group=3)
async def handle_cast_input(client: Bot, message: Message):
    """Handle the broadcast message input from the user."""
    chat_id = message.chat.id
    state = await db.get_temp_state(chat_id)
    logger.info(f"Handling cast input for state: {state} in chat {chat_id}")

    query = await db.full_userbase()
    banned_users = await db.get_ban_users()
    valid_users = [uid for uid in query if uid not in banned_users]
    total = len(valid_users)
    successful = 0
    blocked = 0
    deleted = 0
    unsuccessful = 0

    pls_wait = await message.reply("<i>Bʀᴏᴀᴅᴄᴀꜱᴛ ᴘʀᴏᴄᴇꜱꜱɪɴɢ....</i>")

    if state == "awaiting_broadcast_input":
        for user_id in valid_users:
            try:
                await message.copy(user_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await message.copy(user_id)
                successful += 1
            except UserIsBlocked:
                await db.del_user(user_id)
                blocked += 1
            except InputUserDeactivated:
                await db.del_user(user_id)
                deleted += 1
            except Exception as e:
                logger.error(f"Failed to broadcast to {user_id}: {e}")
                unsuccessful += 1
            await asyncio.sleep(0.1)

        status = f"""<b><u>Bʀᴏᴀᴅᴄᴀꜱᴛ Cᴏᴍᴘʟᴇᴛᴇᴅ</u></b>

Tᴏᴛᴀʟ Uꜱᴇʀꜱ: <code>{total}</code>
Sᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{successful}</code>
Bʟᴏᴄᴋᴇᴅ Uꜱᴇʀꜱ: <code>{blocked}</code>
Dᴇʟᴇᴛᴇᴅ Aᴄᴄᴏᴜɴᴛꜱ: <code>{deleted}</code>
Uɴꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{unsuccessful}</code>"""

    elif state == "awaiting_pin_input":
        for user_id in valid_users:
            try:
                sent_msg = await message.copy(user_id)
                await client.pin_chat_message(chat_id=user_id, message_id=sent_msg.id, both_sides=True)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                sent_msg = await message.copy(user_id)
                await client.pin_chat_message(chat_id=user_id, message_id=sent_msg.id, both_sides=True)
                successful += 1
            except UserIsBlocked:
                await db.del_user(user_id)
                blocked += 1
            except InputUserDeactivated:
                await db.del_user(user_id)
                deleted += 1
            except Exception as e:
                logger.error(f"Failed to pin broadcast to {user_id}: {e}")
                unsuccessful += 1
            await asyncio.sleep(0.1)

        status = f"""<b><u>Pɪɴ Bʀᴏᴀᴅᴄᴀꜱᴛ Cᴏᴍᴘʟᴇᴛᴇᴅ</u></b>

Tᴏᴛᴀʟ Uꜱᴇʀꜱ: <code>{total}</code>
Sᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{successful}</code>
Bʟᴏᴄᴋᴇᴅ Uꜱᴇʀꜱ: <code>{blocked}</code>
Dᴇʟᴇᴛᴇᴅ Aᴄᴄᴏᴜɴᴛꜱ: <code>{deleted}</code>
Uɴꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{unsuccessful}</code>"""

    elif state == "awaiting_delete_message":
        duration = await db.get_temp_data(chat_id, "delete_duration") or 300  # Default 5 minutes
        for user_id in valid_users:
            try:
                sent_msg = await message.copy(user_id)
                await asyncio.sleep(duration)
                await sent_msg.delete()
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                sent_msg = await message.copy(user_id)
                await asyncio.sleep(duration)
                await sent_msg.delete()
                successful += 1
            except UserIsBlocked:
                await db.del_user(user_id)
                blocked += 1
            except InputUserDeactivated:
                await db.del_user(user_id)
                deleted += 1
            except Exception as e:
                logger.error(f"Failed to delete broadcast to {user_id}: {e}")
                unsuccessful += 1
            await asyncio.sleep(0.1)

        status = f"""<b><u>Aᴜᴛᴏ-Dᴇʟᴇᴛᴇ Bʀᴏᴀᴅᴄᴀꜱᴛ Cᴏᴍᴪʟᴇᴛᴇᴅ</u></b>

Tᴏᴛᴀʟ Uꜱᴇʀꜱ: <code>{total}</code>
Sᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{successful}</code>
Bʟᴏᴄᴋᴇᴴ Uꜱᴇʀꜱ: <code>{blocked}</code>
Dᴇʟᴇᴛᴇᴅ Aᴄᴄᴏᴜɴᴛꜱ: <code>{deleted}</code>
Uɴꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{unsuccessful}</code>
Dᴜʀᴀᴛɪᴏɴ: <code>{get_readable_time(duration)}</code>"""

    await pls_wait.edit(status, parse_mode=ParseMode.HTML)
    await db.set_temp_state(chat_id, "")
    logger.info(f"Cleared state for chat {chat_id} after broadcast")

#=====================================================================================##

@Bot.on_message(filters.private & filters.command('pbroadcast') & admin)
async def send_pin_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await db.full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply("<i>Bʀᴏᴀᴅᴄᴀꜱᴛ ᴘʀᴏᴄᴇꜱꜱɪɴɢ....</i>")
        for chat_id in query:
            try:
                sent_msg = await broadcast_msg.copy(chat_id)
                await client.pin_chat_message(chat_id=chat_id, message_id=sent_msg.id, both_sides=True)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                sent_msg = await broadcast_msg.copy(chat_id)
                await client.pin_chat_message(chat_id=chat_id, message_id=sent_msg.id, both_sides=True)
                successful += 1
            except UserIsBlocked:
                await db.del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await db.del_user(chat_id)
                deleted += 1
            except Exception as e:
                logger.error(f"Failed to send or pin message to {chat_id}: {e}")
                unsuccessful += 1
            total += 1

        status = f"""<b><u>Bʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴪʟᴇᴛᴇᴅ</u></b>

Tᴏᴛᴀʟ Uꜱᴇʀꜱ: <code>{total}</code>
Sᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{successful}</code>
Bʟᴏᴄᴋᴇᴅ Uꜱᴇʀꜱ: <code>{blocked}</code>
Dᴇʟᴇᴛᴇᴴ Aᴄᴄᴏᴜɴᴛꜱ: <code>{deleted}</code>
Uɴꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{unsuccessful}</code>"""

        return await pls_wait.edit(status)

    else:
        msg = await message.reply("Rᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ʙʜʀᴏᴀᴅᴄᴀꜱᴛ ᴀɴᴅ ᴘɪɴ ɪᴛ.")
        await asyncio.sleep(8)
        await msg.delete()

#=====================================================================================##

@Bot.on_message(filters.private & filters.command('broadcast') & admin)
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await db.full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply("<i>Bʀᴏᴀᴅᴄᴀꜱᴛ ᴪʀᴏᴄᴇꜱꜱɪɴɢ....</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await db.del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await db.del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1

        status = f"""<b><u>Bʀᴏᴀᴅᴄᴀꜱᴛ ᴄᴏᴍᴪʟᴇᴛᴇᴅ</u></b>

Tᴏᴛᴀʟ Uꜱᴇʀꜱ: <code>{total}</code>
Sᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{successful}</code>
Bʟᴏᴄᴋᴇᴴ Uꜱᴇʀꜱ: <code>{blocked}</code>
Dᴇʟᴇᴛᴇᴴ Aᴄᴄᴏᴜɴᴛꜱ: <code>{deleted}</code>
Uɴꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{unsuccessful}</code>"""

        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()

#=====================================================================================##

@Bot.on_message(filters.private & filters.command('dbroadcast') & admin)
async def delete_broadcast(client: Bot, message: Message):
    if message.reply_to_message:
        try:
            duration = int(message.command[1])  # Get the duration in seconds
        except (IndexError, ValueError):
            await message.reply("<b>Pʟᴇᴀꜱᴇ ᴜꜱᴇ ᴀ ᴠᴀʟɪᴅ ᴅᴜʀᴀᴛɪᴏɴ ɪɴ ꜱᴇᴄᴏɴᴅꜱ.</b> Uꜱᴀɢᴇ: /dbroadcast {duration}")
            return

        query = await db.full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply("<i>Bʀᴏᴀᴅᴄᴀꜱᴛ ᴡɪᴛʜ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ᴪʀᴏᴄᴇꜱꜱɪɴɢ....</i>")
        for chat_id in query:
            try:
                sent_msg = await broadcast_msg.copy(chat_id)
                await asyncio.sleep(duration)
                await sent_msg.delete()
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                sent_msg = await broadcast_msg.copy(chat_id)
                await asyncio.sleep(duration)
                await sent_msg.delete()
                successful += 1
            except UserIsBlocked:
                await db.del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await db.del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1

        status = f"""<b><u>Bʀᴏᴀᴅᴄᴀꜱᴛ ᴡɪᴛʜ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ᴄᴏᴍᴪʟᴇᴛᴇᴅ</u></b>

Tᴏᴛᴀʟ Uꜱᴇʀꜱ: <code>{total}</code>
Sᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{successful}</code>
Bʟᴏᴄᴋᴇᴴ Uꜱᴇʀꜱ: <code>{blocked}</code>
Dᴇʟᴇᴛᴇᴴ Aᴄᴄᴏᴜɴᴛꜱ: <code>{deleted}</code>
Uɴꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ: <code>{unsuccessful}</code>"""

        return await pls_wait.edit(status)

    else:
        msg = await message.reply("Pʟᴇᴀꜱᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀꜱᴛ ɪᴛ ᴡɪᴛʜ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ.")
        await asyncio.sleep(8)
        await msg.delete()

#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#
