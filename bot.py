import logging
import os
import threading

import uvicorn
from fastapi import FastAPI

from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    MenuButtonWebApp,
    WebAppInfo,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import (
    BOT_TOKEN,
    ADMIN_ID,
    DEVELOPER_NAME,
    DEVELOPER_USERNAME,
    MAINTENANCE_MODE,
)

from utils.keyboards import (
    main_menu,
    pdf_menu,
    image_menu,
    qr_menu,
    audio_menu,
    file_menu,
    developer_menu,
    help_menu,
    admin_menu,
)

from handlers.pdf import (
    start_text_to_pdf,
    start_image_to_pdf as start_pdf_image_to_pdf,
    start_merge_pdf,
    start_split_pdf,
    start_pdf_to_image,
    start_pdf_to_text,
    start_protect_pdf,
    handle_pdf_text,
    handle_image_to_pdf as handle_pdf_image,
    handle_pdf_document,
    handle_protect_password,
    done_pdf,
    done_merge_pdf,
)

from handlers.image import (
    start_resize_image,
    start_compress_image,
    start_convert_image,
    start_image_to_pdf,
    start_image_info,
    handle_image,
    handle_image_text,
    handle_convert_format,
    done_image_to_pdf,
)

from handlers.qr import (
    start_qr_text,
    start_qr_url,
    start_qr_wifi,
    start_qr_contact,
    start_qr_email,
    start_qr_phone,
    start_qr_scan,
    start_qr_to_pdf,
    handle_qr_text,
    handle_qr_image,
)

from handlers.audio import (
    start_text_to_voice,
    start_voice_changer,
    start_audio_cutter,
    start_audio_converter,
    start_volume_changer,
    start_audio_info,
    handle_audio_text,
    handle_audio_file,
    handle_audio_format,
    handle_volume_text,
    handle_cut_text,
)

from handlers.file import (
    start_create_zip,
    start_extract_zip,
    start_file_converter,
    start_file_info,
    handle_file_document,
    done_create_zip,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# =========================================================
# FASTAPI / RENDER WEB SERVER
# =========================================================

web_app = FastAPI()


@web_app.get("/")
async def home():
    return {
        "status": "online",
        "service": "Telegram Bot",
    }


@web_app.get("/health")
async def health():
    return {
        "status": "healthy",
    }


def start_web_server():
    port = int(os.environ.get("PORT", "10000"))

    logger.info(
        "Starting web server on port %s",
        port,
    )

    uvicorn.run(
        web_app,
        host="0.0.0.0",
        port=port,
        log_level="warning",
    )


# =========================================================
# TELEGRAM MENU BUTTON
# =========================================================

async def setup_menu_button(application):
    """
    Sets Telegram's left-side bot menu button.

    Clicking:
        🚀 Open Bot

    opens the Render web service URL.
    """

    try:
        await application.bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="🚀 Open Bot",
                web_app=WebAppInfo(
                    url="https://cracker-world.onrender.com/"
                ),
            )
        )

        logger.info(
            "Telegram menu button configured: 🚀 Open Bot"
        )

    except Exception:
        logger.exception(
            "Failed to configure Telegram menu button."
        )


# =========================================================
# START COMMAND
# =========================================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    if MAINTENANCE_MODE:
        await update.message.reply_text(
            "🔧 <b>Bot Maintenance Mode</b>\n\n"
            "এখন bot maintenance-এ আছে। একটু পরে আবার চেষ্টা করো।",
            parse_mode="HTML",
        )
        return

    text = (
        "👋 <b>Welcome to All-in-One Telegram Bot!</b>\n\n"
        "এক জায়গা থেকে PDF, Image, QR, Audio এবং File tools ব্যবহার করতে পারবে।\n\n"
        "নিচের menu থেকে একটি option select করো।"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=main_menu(),
    )


# =========================================================
# HOME COMMAND
# =========================================================

async def home_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    if update.callback_query:
        query = update.callback_query
        await query.answer()

        await query.edit_message_text(
            "🏠 <b>Main Menu</b>\n\n"
            "একটি tool select করো।",
            parse_mode="HTML",
            reply_markup=main_menu(),
        )

    elif update.message:
        await update.message.reply_text(
            "🏠 <b>Main Menu</b>\n\n"
            "একটি tool select করো।",
            parse_mode="HTML",
            reply_markup=main_menu(),
        )


# =========================================================
# PDF CALLBACKS
# =========================================================

async def pdf_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == "pdf_menu":
        await query.answer()
        context.user_data.clear()

        await query.edit_message_text(
            "📄 <b>PDF Tools</b>\n\n"
            "একটি PDF tool select করো।",
            parse_mode="HTML",
            reply_markup=pdf_menu(),
        )
        return

    if data == "text_to_pdf":
        await start_text_to_pdf(update, context)
        return

    if data == "pdf_image_to_pdf":
        await start_pdf_image_to_pdf(update, context)
        return

    if data == "merge_pdf":
        await start_merge_pdf(update, context)
        return

    if data == "split_pdf":
        await start_split_pdf(update, context)
        return

    if data == "pdf_to_image":
        await start_pdf_to_image(update, context)
        return

    if data == "pdf_to_text":
        await start_pdf_to_text(update, context)
        return

    if data == "protect_pdf":
        await start_protect_pdf(update, context)
        return


# =========================================================
# IMAGE CALLBACKS
# =========================================================

async def image_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == "image_menu":
        await query.answer()
        context.user_data.clear()

        await query.edit_message_text(
            "🖼️ <b>Image Tools</b>\n\n"
            "একটি image tool select করো।",
            parse_mode="HTML",
            reply_markup=image_menu(),
        )
        return

    if data == "resize_image":
        await start_resize_image(update, context)
        return

    if data == "compress_image":
        await start_compress_image(update, context)
        return

    if data == "convert_image":
        await start_convert_image(update, context)
        return

    if data == "image_to_pdf":
        await start_image_to_pdf(update, context)
        return

    if data == "image_info":
        await start_image_info(update, context)
        return


async def image_format_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    data = query.data

    formats = {
        "convert_jpg": "jpg",
        "convert_png": "png",
        "convert_webp": "webp",
        "convert_bmp": "bmp",
    }

    output_format = formats.get(data)

    if not output_format:
        await query.answer(
            "Invalid image format.",
            show_alert=True,
        )
        return

    await handle_convert_format(
        update,
        context,
        output_format,
    )


# =========================================================
# QR CALLBACKS
# =========================================================

async def qr_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == "qr_menu":
        await query.answer()
        context.user_data.clear()

        await query.edit_message_text(
            "🔳 <b>QR Tools</b>\n\n"
            "একটি QR tool select করো।",
            parse_mode="HTML",
            reply_markup=qr_menu(),
        )
        return

    if data == "qr_text":
        await start_qr_text(update, context)
        return

    if data == "qr_url":
        await start_qr_url(update, context)
        return

    if data == "qr_wifi":
        await start_qr_wifi(update, context)
        return

    if data == "qr_contact":
        await start_qr_contact(update, context)
        return

    if data == "qr_email":
        await start_qr_email(update, context)
        return

    if data == "qr_phone":
        await start_qr_phone(update, context)
        return

    if data == "qr_scan":
        await start_qr_scan(update, context)
        return

    if data == "qr_to_pdf":
        await start_qr_to_pdf(update, context)
        return


# =========================================================
# AUDIO CALLBACKS
# =========================================================

async def audio_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    data = query.data

    if data == "audio_menu":
        await query.answer()
        context.user_data.clear()

        await query.edit_message_text(
            "🎙️ <b>Audio Tools</b>\n\n"
            "একটি audio tool select করো।",
            parse_mode="HTML",
            reply_markup=audio_menu(),
        )
        return

    if data == "text_to_voice":
        await start_text_to_voice(update, context)
        return

    if data == "voice_changer":
        await start_voice_changer(update, context)
        return

    if data == "audio_cutter":
        await start_audio_cutter(update, context)
        return

    if data == "audio_converter":
        await start_audio_converter(update, context)
        return

    if data == "volume_changer":
        await start_volume_changer(update, context)
        return

    if data == "audio_info":
        await start_audio_info(update, context)
        return


async def audio_format_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    data = query.data

    formats = {
        "audio_mp3": "mp3",
        "audio_wav": "wav",
        "audio_ogg": "ogg",
        "audio_m4a": "m4a",
        "audio_flac": "flac",
    }

    output_format = formats.get(data)

    if not output_format:
        await query.answer(
            "Invalid audio format.",
            show_alert=True,
        )
        return

    await handle_audio_format(
        update,
        context,
        output_format,
    )


# =========================================================
# FILE CALLBACKS
# =========================================================

async def file_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    data = query.data

    if data == "file_menu":
        await query.answer()
        context.user_data.clear()

        await query.edit_message_text(
            "🛠️ <b>File Tools</b>\n\n"
            "একটি file tool select করো।",
            parse_mode="HTML",
            reply_markup=file_menu(),
        )
        return

    if data == "create_zip":
        await start_create_zip(update, context)
        return

    if data == "extract_zip":
        await start_extract_zip(update, context)
        return

    if data == "file_converter":
        await start_file_converter(update, context)
        return

    if data == "file_info":
        await start_file_info(update, context)
        return


# =========================================================
# DEVELOPER / HELP
# =========================================================

async def developer_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    context.user_data.clear()

    await query.edit_message_text(
        "👨‍💻 <b>Developer</b>\n\n"
        f"Name: <b>{DEVELOPER_NAME}</b>\n"
        f"Telegram: <b>{DEVELOPER_USERNAME}</b>",
        parse_mode="HTML",
        reply_markup=developer_menu(DEVELOPER_USERNAME),
    )


async def help_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    context.user_data.clear()

    await query.edit_message_text(
        "ℹ️ <b>Help</b>\n\n"
        "📄 PDF Tools — PDF তৈরি ও process\n"
        "🖼️ Image Tools — resize, compress, convert\n"
        "🔳 QR Tools — QR generate ও scan\n"
        "🎙️ Audio Tools — voice ও audio processing\n"
        "🛠️ File Tools — ZIP ও file information\n\n"
        "কোনো tool ব্যবহার করতে Main Menu থেকে option select করো।",
        parse_mode="HTML",
        reply_markup=help_menu(),
    )


# =========================================================
# ADMIN
# =========================================================

async def admin_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.effective_user:
        return

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(
            "⛔ এই command শুধু admin-এর জন্য।"
        )
        return

    await update.message.reply_text(
        "🛠️ <b>Admin Panel</b>\n\n"
        "একটি option select করো।",
        parse_mode="HTML",
        reply_markup=admin_menu(),
    )


async def admin_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query

    if not update.effective_user:
        return

    if update.effective_user.id != ADMIN_ID:
        await query.answer(
            "⛔ Admin only.",
            show_alert=True,
        )
        return

    await query.answer()

    data = query.data

    if data == "admin_statistics":
        await query.edit_message_text(
            "📊 <b>Statistics</b>\n\n"
            "Database system বর্তমানে active নেই।",
            parse_mode="HTML",
            reply_markup=admin_menu(),
        )
        return

    if data == "admin_users":
        await query.edit_message_text(
            "👥 <b>Users</b>\n\n"
            "Database system বর্তমানে active নেই।",
            parse_mode="HTML",
            reply_markup=admin_menu(),
        )
        return

    if data == "admin_broadcast":
        await query.edit_message_text(
            "📢 <b>Broadcast</b>\n\n"
            "Database system বর্তমানে active নেই।",
            parse_mode="HTML",
            reply_markup=admin_menu(),
        )
        return

    if data == "admin_ban":
        await query.edit_message_text(
            "🚫 <b>Ban</b>\n\n"
            "Database system বর্তমানে active নেই।",
            parse_mode="HTML",
            reply_markup=admin_menu(),
        )
        return

    if data == "admin_unban":
        await query.edit_message_text(
            "✅ <b>Unban</b>\n\n"
            "Database system বর্তমানে active নেই।",
            parse_mode="HTML",
            reply_markup=admin_menu(),
        )
        return

    if data == "admin_maintenance":
        await query.edit_message_text(
            "🔧 <b>Maintenance</b>\n\n"
            "বর্তমানে config.py থেকে maintenance mode control করা হয়।",
            parse_mode="HTML",
            reply_markup=admin_menu(),
        )
        return


# =========================================================
# TEXT HANDLER
# =========================================================

async def text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    data = context.user_data

    if data.get("pdf_action") == "text_to_pdf":
        await handle_pdf_text(update, context)
        return

    if data.get("pdf_action") == "protect":
        if data.get("protect_waiting_password"):
            await handle_protect_password(update, context)
            return

    if data.get("image_action") == "resize":
        if data.get("image_waiting_dimensions"):
            await handle_image_text(update, context)
            return

    if data.get("qr_action"):
        await handle_qr_text(update, context)
        return

    if data.get("audio_action") == "text_to_voice":
        await handle_audio_text(update, context)
        return

    if data.get("audio_waiting_volume"):
        await handle_volume_text(update, context)
        return

    if data.get("audio_waiting_cut"):
        await handle_cut_text(update, context)
        return

    await update.message.reply_text(
        "ℹ️ কোনো active tool নেই।\n\n"
        "/start দিয়ে Main Menu খুলো।"
    )


# =========================================================
# PHOTO HANDLER
# =========================================================

async def photo_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    data = context.user_data

    if data.get("pdf_action") == "image_to_pdf":
        await handle_pdf_image(update, context)
        return

    if data.get("image_action"):
        await handle_image(update, context)
        return

    if data.get("qr_action") == "scan":
        await handle_qr_image(update, context)
        return


# =========================================================
# DOCUMENT HANDLER
# =========================================================

async def document_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    data = context.user_data

    if data.get("pdf_action") in {
        "merge",
        "split",
        "pdf_to_text",
        "pdf_to_image",
        "protect",
    }:
        await handle_pdf_document(update, context)
        return

    if data.get("qr_action") == "scan":
        await handle_qr_image(update, context)
        return

    if data.get("audio_action") in {
        "voice_changer",
        "cutter",
        "converter",
        "volume",
        "info",
    }:
        await handle_audio_file(update, context)
        return

    if data.get("file_action") in {
        "create_zip",
        "extract_zip",
        "file_info",
    }:
        await handle_file_document(update, context)
        return


# =========================================================
# AUDIO / VOICE HANDLERS
# =========================================================

async def audio_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    await handle_audio_file(update, context)


async def voice_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    await handle_audio_file(update, context)


# =========================================================
# DONE COMMAND
# =========================================================

async def done_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    data = context.user_data

    if data.get("pdf_action") == "image_to_pdf":
        await done_pdf(update, context)
        return

    if data.get("pdf_action") == "merge":
        await done_merge_pdf(update, context)
        return

    if data.get("image_action") == "image_to_pdf":
        await done_image_to_pdf(update, context)
        return

    if data.get("file_action") == "create_zip":
        await done_create_zip(update, context)
        return

    await update.message.reply_text(
        "ℹ️ কোনো active multi-file operation নেই।"
    )


# =========================================================
# CANCEL COMMAND
# =========================================================

async def cancel_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()

    await update.message.reply_text(
        "❌ Current operation cancelled.\n\n"
        "🏠 Main Menu:",
        reply_markup=main_menu(),
    )


# =========================================================
# ERROR HANDLER
# =========================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):
    logger.error(
        "Unhandled exception:",
        exc_info=context.error,
    )


# =========================================================
# MAIN
# =========================================================

def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable is missing."
        )

    # -----------------------------------------------------
    # Start Render Web Server
    # -----------------------------------------------------

    web_thread = threading.Thread(
        target=start_web_server,
        daemon=True,
    )

    web_thread.start()

    logger.info(
        "Render web server started."
    )

    # -----------------------------------------------------
    # Telegram Application
    # -----------------------------------------------------

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(setup_menu_button)
        .build()
    )

    # -----------------------------------------------------
    # Commands
    # -----------------------------------------------------

    application.add_handler(
        CommandHandler(
            "start",
            start_command,
        )
    )

    application.add_handler(
        CommandHandler(
            "done",
            done_command,
        )
    )

    application.add_handler(
        CommandHandler(
            "cancel",
            cancel_command,
        )
    )

    application.add_handler(
        CommandHandler(
            "admin",
            admin_command,
        )
    )

    # -----------------------------------------------------
    # Callback Queries
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            home_command,
            pattern=r"^home$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            pdf_callback,
            pattern=r"^(pdf_menu|text_to_pdf|pdf_image_to_pdf|merge_pdf|split_pdf|pdf_to_image|pdf_to_text|protect_pdf)$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            image_callback,
            pattern=r"^(image_menu|resize_image|compress_image|convert_image|image_to_pdf|image_info)$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            image_format_callback,
            pattern=r"^convert_(jpg|png|webp|bmp)$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            qr_callback,
            pattern=r"^(qr_menu|qr_text|qr_url|qr_wifi|qr_contact|qr_email|qr_phone|qr_scan|qr_to_pdf)$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            audio_callback,
            pattern=r"^(audio_menu|text_to_voice|voice_changer|audio_cutter|audio_converter|volume_changer|audio_info)$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            audio_format_callback,
            pattern=r"^audio_(mp3|wav|ogg|m4a|flac)$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            file_callback,
            pattern=r"^(file_menu|create_zip|extract_zip|file_converter|file_info)$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            developer_callback,
            pattern=r"^developer$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            help_callback,
            pattern=r"^help$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            admin_callback,
            pattern=r"^admin_",
        )
    )

    # -----------------------------------------------------
    # Message Handlers
    # -----------------------------------------------------

    application.add_handler(
        MessageHandler(
            filters.PHOTO,
            photo_handler,
        )
    )

    application.add_handler(
        MessageHandler(
            filters.Document.ALL,
            document_handler,
        )
    )

    application.add_handler(
        MessageHandler(
            filters.AUDIO,
            audio_handler,
        )
    )

    application.add_handler(
        MessageHandler(
            filters.VOICE,
            voice_handler,
        )
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler,
        )
    )

    # -----------------------------------------------------
    # Error Handler
    # -----------------------------------------------------

    application.add_error_handler(
        error_handler
    )

    logger.info(
        "Telegram bot is starting..."
    )

    # -----------------------------------------------------
    # Start Polling
    # -----------------------------------------------------

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    main()
