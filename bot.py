import logging

from telegram import Update
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
    start_pdf_to_image,
    start_merge_pdf,
    start_split_pdf,
    start_pdf_to_text,
    start_protect_pdf,
    handle_pdf_text,
    handle_pdf_document,
    handle_image_to_pdf as handle_pdf_image_to_pdf,
    handle_protect_password,
    done_pdf,
    done_merge_pdf,
)

from handlers.image import (
    start_resize,
    start_compress,
    start_convert,
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
    handle_audio_file,
    handle_audio_text,
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


# ==========================================
# START
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    await update.message.reply_text(
        f"🤖 <b>{DEVELOPER_NAME} All-in-One Bot</b>\n\n"
        "এক জায়গায় PDF, Image, QR, Audio এবং File Tools।\n\n"
        "নিচের menu থেকে একটি option বেছে নাও।",
        reply_markup=main_menu(),
        parse_mode="HTML",
    )


# ==========================================
# MENU CALLBACKS
# ==========================================

async def menu_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    data = query.data

    if data == "home":
        context.user_data.clear()
        await query.answer()
        await query.edit_message_text(
            "🏠 <b>Main Menu</b>\n\n"
            "একটি tool select করো।",
            reply_markup=main_menu(),
            parse_mode="HTML",
        )
        return

    if data == "pdf_menu":
        context.user_data.clear()
        await query.answer()
        await query.edit_message_text(
            "📄 <b>PDF Tools</b>\n\n"
            "একটি PDF tool select করো।",
            reply_markup=pdf_menu(),
            parse_mode="HTML",
        )
        return

    if data == "image_menu":
        context.user_data.clear()
        await query.answer()
        await query.edit_message_text(
            "🖼️ <b>Image Tools</b>\n\n"
            "একটি image tool select করো।",
            reply_markup=image_menu(),
            parse_mode="HTML",
        )
        return

    if data == "qr_menu":
        context.user_data.clear()
        await query.answer()
        await query.edit_message_text(
            "🔳 <b>QR Tools</b>\n\n"
            "একটি QR tool select করো।",
            reply_markup=qr_menu(),
            parse_mode="HTML",
        )
        return

    if data == "audio_menu":
        context.user_data.clear()
        await query.answer()
        await query.edit_message_text(
            "🎙️ <b>Audio Tools</b>\n\n"
            "একটি audio tool select করো।",
            reply_markup=audio_menu(),
            parse_mode="HTML",
        )
        return

    if data == "file_menu":
        context.user_data.clear()
        await query.answer()
        await query.edit_message_text(
            "🛠️ <b>File Tools</b>\n\n"
            "একটি file tool select করো।",
            reply_markup=file_menu(),
            parse_mode="HTML",
        )
        return

    if data == "developer":
        context.user_data.clear()
        await query.answer()
        await query.edit_message_text(
            "👨‍💻 <b>Developer</b>\n\n"
            f"Name: <b>{DEVELOPER_NAME}</b>\n"
            f"Telegram: <b>{DEVELOPER_USERNAME}</b>",
            reply_markup=developer_menu(
                DEVELOPER_USERNAME
            ),
            parse_mode="HTML",
        )
        return

    if data == "help":
        context.user_data.clear()
        await query.answer()
        await query.edit_message_text(
            "ℹ️ <b>Help</b>\n\n"
            "📄 PDF Tools — PDF তৈরি ও edit\n"
            "🖼️ Image Tools — resize, compress, convert\n"
            "🔳 QR Tools — QR generate ও scan\n"
            "🎙️ Audio Tools — voice ও audio processing\n"
            "🛠️ File Tools — ZIP ও file information\n\n"
            "কোনো কাজ শেষ করার জন্য bot যেটা চাইবে "
            "সেটাই পাঠাও।",
            reply_markup=help_menu(),
            parse_mode="HTML",
        )
        return


# ==========================================
# PDF CALLBACKS
# ==========================================

async def pdf_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    data = query.data

    handlers = {
        "text_to_pdf": start_text_to_pdf,
        "pdf_image_to_pdf": start_pdf_image_to_pdf,
        "merge_pdf": start_merge_pdf,
        "split_pdf": start_split_pdf,
        "pdf_to_image": start_pdf_to_image,
        "pdf_to_text": start_pdf_to_text,
        "protect_pdf": start_protect_pdf,
    }

    handler = handlers.get(data)

    if handler:
        await handler(update, context)


# ==========================================
# IMAGE CALLBACKS
# ==========================================

async def image_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    data = query.data

    handlers = {
        "resize_image": start_resize,
        "compress_image": start_compress,
        "convert_image": start_convert,
        "image_to_pdf": start_image_to_pdf,
        "image_info": start_image_info,
    }

    handler = handlers.get(data)

    if handler:
        await handler(update, context)


async def image_format_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query

    formats = {
        "convert_jpg": "jpg",
        "convert_png": "png",
        "convert_webp": "webp",
        "convert_bmp": "bmp",
    }

    output_format = formats.get(query.data)

    if output_format:
        await handle_convert_format(
            update,
            context,
            output_format,
        )


# ==========================================
# QR CALLBACKS
# ==========================================

async def qr_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    data = query.data

    handlers = {
        "qr_text": start_qr_text,
        "qr_url": start_qr_url,
        "qr_wifi": start_qr_wifi,
        "qr_contact": start_qr_contact,
        "qr_email": start_qr_email,
        "qr_phone": start_qr_phone,
        "qr_scan": start_qr_scan,
        "qr_to_pdf": start_qr_to_pdf,
    }

    handler = handlers.get(data)

    if handler:
        await handler(update, context)


# ==========================================
# AUDIO CALLBACKS
# ==========================================

async def audio_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    data = query.data

    handlers = {
        "text_to_voice": start_text_to_voice,
        "voice_changer": start_voice_changer,
        "audio_cutter": start_audio_cutter,
        "audio_converter": start_audio_converter,
        "volume_changer": start_volume_changer,
        "audio_info": start_audio_info,
    }

    handler = handlers.get(data)

    if handler:
        await handler(update, context)


async def audio_format_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query

    formats = {
        "audio_mp3": "mp3",
        "audio_wav": "wav",
        "audio_ogg": "ogg",
        "audio_m4a": "m4a",
        "audio_flac": "flac",
    }

    output_format = formats.get(query.data)

    if output_format:
        await handle_audio_format(
            update,
            context,
            output_format,
        )


# ==========================================
# FILE CALLBACKS
# ==========================================

async def file_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    data = query.data

    handlers = {
        "create_zip": start_create_zip,
        "extract_zip": start_extract_zip,
        "file_converter": start_file_converter,
        "file_info": start_file_info,
    }

    handler = handlers.get(data)

    if handler:
        await handler(update, context)


# ==========================================
# ADMIN
# ==========================================

async def admin_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(
            "⛔ Access denied."
        )
        return

    await update.message.reply_text(
        "🛠️ <b>Admin Panel</b>",
        reply_markup=admin_menu(),
        parse_mode="HTML",
    )


async def admin_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query

    if (
        not update.effective_user
        or update.effective_user.id != ADMIN_ID
    ):
        await query.answer(
            "Access denied.",
            show_alert=True,
        )
        return

    await query.answer()

    await query.message.reply_text(
        "ℹ️ এই admin feature-এর জন্য "
        "database/backend এখনো active করা হয়নি।"
    )


# ==========================================
# TEXT HANDLER
# ==========================================

async def text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    data = context.user_data

    if data.get("pdf_action") == "text_to_pdf":
        await handle_pdf_text(
            update,
            context,
        )
        return

    if data.get("pdf_action") == "protect":
        if data.get("protect_waiting_password"):
            await handle_protect_password(
                update,
                context,
            )
            return

    if data.get("image_waiting_dimensions"):
        await handle_image_text(
            update,
            context,
        )
        return

    if data.get("audio_action") == "text_to_voice":
        await handle_audio_text(
            update,
            context,
        )
        return

    if data.get("audio_waiting_volume"):
        await handle_volume_text(
            update,
            context,
        )
        return

    if data.get("audio_waiting_cut"):
        await handle_cut_text(
            update,
            context,
        )
        return

    if data.get("qr_action"):
        await handle_qr_text(
            update,
            context,
        )
        return

    await update.message.reply_text(
        "ℹ️ আগে একটি tool select করো।",
        reply_markup=main_menu(),
    )


# ==========================================
# PHOTO HANDLER
# ==========================================

async def photo_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    data = context.user_data

    if data.get("qr_action") in {
        "scan",
        "qr_to_pdf",
    }:
        await handle_qr_image(
            update,
            context,
        )
        return

    if data.get("pdf_action") == "image_to_pdf":
        await handle_pdf_image_to_pdf(
            update,
            context,
        )
        return

    if data.get("image_action"):
        await handle_image(
            update,
            context,
        )
        return

    await update.message.reply_text(
        "ℹ️ আগে Image Tools থেকে একটি option select করো।"
    )


# ==========================================
# DOCUMENT HANDLER
# ==========================================

async def document_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    data = context.user_data

    if data.get("qr_action") in {
        "scan",
        "qr_to_pdf",
    }:
        await handle_qr_image(
            update,
            context,
        )
        return

    if data.get("pdf_action"):
        await handle_pdf_document(
            update,
            context,
        )
        return

    if data.get("audio_action"):
        await handle_audio_file(
            update,
            context,
        )
        return

    if data.get("file_action"):
        await handle_file_document(
            update,
            context,
        )
        return

    await update.message.reply_text(
        "ℹ️ আগে একটি tool select করো।"
    )


# ==========================================
# AUDIO / VOICE
# ==========================================

async def audio_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if context.user_data.get(
        "audio_action"
    ):
        await handle_audio_file(
            update,
            context,
        )


async def voice_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if context.user_data.get(
        "audio_action"
    ):
        await handle_audio_file(
            update,
            context,
        )


# ==========================================
# DONE
# ==========================================

async def done_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    data = context.user_data

    if data.get("pdf_action") == "image_to_pdf":
        await done_pdf(
            update,
            context,
        )
        return

    if data.get("pdf_action") == "merge":
        await done_merge_pdf(
            update,
            context,
        )
        return

    if data.get("image_action") == "image_to_pdf":
        await done_image_to_pdf(
            update,
            context,
        )
        return

    if data.get("file_action") == "create_zip":
        await done_create_zip(
            update,
            context,
        )
        return

    await update.message.reply_text(
        "ℹ️ কোনো active multi-file operation নেই।"
    )


# ==========================================
# CANCEL
# ==========================================

async def cancel_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()

    await update.message.reply_text(
        "❌ Current operation cancelled.",
        reply_markup=main_menu(),
    )


# ==========================================
# ERROR HANDLER
# ==========================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):
    logger.exception(
        "Unhandled exception:",
        exc_info=context.error,
    )


# ==========================================
# MAIN
# ==========================================

def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable is missing."
        )

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # Commands
    application.add_handler(
        CommandHandler(
            "start",
            start,
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

    # Main menus
    application.add_handler(
        CallbackQueryHandler(
            menu_callback,
            pattern=r"^(home|pdf_menu|image_menu|qr_menu|audio_menu|file_menu|developer|help)$",
        )
    )

    # PDF
    application.add_handler(
        CallbackQueryHandler(
            pdf_callback,
            pattern=r"^(text_to_pdf|pdf_image_to_pdf|merge_pdf|split_pdf|pdf_to_image|pdf_to_text|protect_pdf)$",
        )
    )

    # Image
    application.add_handler(
        CallbackQueryHandler(
            image_callback,
            pattern=r"^(resize_image|compress_image|convert_image|image_to_pdf|image_info)$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            image_format_callback,
            pattern=r"^convert_(jpg|png|webp|bmp)$",
        )
    )

    # QR
    application.add_handler(
        CallbackQueryHandler(
            qr_callback,
            pattern=r"^(qr_text|qr_url|qr_wifi|qr_contact|qr_email|qr_phone|qr_scan|qr_to_pdf)$",
        )
    )

    # Audio
    application.add_handler(
        CallbackQueryHandler(
            audio_callback,
            pattern=r"^(text_to_voice|voice_changer|audio_cutter|audio_converter|volume_changer|audio_info)$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            audio_format_callback,
            pattern=r"^audio_(mp3|wav|ogg|m4a|flac)$",
        )
    )

    # File
    application.add_handler(
        CallbackQueryHandler(
            file_callback,
            pattern=r"^(create_zip|extract_zip|file_converter|file_info)$",
        )
    )

    # Admin callbacks
    application.add_handler(
        CallbackQueryHandler(
            admin_callback,
            pattern=r"^admin_",
        )
    )

    # Text
    application.add_handler(
        MessageHandler(
            filters.TEXT
            & ~filters.COMMAND,
            text_handler,
        )
    )

    # Photos
    application.add_handler(
        MessageHandler(
            filters.PHOTO,
            photo_handler,
        )
    )

    # Documents
    application.add_handler(
        MessageHandler(
            filters.Document.ALL,
            document_handler,
        )
    )

    # Audio
    application.add_handler(
        MessageHandler(
            filters.AUDIO,
            audio_handler,
        )
    )

    # Voice
    application.add_handler(
        MessageHandler(
            filters.VOICE,
            voice_handler,
        )
    )

    application.add_error_handler(
        error_handler
    )

    logger.info(
        "Bot is starting..."
    )

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
