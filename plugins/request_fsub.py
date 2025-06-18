#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved
#

import asyncio
import os
import random
import sys
import time
import logging
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction, ChatMemberStatus, ChatType
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatMemberUpdated, ChatPermissions, InputMediaPhoto
from bot import Bot
from helper_func import *
from database.database import *
from config import OWNER_ID, RANDOM_IMAGES, START_PIC

# Set up logging for this module
logger = logging.getLogger(__name__)

# Define message effect IDs
MESSAGE_EFFECT_IDS = [
    5104841245755180586,  # 🔥
    5107584321108051014,  # 👍
    5044134455711629726,  # ❤️
    5046509860389126442,  # 🎉
    5104858069142078462,  # 👎
    5046589136895476101,  # 💩
]

# Function to show force-sub settings with channels list, buttons, image, and message effects
async def show_force_sub_settings(client: Client, chat_id: int, message_id: int = None):
    """Show the force-sub settings menu with channel list and controls."""
    settings = await db.get_settings()
    force_sub_enabled = settings.get('FORCE_SUB_ENABLED', True)
    mode_status = "🟢 Enabled" if force_sub_enabled else "🔴 Disabled"
    settings_text = f"<b>›› Request Fsub Settings:</b>\n\n<blockquote><b>Force Sub Mode: {mode_status}</b></blockquote>\n\n"
    channels = await db.show_channels()
    
    if not channels:
        settings_text += "<blockquote><i>No channels configured yet. Use 𖤓 Add Channels 𖤓 to add channels.</i></blockquote>"
    else:
        settings_text += "<blockquote><b>⚡ Force-sub Channels:</b></blockquote>\n\n"
        for ch_id in channels[:5]:  # Show only first 5 channels
            try:
                chat = await client.get_chat(ch_id)
                temp_off = await db.get_channel_temp_off(ch_id)
                status = "🔴 Off" if temp_off else "🟢 On"
                link = await client.export_chat_invite_link(ch_id) if not chat.username else f"https://t.me/{chat.username}"
                settings_text += f"<blockquote><b><a href='{link}'>{chat.title}</a> - <code>{ch_id}</code> ({status})</b></blockquote>\n"
            except Exception as e:
                logger.error(f"Failed to fetch chat {ch_id}: {e}")
                if "USERNAME_NOT_OCCUPIED" in str(e):
                    await db.rem_channel(ch_id)  # Remove invalid channel from database
                    logger.info(f"Removed invalid channel {ch_id} from database")
                    continue
                settings_text += f"<blockquote><b><code>{ch_id}</code> — <i>Unavailable</i></b></blockquote>\n"
        if len(channels) > 5:  # If more than 5 channels
            settings_text += f"<blockquote><i>...and {len(channels) - 5} more.</i></blockquote>\n"

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("• Add Channels ", callback_data="fsub_add_channel"),
                InlineKeyboardButton(" Remove Channels •", callback_data="fsub_remove_channel")
            ],
            [
                InlineKeyboardButton("• Toggle Mode •", callback_data="fsub_toggle_mode")
            ],
            [
                InlineKeyboardButton("• Single Off •", callback_data="fsub_single_off"),
                InlineKeyboardButton(" Fully Off •", callback_data="fsub_fully_off")
            ],
            [
                InlineKeyboardButton(" Channels List •", callback_data="fsub_channels_list")
            ],
            [
                InlineKeyboardButton("• Refresh ", callback_data="fsub_refresh"),
                InlineKeyboardButton(" Close•", callback_data="fsub_close")
            ]
        ]
    )

    selected_image = random.choice(RANDOM_IMAGES) if RANDOM_IMAGES else START_PIC
    selected_effect = random.choice(MESSAGE_EFFECT_IDS) if MESSAGE_EFFECT_IDS else None

    if message_id:
        try:
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=settings_text,
                reply_markup=buttons,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
            logger.info("Edited message as text-only")
        except Exception as e:
            logger.error(f"Failed to edit message: {e}")
    else:
        try:
            await client.send_photo(
                chat_id=chat_id,
                photo=selected_image,
                caption=settings_text,
                reply_markup=buttons,
                parse_mode=ParseMode.HTML,
                message_effect_id=selected_effect
            )
            logger.info(f"Sent photo message with image {selected_image} and effect {selected_effect}")
        except Exception as e:
            logger.error(f"Failed to send photo message with image {selected_image}: {e}")
            try:
                await client.send_message(
                    chat_id=chat_id,
                    text=settings_text,
                    reply_markup=buttons,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                    message_effect_id=selected_effect
                )
                logger.info(f"Sent text-only message with effect {selected_effect} as fallback")
            except Exception as e:
                logger.error(f"Failed to send text-only message with effect {selected_effect}: {e}")
                await client.send_message(
                    chat_id=chat_id,
                    text=settings_text,
                    reply_markup=buttons,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )
                logger.info("Sent text-only message without effect as final fallback")

# Function to show the channels list
async def show_channels_list(client: Client, chat_id: int, message_id: int):
    """Show the list of force-sub channels with their links."""
    channels = await db.show_channels()
    settings_text = "<b>›› Force-sub Channels List:</b>\n\n"
    
    if not channels:
        settings_text += "<blockquote><i>No channels configured yet.</i></blockquote>"
    else:
        for ch_id in channels:
            try:
                chat = await client.get_chat(ch_id)
                link = await client.export_chat_invite_link(ch_id) if not chat.username else f"https://t.me/{chat.username}"
                settings_text += f"<blockquote><b><a href='{link}'>{chat.title}</a> - <code>{ch_id}</code></b></blockquote>\n"
            except Exception as e:
                logger.error(f"Failed to fetch chat {ch_id}: {e}")
                if "USERNAME_NOT_OCCUPIED" in str(e):
                    await db.rem_channel(ch_id)  # Remove invalid channel from database
                    logger.info(f"Removed invalid channel {ch_id} from database")
                    continue
                settings_text += f"<blockquote><b><code>{ch_id}</code> — <i>Unavailable</i></b></blockquote>\n"

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("• Back •", callback_data="fsub_back"),
                InlineKeyboardButton("• Close •", callback_data="fsub_close")
            ]
        ]
    )

    selected_image = random.choice(RANDOM_IMAGES) if RANDOM_IMAGES else START_PIC
    selected_effect = random.choice(MESSAGE_EFFECT_IDS) if MESSAGE_EFFECT_IDS else None

    try:
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=settings_text,
            reply_markup=buttons,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        logger.info("Edited message with channels list")
    except Exception as e:
        logger.error(f"Failed to edit message: {e}")
        await client.send_message(
            chat_id=chat_id,
            text=settings_text,
            reply_markup=buttons,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
            message_effect_id=selected_effect
        )
        logger.info(f"Sent channels list message with effect {selected_effect}")

# Function to show the fully off settings
async def show_fully_off_settings(client: Client, chat_id: int, message_id: int = None):
    """Show the fully off settings menu for force-sub system."""
    settings = await db.get_settings()
    force_sub_enabled = settings.get('FORCE_SUB_ENABLED', True)
    mode_status = "🟢 Enabled" if force_sub_enabled else "🔴 Disabled"
    settings_text = f"<b>›› Force Sub Fully Off Settings:</b>\n\n<blockquote><b>Force Sub Mode: {mode_status}</b></blockquote>\n\n"
    settings_text += "<b>Click below buttons to change settings</b>"

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("• Disable ❌" if force_sub_enabled else "• Enable ✅", callback_data="fsub_toggle_full"),
                InlineKeyboardButton("• Refresh ", callback_data="fsub_full_refresh")
            ],
            [
                InlineKeyboardButton("• Back •", callback_data="fsub_back"),
                InlineKeyboardButton("• Close •", callback_data="fsub_close")
            ]
        ]
    )

    selected_image = random.choice(RANDOM_IMAGES) if RANDOM_IMAGES else START_PIC
    selected_effect = random.choice(MESSAGE_EFFECT_IDS) if MESSAGE_EFFECT_IDS else None

    if message_id:
        try:
            await client.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=InputMediaPhoto(media=selected_image, caption=settings_text),
                reply_markup=buttons
            )
            logger.info("Edited message with fully off settings")
        except Exception as e:
            logger.error(f"Failed to edit message with image: {e}")
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=settings_text,
                reply_markup=buttons,
                parse_mode=ParseMode.HTML
            )
    else:
        try:
            await client.send_photo(
                chat_id=chat_id,
                photo=selected_image,
                caption=settings_text,
                reply_markup=buttons,
                parse_mode=ParseMode.HTML,
                message_effect_id=selected_effect
            )
            logger.info(f"Sent fully off settings message with image {selected_image} and effect {selected_effect}")
        except Exception as e:
            logger.error(f"Failed to send photo: {e}")
            await client.send_message(
                chat_id=chat_id,
                text=settings_text,
                reply_markup=buttons,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
                message_effect_id=selected_effect
            )
            logger.info(f"Sent fully off settings message with effect {selected_effect} as fallback")

@Bot.on_message(filters.command('forcesub') & filters.private & admin)
async def force_sub_settings(client: Client, message: Message):
    """Handle /forcesub command to show settings."""
    logger.info(f"Received /forcesub command from chat {message.chat.id}")
    await show_force_sub_settings(client, message.chat.id)

@Bot.on_callback_query(filters.regex(r"^fsub_"))
async def force_sub_callback(client: Client, callback: CallbackQuery):
    """Handle callback queries for force-sub settings."""
    data = callback.data
    chat_id = callback.message.chat.id
    message_id = callback.message.id

    logger.info(f"Received callback query with data: {data} in chat {chat_id}")

    if data == "fsub_add_channel":
        await db.set_temp_state(chat_id, "awaiting_add_channel_input")
        logger.info(f"Set state to 'awaiting_add_channel_input' for chat {chat_id}")
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="<blockquote><b>Give me the channel IDs (space-separated).</b>\n<b>Example: -1001234567890 -1000987654321</b></blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("•Back•", callback_data="fsub_back"),
                    InlineKeyboardButton("•Close•", callback_data="fsub_close")
                ]
            ]),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        await callback.answer("Provide the channel IDs (space-separated).")

    elif data == "fsub_remove_channel":
        await db.set_temp_state(chat_id, "awaiting_remove_channel_input")
        logger.info(f"Set state to 'awaiting_remove_channel_input' for chat {chat_id}")
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="<blockquote><b>Give me the channel IDs (space-separated) or type '<code>all</code>' to remove all channels.</b></blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("•Back•", callback_data="fsub_back"),
                    InlineKeyboardButton("•Close•", callback_data="fsub_close")
                ]
            ]),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        await callback.answer("Provide the channel IDs (space-separated) or type 'all'.")

    elif data == "fsub_toggle_mode":
        temp = await callback.message.reply("<b><i>Wait a sec...</i></b>", quote=True)
        channels = await db.show_channels()

        if not channels:
            await temp.edit("<blockquote><b>❌ No force-sub channels found.</b></blockquote>")
            await callback.answer()
            return

        buttons = []
        for ch_id in channels:
            try:
                chat = await client.get_chat(ch_id)
                mode = await db.get_channel_mode(ch_id)
                status = "🟢" if mode == "on" else "🔴"
                title = f"{status} {chat.title}"
                buttons.append([InlineKeyboardButton(title, callback_data=f"rfs_ch_{ch_id}")])
            except Exception as e:
                logger.error(f"Failed to fetch chat {ch_id}: {e}")
                if "USERNAME_NOT_OCCUPIED" in str(e):
                    await db.rem_channel(ch_id)  # Remove invalid channel from database
                    logger.info(f"Removed invalid channel {ch_id} from database")
                    continue
                buttons.append([InlineKeyboardButton(f"⚠️ {ch_id} (Unavailable)", callback_data=f"rfs_ch_{ch_id}")])

        buttons.append([InlineKeyboardButton("Close ✖️", callback_data="fsub_close")])

        await temp.edit(
            "<blockquote><b>⚡ Select a channel to toggle force-sub mode:</b></blockquote>",
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )
        await callback.answer()

    elif data == "fsub_channels_list":
        await show_channels_list(client, chat_id, message_id)
        await callback.answer("Showing channels list!")

    elif data == "fsub_single_off":
        temp = await callback.message.reply("<b><i>Wait a sec...</i></b>", quote=True)
        channels = await db.show_channels()

        if not channels:
            await temp.edit("<blockquote><b>❌ No force-sub channels found.</b></blockquote>")
            await callback.answer()
            return

        buttons = []
        for ch_id in channels:
            try:
                chat = await client.get_chat(ch_id)
                temp_off = await db.get_channel_temp_off(ch_id)
                status = "🔴 Off" if temp_off else "🟢 On"
                title = f"{status} {chat.title}"
                buttons.append([InlineKeyboardButton(title, callback_data=f"fsub_temp_off_{ch_id}")])
            except Exception as e:
                logger.error(f"Failed to fetch chat {ch_id}: {e}")
                if "USERNAME_NOT_OCCUPIED" in str(e):
                    await db.rem_channel(ch_id)  # Remove invalid channel from database
                    logger.info(f"Removed invalid channel {ch_id} from database")
                    continue
                buttons.append([InlineKeyboardButton(f"⚠️ {ch_id} (Unavailable)", callback_data=f"fsub_temp_off_{ch_id}")])

        buttons.append([InlineKeyboardButton("Close ✖️", callback_data="fsub_close")])

        await temp.edit(
            "<blockquote><b>⚡ Select a channel to toggle temporary off mode:</b></blockquote>",
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )
        await callback.answer()

    elif data == "fsub_fully_off":
        await show_fully_off_settings(client, chat_id, message_id)
        await callback.answer("Showing fully off settings!")

    elif data == "fsub_toggle_full":
        settings = await db.get_settings()
        current_mode = settings.get('FORCE_SUB_ENABLED', True)
        new_mode = not current_mode
        await db.update_setting('FORCE_SUB_ENABLED', new_mode)
        await show_fully_off_settings(client, chat_id, message_id)
        await callback.answer(f"Force-sub mode {'enabled' if new_mode else 'disabled'}!")

    elif data == "fsub_full_refresh":
        await show_fully_off_settings(client, chat_id, message_id)
        await callback.answer("Settings refreshed!")

    elif data == "fsub_refresh":
        await show_force_sub_settings(client, chat_id, callback.message.id)
        await callback.answer("Settings refreshed!")

    elif data == "fsub_close":
        await db.set_temp_state(chat_id, "")
        await callback.message.delete()
        await callback.answer("Settings closed!")

    elif data == "fsub_back":
        await db.set_temp_state(chat_id, "")
        await show_force_sub_settings(client, chat_id, message_id)
        await callback.answer("Back to settings!")

    elif data.startswith("fsub_temp_off_"):
        ch_id = int(callback.data.split("_")[-1])
        logger.info(f"Toggling temp_off for channel {ch_id} by user {callback.from_user.id}")

        try:
            current_temp_off = await db.get_channel_temp_off(ch_id)
            new_temp_off = not current_temp_off
            await db.set_channel_temp_off(ch_id, new_temp_off)
            
            chat = await client.get_chat(ch_id)
            status = "🔴 Off" if new_temp_off else "🟢 On"
            await callback.message.edit_text(
                f"<blockquote><b>✅ Temporary mode toggled for channel:</b></blockquote>\n\n"
                f"<blockquote><b>Name:</b> <a href='https://t.me/{chat.username}'>{chat.title}</a></blockquote>\n"
                f"<blockquote><b>ID:</b> <code>{ch_id}</code></blockquote>\n"
                f"<blockquote><b>Mode:</b> {status} {'Disabled' if new_temp_off else 'Enabled'}</blockquote>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("• Back •", callback_data="fsub_single_off")]
                ]),
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
            await callback.answer(f"Channel {ch_id} {'disabled' if new_temp_off else 'enabled'} temporarily!")
        except Exception as e:
            logger.error(f"Failed to toggle temp_off for channel {ch_id}: {e}")
            await callback.message.edit_text(
                f"<blockquote><b>❌ Failed to toggle temporary mode for channel:</b></blockquote>\n<code>{ch_id}</code>\n\n<i>{e}</i>",
                parse_mode=ParseMode.HTML
            )
            await callback.answer()

# Modified filter to allow multiple channel IDs
async def fsub_state_filter(_, __, message: Message):
    """Filter to ensure messages are processed only for force-sub related states."""
    chat_id = message.chat.id
    state = await db.get_temp_state(chat_id)
    logger.info(f"Checking fsub_state_filter for chat {chat_id}: state={state}, message_text={message.text}")
    if state not in ["awaiting_add_channel_input", "awaiting_remove_channel_input"]:
        logger.info(f"State {state} not relevant for fsub_state_filter in chat {chat_id}")
        return False
    if not message.text:
        logger.info(f"No message text provided in chat {chat_id}")
        return False
    # Allow multiple channel IDs (space-separated) or 'all'
    is_valid_input = message.text.lower() == "all" or all(
        part.startswith("-") and part[1:].isdigit() for part in message.text.split()
    )
    logger.info(f"Input validation for chat {chat_id}: is_valid_input={is_valid_input}")
    return is_valid_input

@Bot.on_message(filters.private & admin & filters.create(fsub_state_filter), group=1)
async def handle_channel_input(client: Client, message: Message):
    """Handle channel ID input for force-sub settings."""
    chat_id = message.chat.id
    state = await db.get_temp_state(chat_id)
    logger.info(f"Handling input: {message.text} for state: {state} in chat {chat_id}")

    try:
        if state == "awaiting_add_channel_input":
            channel_ids = message.text.split()  # Split input into list of channel IDs
            all_channels = await db.show_channels()
            channel_ids_only = [cid if isinstance(cid, int) else cid[0] for cid in all_channels]
            report = ""
            success_count = 0

            for channel_id in channel_ids:
                try:
                    channel_id = int(channel_id)
                    if channel_id in channel_ids_only:
                        report += f"<blockquote><b>Channel already exists:</b> <code>{channel_id}</code></blockquote>\n"
                        continue

                    chat = await client.get_chat(channel_id)
                    if chat.type != ChatType.CHANNEL:
                        report += f"<blockquote><b>❌ Only public or private channels are allowed:</b> <code>{channel_id}</code></blockquote>\n"
                        continue

                    member = await client.get_chat_member(chat.id, "me")
                    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                        report += f"<blockquote><b>❌ Bot must be an admin in that channel:</b> <code>{channel_id}</code></blockquote>\n"
                        continue

                    link = await client.export_chat_invite_link(chat.id) if not chat.username else f"https://t.me/{chat.username}"
                    await db.add_channel(channel_id)
                    report += f"<blockquote><b>✅ Channel added:</b> <a href='{link}'>{chat.title}</a> - <code>{channel_id}</code></blockquote>\n"
                    success_count += 1
                except ValueError:
                    report += f"<blockquote><b>❌ Invalid channel ID:</b> <code>{channel_id}</code></blockquote>\n"
                except Exception as e:
                    logger.error(f"Failed to add channel {channel_id}: {e}")
                    report += f"<blockquote><b>❌ Failed to add channel:</b> <code>{channel_id}</code> - <i>{e}</i></blockquote>\n"

            await message.reply(
                f"<b>📋 Add Channel Report:</b>\n\n{report}",
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
            await db.set_temp_state(chat_id, "")
            await show_force_sub_settings(client, chat_id)

        elif state == "awaiting_remove_channel_input":
            all_channels = await db.show_channels()
            if message.text.lower() == "all":
                if not all_channels:
                    await message.reply("<blockquote><b>❌ No force-sub channels found.</b></blockquote>")
                    await db.set_temp_state(chat_id, "")
                    await show_force_sub_settings(client, chat_id)
                    return
                for ch_id in all_channels:
                    await db.rem_channel(ch_id)
                await message.reply("<blockquote><b>✅ All force-sub channels removed.</b></blockquote>")
            else:
                channel_ids = message.text.split()  # Split input into list of channel IDs
                report = ""
                for ch_id in channel_ids:
                    try:
                        ch_id = int(ch_id)
                        if ch_id in all_channels:
                            await db.rem_channel(ch_id)
                            report += f"<blockquote><b>✅ Channel removed:</b> <code>{ch_id}</code></blockquote>\n"
                        else:
                            report += f"<blockquote><b>❌ Channel not found:</b> <code>{ch_id}</code></blockquote>\n"
                    except ValueError:
                        report += f"<blockquote><b>❌ Invalid channel ID:</b> <code>{ch_id}</code></blockquote>\n"

                await message.reply(
                    f"<b>📋 Remove Channel Report:</b>\n\n{report}",
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True
                )
            await db.set_temp_state(chat_id, "")
            await show_force_sub_settings(client, chat_id)

    except Exception as e:
        logger.error(f"Failed to process channel input {message.text}: {e}")
        await message.reply(
            f"<blockquote><b>❌ Failed to process input:</b></blockquote>\n<code>{message.text}</code>\n\n<i>{e}</i>",
            parse_mode=ParseMode.HTML
        )
        await db.set_temp_state(chat_id, "")
        await show_force_sub_settings(client, chat_id)

@Bot.on_message(filters.command('fsub_mode') & filters.private & admin)
async def change_force_sub_mode(client: Client, message: Message):
    """Handle /fsub_mode command to toggle force-sub mode for channels."""
    temp = await message.reply("<b><i>Wait a sec...</i></b>", quote=True)
    channels = await db.show_channels()

    if not channels:
        await temp.edit("<blockquote><b>❌ No force-sub channels found.</b></blockquote>")
        return

    buttons = []
    for ch_id in channels:
        try:
            chat = await client.get_chat(ch_id)
            mode = await db.get_channel_mode(ch_id)
            status = "🟢" if mode == "on" else "🔴"
            title = f"{status} {chat.title}"
            buttons.append([InlineKeyboardButton(title, callback_data=f"rfs_ch_{ch_id}")])
        except Exception as e:
            logger.error(f"Failed to fetch chat {ch_id}: {e}")
            if "USERNAME_NOT_OCCUPIED" in str(e):
                await db.rem_channel(ch_id)  # Remove invalid channel from database
                logger.info(f"Removed invalid channel {ch_id} from database")
                continue
            buttons.append([InlineKeyboardButton(f"⚠️ {ch_id} (Unavailable)", callback_data=f"rfs_ch_{ch_id}")])

    buttons.append([InlineKeyboardButton("Close ✖️", callback_data="fsub_close")])

    await temp.edit(
        "<blockquote><b>⚡ Select a channel to toggle force-sub mode:</b></blockquote>",
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )

@Bot.on_callback_query(filters.regex(r"^rfs_ch_"))
async def toggle_channel_mode(client: Client, callback: CallbackQuery):
    """Handle callback to toggle force-sub mode for a specific channel."""
    ch_id = int(callback.data.split("_")[-1])
    logger.info(f"Toggling mode for channel {ch_id} by user {callback.from_user.id}")

    try:
        current_mode = await db.get_channel_mode(ch_id)
        new_mode = "off" if current_mode == "on" else "on"
        await db.set_channel_mode(ch_id, new_mode)
        
        chat = await client.get_chat(ch_id)
        status = "🟢" if new_mode == "on" else "🔴"
        await callback.message.edit_text(
            f"<blockquote><b>✅ Mode toggled for channel:</b></blockquote>\n\n"
            f"<blockquote><b>Name:</b> <a href='https://t.me/{chat.username}'>{chat.title}</a></blockquote>\n"
            f"<blockquote><b>ID:</b> <code>{ch_id}</code></blockquote>\n"
            f"<blockquote><b>Mode:</b> {status} {'Enabled' if new_mode == 'on' else 'Disabled'}</blockquote>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• Back •", callback_data="fsub_toggle_mode")]
            ]),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        await callback.answer(f"Force-sub {'enabled' if new_mode == 'on' else 'disabled'} for channel {ch_id}")
    except Exception as e:
        logger.error(f"Failed to toggle mode for channel {ch_id}: {e}")
        await callback.message.edit_text(
            f"<blockquote><b>❌ Failed to toggle mode for channel:</b></blockquote>\n<code>{ch_id}</code>\n\n<i>{e}</i>",
            parse_mode=ParseMode.HTML
        )
        await callback.answer()

@Bot.on_chat_member_updated()
async def handle_Chatmembers(client: Client, chat_member_updated: ChatMemberUpdated):    
    """Handle updates to chat members for force-sub channels."""
    chat_id = chat_member_updated.chat.id

    if await db.reqChannel_exist(chat_id):
        old_member = chat_member_updated.old_chat_member

        if not old_member:
            return

        if old_member.status == ChatMemberStatus.MEMBER:
            user_id = old_member.user.id

            if await db.req_user_exist(chat_id, user_id):
                await db.del_req_user(chat_id, user_id)
                logger.info(f"Removed user {user_id} from request list for channel {chat_id} after joining")

@Bot.on_chat_join_request()
async def handle_join_request(client: Client, chat_join_request):
    """Handle join requests for force-sub channels."""
    chat_id = chat_join_request.chat.id
    user_id = chat_join_request.from_user.id

    if await db.reqChannel_exist(chat_id):
        mode = await db.get_channel_mode(chat_id)
        if mode == "on" and not await db.req_user_exist(chat_id, user_id):
            await db.req_user(chat_id, user_id)
            logger.info(f"Added join request for user {user_id} in channel {chat_id}")

@Bot.on_message(filters.command('addchnl') & filters.private & admin)
async def add_force_sub(client: Client, message: Message):
    """Handle /addchnl command to add a force-sub channel."""
    temp = await message.reply("<b><i>Waiting...</i></b>", quote=True)
    args = message.text.split(maxsplit=1)

    if len(args) != 2:
        buttons = [[InlineKeyboardButton("Close", callback_data="fsub_close")]]
        await temp.edit(
            "<blockquote><b>Usage:</b></blockquote>\n<code>/addchnl -100XXXXXXXXXX</code>\n\n"
            "<b>Add only one channel at a time.</b>",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.HTML
        )
        return

    try:
        channel_id = int(args[1])
        all_channels = await db.show_channels()
        channel_ids_only = [cid if isinstance(cid, int) else cid[0] for cid in all_channels]
        if channel_id in channel_ids_only:
            await temp.edit(f"<blockquote><b>Channel already exists:</b></blockquote>\n <blockquote><code>{channel_id}</code></blockquote>")
            return

        chat = await client.get_chat(channel_id)

        if chat.type != ChatType.CHANNEL:
            await temp.edit("<b>❌ Only public or private channels are allowed.</b>")
            return

        member = await client.get_chat_member(chat.id, "me")
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            await temp.edit("<b>❌ Bot must be an admin in that channel.</b>")
            return

        link = await client.export_chat_invite_link(chat.id) if not chat.username else f"https://t.me/{chat.username}"
        
        await db.add_channel(channel_id)
        await temp.edit(
            f"<blockquote><b>✅ Force-sub Channel added successfully!</b></blockquote>\n\n"
            f"<blockquote><b>Name:</b> <a href='{link}'>{chat.title}</a></blockquote>\n"
            f"<blockquote><b>ID: <code>{channel_id}</code></b></blockquote>",
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    except ValueError:
        await temp.edit("<blockquote><b>❌ Invalid channel ID!</b></blockquote>")
    except Exception as e:
        logger.error(f"Failed to add channel {args[1]}: {e}")
        await temp.edit(f"<blockquote><b>❌ Failed to add channel:</b></blockquote>\n<code>{args[1]}</code>\n\n<i>{e}</i>", parse_mode=ParseMode.HTML)

#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved
#
