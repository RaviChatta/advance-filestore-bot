from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from pyrogram.handlers import MessageHandler
from config import PROTECT_CONTENT, HIDE_CAPTION, DISABLE_CHANNEL_BUTTON, BUTTON_NAME, BUTTON_LINK, update_setting, get_settings, RANDOM_IMAGES, START_PIC
import random
import logging

logger = logging.getLogger(__name__)

# Define message effect IDs (used only for /fsettings initial message)
MESSAGE_EFFECT_IDS = [
    5104841245755180586,  # 🔥
    5107584321108051014,  # 👍
    5044134455711629726,  # ❤️
    5046509860389126442,  # 🎉
    5104858069142078462,  # 👎
    5046589136895476101,  # 💩
]

# States for conversation handler
WAITING_FOR_BUTTON_NAME = 'waiting_for_button_name'
WAITING_FOR_BUTTON_LINK = 'waiting_for_button_link'

# Dictionary to track user states
user_states = {}

async def show_settings_message(client, message_or_callback, is_callback=False):
    settings = get_settings()
    
    # Create the settings text in the requested format
    settings_text = "<b>Fɪʟᴇs ʀᴇʟᴀᴛᴇᴅ sᴇᴛᴛɪɴɢs:</b>\n\n"
    settings_text += f"<blockquote><b>›› Pʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ: {'Eɴᴀʙʲʟᴇᴅ' if settings['PROTECT_CONTENT'] else 'Dɪsᴀʙʲʟᴇᴅ'} {'✅' if settings['PROTECT_CONTENT'] else '❌'}\n"
    settings_text += f"›› Hɪᴅᴇ ᴄᴀᴪᴛɪᴏɴ: {'Eɴᴀʙʲʟᴇᴅ' if settings['HIDE_CAPTION'] else 'Dɪsᴀʙʲʟᴇᴅ'} {'✅' if settings['HIDE_CAPTION'] else '❌'}\n"
    settings_text += f"›› Cʜᴀɴɴᴇʟ ʙᴜᴛᴛᴏɴ: {'Eɴᴀʙʲʟᴇᴅ' if not settings['DISABLE_CHANNEL_BUTTON'] else 'Dɪsᴀʙʲʟᴇᴅ'} {'✅' if not settings['DISABLE_CHANNEL_BUTTON'] else '❌'}\n\n"
    settings_text += f"›› Bᴜᴛᴛᴏɴ Nᴀᴍᴇ: {settings['BUTTON_NAME'] if settings['BUTTON_NAME'] else 'not set'}\n"
    settings_text += f"›› Bᴜᴛᴛᴏɴ Lɪɴᴋ: {settings['BUTTON_LINK'] if settings['BUTTON_LINK'] else 'not set'}</b></blockquote>\n\n"
    settings_text += "<b>Cʟɪᴄᴋ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ᴛᴏ ᴄʜᴀɴɢᴇ sᴇᴛᴛɪɴɢs</b>"

    # Create inline buttons for toggling settings
    buttons = [
        [
            InlineKeyboardButton("•ᴘᴄ", callback_data="toggle_protect_content"),
            InlineKeyboardButton("ʜᴄ•", callback_data="toggle_hide_caption"),
        ],
        [
            InlineKeyboardButton("•ᴄʙ", callback_data="toggle_channel_button"),
            InlineKeyboardButton("sʙ•", callback_data="set_button"),
        ],
        [
            InlineKeyboardButton("•ʀᴇꜰᴇʀsʜ•", callback_data="refresh_settings"),
            InlineKeyboardButton("•ʙᴀᴄᴋ•", callback_data="go_back"),
        ]
    ]

    # Select a random image
    selected_image = random.choice(RANDOM_IMAGES) if RANDOM_IMAGES else START_PIC

    if is_callback:
        try:
            await message_or_callback.message.edit_media(
                media=InputMediaPhoto(media=selected_image, caption=settings_text),
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            logger.debug(f"Edited settings message for user {message_or_callback.from_user.id}")
        except Exception as e:
            logger.error(f"Error editing message with photo: {e}")
            await message_or_callback.message.edit_text(
                text=settings_text,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    else:
        try:
            await message_or_callback.reply_photo(
                photo=selected_image,
                caption=settings_text,
                reply_markup=InlineKeyboardMarkup(buttons),
                message_effect_id=random.choice(MESSAGE_EFFECT_IDS)
            )
            logger.debug(f"Sent settings message to user {message_or_callback.from_user.id}")
        except Exception as e:
            logger.error(f"Error sending photo: {e}")
            await message_or_callback.reply_text(
                text=settings_text,
                reply_markup=InlineKeyboardMarkup(buttons)
            )

@Client.on_message(filters.command("fsettings") & filters.private)
async def fsettings_command(client, message):
    logger.info(f"/fsettings command received from user {message.from_user.id}")
    await show_settings_message(client, message)

@Client.on_callback_query(filters.regex(r"^toggle_protect_content$"))
async def toggle_protect_content(client, callback_query):
    logger.info(f"Toggle protect content triggered by user {callback_query.from_user.id}")
    await update_setting("PROTECT_CONTENT", not get_settings()["PROTECT_CONTENT"])
    await show_settings_message(client, callback_query, is_callback=True)
    await callback_query.answer("Pʀᴏᴛᴇᴄᴛ Cᴏɴᴛᴇɴᴛ ᴛᴏɢɢʟᴇᴅ!")

@Client.on_callback_query(filters.regex(r"^toggle_hide_caption$"))
async def toggle_hide_caption(client, callback_query):
    logger.info(f"Toggle hide caption triggered by user {callback_query.from_user.id}")
    await update_setting("HIDE_CAPTION", not get_settings()["HIDE_CAPTION"])
    await show_settings_message(client, callback_query, is_callback=True)
    await callback_query.answer("Hɪᴅᴇ Cᴀᴪᴛɪᴏɴ ᴛᴏɢɢʟᴇᴅ!")

@Client.on_callback_query(filters.regex(r"^toggle_channel_button$"))
async def toggle_channel_button(client, callback_query):
    logger.info(f"Toggle channel button triggered by user {callback_query.from_user.id}")
    await update_setting("DISABLE_CHANNEL_BUTTON", not get_settings()["DISABLE_CHANNEL_BUTTON"])
    await show_settings_message(client, callback_query, is_callback=True)
    await callback_query.answer("Cʜᴀɴɴᴇʟ Bᴜᴛᴛᴏɴ ᴛᴏɢɢʟᴇᴅ!")

@Client.on_callback_query(filters.regex(r"^refresh_settings$"))
async def refresh_settings_message(client, callback_query):
    logger.info(f"Refresh settings triggered by user {callback_query.from_user.id}")
    await show_settings_message(client, callback_query, is_callback=True)
    await callback_query.answer("Sᴇᴛᴛɪɴɢs ʀᴇғʀᴇsʜᴇᴅ!")

@Client.on_callback_query(filters.regex(r"^go_back$"))
async def go_back(client, callback_query):
    logger.info(f"Go back triggered by user {callback_query.from_user.id}")
    await callback_query.message.delete()
    await callback_query.answer("Bᴀᴄᴋ ᴛᴏ ᴍᴀɪɴ ᴍᴇɴᴜ!")

@Client.on_callback_query(filters.regex(r"^set_button$"))
async def set_button_start(client, callback_query):
    user_id = callback_query.from_user.id
    logger.info(f"Set Button callback triggered for user {user_id}")
    user_states[user_id] = WAITING_FOR_BUTTON_NAME
    try:
        await callback_query.message.reply_text(
            "Give me the button name:",
            quote=True
        )
        logger.info(f"Sent 'Give me the button name' message to user {user_id}")
    except Exception as e:
        logger.error(f"Error sending 'Give me the button name' message to user {user_id}: {e}")
        await callback_query.message.reply_text(
            "Error occurred. Please try again."
        )
        await callback_query.answer("Error occurred!")
        return
    await callback_query.answer("Please provide the button name.")

@Client.on_message(filters.private)
async def handle_user_input(client, message):
    user_id = message.from_user.id
    state = user_states.get(user_id)
    if state == WAITING_FOR_BUTTON_NAME:
        await set_button_name(client, message)
    elif state == WAITING_FOR_BUTTON_LINK:
        await set_button_link(client, message)

async def set_button_name(client, message):
    user_id = message.from_user.id
    new_button_name = message.text.strip()
    logger.info(f"Received button name '{new_button_name}' from user {user_id}")
    try:
        await update_setting("BUTTON_NAME", new_button_name)
        logger.debug(f"Updated BUTTON_NAME to '{new_button_name}' for user {user_id}")
    except Exception as e:
        logger.error(f"Error updating BUTTON_NAME for user {user_id}: {e}")
        await message.reply_text("Error updating button name. Please try again.")
        return
    user_states[user_id] = WAITING_FOR_BUTTON_LINK
    try:
        await message.reply_text(
            "Give me the button link:",
            quote=True
        )
        logger.info(f"Sent 'Give me the button link' message to user {user_id}")
    except Exception as e:
        logger.error(f"Error sending 'Give me the button link' message to user {user_id}: {e}")
        await message.reply_text("Error occurred. Please try again.")
        return

async def set_button_link(client, message):
    user_id = message.from_user.id
    new_button_link = message.text.strip()
    logger.info(f"Received button link '{new_button_link}' from user {user_id}")
    try:
        await update_setting("BUTTON_LINK", new_button_link)
        logger.debug(f"Updated BUTTON_LINK to '{new_button_link}' for user {user_id}")
    except Exception as e:
        logger.error(f"Error updating BUTTON_LINK for user {user_id}: {e}")
        await message.reply_text("Error updating button link. Please try again.")
        return
    try:
        await message.reply_text(
            "Bᴜᴛᴛᴏɴ Lɪɴᴋ ᴜᴪᴅᴀᴛᴇᴅ! Uꜱᴇ /fsettings ᴛᴏ sᴇᴇ ᴛʜᴇ ᴜᴪᴅᴀᴛᴇᴅ sᴇᴛᴛɪɴɢs.",
            quote=True
        )
        logger.info(f"Sent confirmation message to user {user_id}")
    except Exception as e:
        logger.error(f"Error sending confirmation message to user {user_id}: {e}")
        await message.reply_text("Error occurred. Please try again.")
    del user_states[user_id]
