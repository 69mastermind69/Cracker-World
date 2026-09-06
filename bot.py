import logging
import os

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN, ADMIN_ID, BOT_NAME

# =========================
# PDF HANDLERS
# =========================
from handlers.pdf import (
    start_text_to_pdf,
    start_image_to_pdf as start_pdf_image_to_pdf,
    start_merge_pdf,
    start_split_pdf,
    start_pdf_to_image,
    start_pdf_to_text,
    start_protect_pdf,
    handle_pdf_text,
    handle_pdf_document,
    handle_pdf_to_image,
    handle_protect_password,
    done_pdf,
)

# =========================
# IMAGE HANDLERS
# =========================
from handlers.image import (
    start_resize_image,
    start_compress_image,
    start_convert_image,
    start_image_info,
    start_image_to_pdf as start_image_tool_to_pdf,
    handle_image,
    handle_image_text,
    handle_convert_format,
    done_image_to_pdf,
)

# =========================
# QR HANDLERS
# =========================
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

# =========================
# AUDIO HANDLERS
# =========================
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
)

# =========================
# KEYBOARDS
# =========================
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

# =========================
# FILE SERVICE
# =========================
from services.file_service import (
    get_file_info,
    create_zip,
    extract_zip,
)


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ============================================================
# TEMP USER STATE
# ============================================================

user_states = {}


def set_state(user_id: int, state: str):
    user_states[user_id] = state


def get_state(user_id: int):
    return user_states.get(user_id)


def clear_state(user_id: int):
    user_states.pop(user_id, None)


# ============================================================
# START
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = update.effective_user.id

    clear_state(user_id)

    await update.message.reply_text(
        f"🤖 *{BOT_NAME}*\n\n"
        "Welcome!\n"
        "Choose a tool from the menu below.",
        reply_markup=main_menu(),
        parse_mode="Markdown",
    )


# ============================================================
# HELP
# ============================================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "ℹ️ *Help*\n\n"
            "Choose a category from the main menu and follow the instructions.\n\n"
            "📄 PDF Tools\n"
            "🖼️ Image Tools\n"
            "🔳 QR Tools\n"
            "🎙️ Audio Tools\n"
            "🛠️ File Tools\n\n"
            "If something fails, try sending the file again.",
            reply_markup=help_menu(),
            parse_mode="Markdown",
        )


# ============================================================
# MAIN CALLBACK ROUTER
# ============================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query

    if not query:
        return

    await query.answer()

    data = query.data
    user_id = query.from_user.id

    # ========================================================
    # MAIN MENUS
    # ========================================================

    if data in ("main_menu", "home"):
        clear_state(user_id)

        await query.edit_message_text(
            "🤖 *Main Menu*\n\nChoose a tool:",
            reply_markup=main_menu(),
            parse_mode="Markdown",
        )
        return

    if data in ("pdf_menu", "pdf_tools"):
        clear_state(user_id)

        await query.edit_message_text(
            "📄 *PDF Tools*\n\nChoose an option:",
            reply_markup=pdf_menu(),
            parse_mode="Markdown",
        )
        return

    if data in ("image_menu", "image_tools"):
        clear_state(user_id)

        await query.edit_message_text(
            "🖼️ *Image Tools*\n\nChoose an option:",
            reply_markup=image_menu(),
            parse_mode="Markdown",
        )
        return

    if data in ("qr_menu", "qr_tools"):
        clear_state(user_id)

        await query.edit_message_text(
            "🔳 *QR Tools*\n\nChoose an option:",
            reply_markup=qr_menu(),
            parse_mode="Markdown",
        )
        return

    if data in ("audio_menu", "audio_tools"):
        clear_state(user_id)

        await query.edit_message_text(
            "🎙️ *Audio Tools*\n\nChoose an option:",
            reply_markup=audio_menu(),
            parse_mode="Markdown",
        )
        return

    if data in ("file_menu", "file_tools"):
        clear_state(user_id)

        await query.edit_message_text(
            "🛠️ *File Tools*\n\nChoose an option:",
            reply_markup=file_menu(),
            parse_mode="Markdown",
        )
        return

    if data in ("developer", "developer_menu"):
        clear_state(user_id)

        await query.edit_message_text(
            "👨‍💻 *Developer*\n\n"
            "Name: MASTERMIND\n"
            "Telegram: @Do_x_Die",
            reply_markup=developer_menu(),
            parse_mode="Markdown",
        )
        return

    if data in ("help", "help_menu"):
        clear_state(user_id)

        await query.edit_message_text(
            "ℹ️ *Help*\n\n"
            "Select a tool from the main menu and follow the instructions.",
            reply_markup=help_menu(),
            parse_mode="Markdown",
        )
        return

    # ========================================================
    # PDF TOOLS
    # ========================================================

    if data == "text_to_pdf":
        set_state(user_id, "pdf_text")
        await start_text_to_pdf(update, context)
        return

    if data == "pdf_image_to_pdf":
        set_state(user_id, "pdf_image_to_pdf")
        await start_pdf_image_to_pdf(update, context)
        return

    if data == "merge_pdf":
        set_state(user_id, "merge_pdf")
        await start_merge_pdf(update, context)
        return

    if data == "split_pdf":
        set_state(user_id, "split_pdf")
        await start_split_pdf(update, context)
        return

    if data == "pdf_to_image":
        set_state(user_id, "pdf_to_image")
        await start_pdf_to_image(update, context)
        return

    if data == "pdf_to_text":
        set_state(user_id, "pdf_to_text")
        await start_pdf_to_text(update, context)
        return

    if data == "protect_pdf":
        set_state(user_id, "protect_pdf")
        await start_protect_pdf(update, context)
        return

    # ========================================================
    # IMAGE TOOLS
    # ========================================================

    if data in ("resize_image", "resize"):
        set_state(user_id, "resize_image")
        await start_resize_image(update, context)
        return

    if data in ("compress_image", "compress"):
        set_state(user_id, "compress_image")
        await start_compress_image(update, context)
        return

    if data in ("convert_image", "convert"):
        set_state(user_id, "convert_image")
        await start_convert_image(update, context)
        return

    if data == "image_to_pdf":
        set_state(user_id, "image_to_pdf")
        await start_image_tool_to_pdf(update, context)
        return

    if data in ("image_info", "info_image"):
        set_state(user_id, "image_info")
        await start_image_info(update, context)
        return

    # Image conversion format buttons
    if data.startswith("convert_"):
        await handle_convert_format(update, context)
        return

    # ========================================================
    # QR TOOLS
    # ========================================================

    if data in ("qr_text", "text_qr"):
        set_state(user_id, "qr_text")
        await start_qr_text(update, context)
        return

    if data in ("qr_url", "url_qr"):
        set_state(user_id, "qr_url")
        await start_qr_url(update, context)
        return

    if data in ("qr_wifi", "wifi_qr"):
        set_state(user_id, "qr_wifi")
        await start_qr_wifi(update, context)
        return

    if data in ("qr_contact", "contact_qr"):
        set_state(user_id, "qr_contact")
        await start_qr_contact(update, context)
        return

    if data in ("qr_email", "email_qr"):
        set_state(user_id, "qr_email")
        await start_qr_email(update, context)
        return

    if data in ("qr_phone", "phone_qr"):
        set_state(user_id, "qr_phone")
        await start_qr_phone(update, context)
        return

    if data in ("qr_scan", "scan_qr"):
        set_state(user_id, "qr_scan")
        await start_qr_scan(update, context)
        return

    if data in ("qr_to_pdf", "qr_pdf"):
        set_state(user_id, "qr_to_pdf")
        await start_qr_to_pdf(update, context)
        return

    # ========================================================
    # AUDIO TOOLS
    # ========================================================

    if data in ("text_to_voice", "text_to_audio"):
        set_state(user_id, "text_to_voice")
        await start_text_to_voice(update, context)
        return

    if data in ("voice_changer", "change_voice"):
        set_state(user_id, "voice_changer")
        await start_voice_changer(update, context)
        return

    if data in ("audio_cutter", "cut_audio"):
        set_state(user_id, "audio_cutter")
        await start_audio_cutter(update, context)
        return

    if data in ("audio_converter", "convert_audio"):
        set_state(user_id, "audio_converter")
        await start_audio_converter(update, context)
        return

    if data in ("volume_changer", "change_volume"):
        set_state(user_id, "volume_changer")
        await start_volume_changer(update, context)
        return

    if data in ("audio_info", "info_audio"):
        set_state(user_id, "audio_info")
        await start_audio_info(update, context)
        return

    # Audio output format buttons
    if data.startswith("audio_format_"):
        await handle_audio_format(update, context)
        return

    # ========================================================
    # FILE TOOLS
    # ========================================================

    if data in ("create_zip", "zip_create"):
        set_state(user_id, "create_zip")

        await query.edit_message_text(
            "🗜️ *Create ZIP*\n\n"
            "Send the files you want to put into a ZIP.\n"
            "When finished, send /done.",
            parse_mode="Markdown",
        )
        return

    if data in ("extract_zip", "zip_extract"):
        set_state(user_id, "extract_zip")

        await query.edit_message_text(
            "📦 *Extract ZIP*\n\n"
            "Send a ZIP file.",
            parse_mode="Markdown",
        )
        return

    if data in ("file_converter", "convert_file"):
        set_state(user_id, "file_converter")

        await query.edit_message_text(
            "🔄 *File Converter*\n\n"
            "Send the file you want to convert.",
            parse_mode="Markdown",
        )
        return

    if data in ("file_info", "info_file"):
        set_state(user_id, "file_info")

        await query.edit_message_text(
            "ℹ️ *File Info*\n\n"
            "Send a file to inspect it.",
            parse_mode="Markdown",
        )
        return

    # ========================================================
    # ADMIN
    # ========================================================

    if data.startswith("admin_"):
        if user_id != ADMIN_ID:
            await query.answer(
                "❌ You are not authorized.",
                show_alert=True,
            )
            return

        if data == "admin_stats":
            await query.edit_message_text(
                "📊 Statistics\n\n"
                "Database/statistics system is currently disabled."
            )
            return

        if data == "admin_users":
            await query.edit_message_text(
                "👥 Users\n\n"
                "User database is currently disabled."
            )
            return

        if data == "admin_broadcast":
            await query.edit_message_text(
                "📢 Broadcast\n\n"
                "Broadcast system is currently disabled."
            )
            return

        if data == "admin_ban":
            await query.edit_message_text(
                "🚫 Ban\n\n"
                "Ban system requires a database and is currently disabled."
            )
            return

        if data == "admin_unban":
            await query.edit_message_text(
                "✅ Unban\n\n"
                "Unban system requires a database and is currently disabled."
            )
            return

        if data == "admin_maintenance":
            await query.edit_message_text(
                "🛠️ Maintenance\n\n"
                "Maintenance control is currently disabled."
            )
            return

    # ========================================================
    # UNKNOWN CALLBACK
    # ========================================================

    await query.answer(
        "This button is not available.",
        show_alert=True,
    )


# ============================================================
# TEXT MESSAGE ROUTER
# ============================================================

async def text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message or not update.effective_user:
        return

    user_id = update.effective_user.id
    state = get_state(user_id)

    if not state:
        await update.message.reply_text(
            "Please choose a tool from the menu.",
            reply_markup=main_menu(),
        )
        return

    # ========================================================
    # PDF TEXT
    # ========================================================

    if state == "pdf_text":
        await handle_pdf_text(update, context)
        return

    # ========================================================
    # PDF PASSWORD
    # ========================================================

    if state in ("protect_pdf_password", "pdf_password"):
        await handle_protect_password(update, context)
        return

    # ========================================================
    # IMAGE TEXT INPUT
    # ========================================================

    if state in (
        "resize_image",
        "compress_image",
        "convert_image",
    ):
        await handle_image_text(update, context)
        return

    # ========================================================
    # AUDIO TEXT INPUT
    # ========================================================

    if state in (
        "text_to_voice",
        "audio_cutter_waiting",
        "volume_waiting",
    ):
        await handle_audio_text(update, context)
        return

    # ========================================================
    # QR TEXT INPUT
    # ========================================================

    if state.startswith("qr_"):
        await handle_qr_text(update, context)
        return

    await update.message.reply_text(
        "Please send the required file or input for this tool."
    )


# ============================================================
# PHOTO ROUTER
# ============================================================

async def photo_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message or not update.effective_user:
        return

    user_id = update.effective_user.id
    state = get_state(user_id)

    if not state:
        await update.message.reply_text(
            "Please choose an image tool first.",
            reply_markup=main_menu(),
        )
        return

    # QR scanner
    if state == "qr_scan":
        await handle_qr_image(update, context)
        return

    # PDF image -> PDF
    if state == "pdf_image_to_pdf":
        await handle_image(update, context)
        return

    # Image Tools
    if state in (
        "resize_image",
        "compress_image",
        "convert_image",
        "image_info",
        "image_to_pdf",
    ):
        await handle_image(update, context)
        return

    await update.message.reply_text(
        "This image is not expected for the current tool."
    )


# ============================================================
# DOCUMENT ROUTER
# ============================================================

async def document_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message or not update.effective_user:
        return

    user_id = update.effective_user.id
    state = get_state(user_id)

    if not state:
        await update.message.reply_text(
            "Please choose a tool first.",
            reply_markup=main_menu(),
        )
        return

    # ========================================================
    # PDF
    # ========================================================

    if state in (
        "merge_pdf",
        "split_pdf",
        "pdf_to_image",
        "pdf_to_text",
        "protect_pdf",
    ):
        await handle_pdf_document(update, context)
        return

    # ========================================================
    # AUDIO
    # ========================================================

    if state in (
        "audio_info",
        "audio_converter",
        "audio_cutter",
        "volume_changer",
        "voice_changer",
    ):
        await handle_audio_file(update, context)
        return

    # ========================================================
    # FILE INFO
    # ========================================================

    if state == "file_info":
        try:
            result = await get_file_info(update, context)

            if result:
                await update.message.reply_text(str(result))
        except Exception as exc:
            logger.exception("File info error")
            await update.message.reply_text(
                f"❌ Could not read file information.\n\n{exc}"
            )
        return

    # ========================================================
    # ZIP EXTRACTION
    # ========================================================

    if state == "extract_zip":
        try:
            await extract_zip(update, context)
        except Exception as exc:
            logger.exception("ZIP extraction error")
            await update.message.reply_text(
                f"❌ ZIP extraction failed.\n\n{exc}"
            )
        return

    # ========================================================
    # ZIP CREATION
    # ========================================================

    if state == "create_zip":
        try:
            await create_zip(update, context)
        except Exception as exc:
            logger.exception("ZIP creation error")
            await update.message.reply_text(
                f"❌ Could not add this file.\n\n{exc}"
            )
        return

    # ========================================================
    # IMAGE DOCUMENT
    # ========================================================

    if state in (
        "resize_image",
        "compress_image",
        "convert_image",
        "image_info",
        "image_to_pdf",
    ):
        await handle_image(update, context)
        return

    await update.message.reply_text(
        "❌ This file is not expected for the current tool."
    )


# ============================================================
# AUDIO / VOICE ROUTER
# ============================================================

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


# ============================================================
# /DONE
# ============================================================

async def done_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message or not update.effective_user:
        return

    user_id = update.effective_user.id
    state = get_state(user_id)

    if state in ("merge_pdf", "split_pdf"):
        try:
            await done_pdf(update, context)
        finally:
            clear_state(user_id)
        return

    if state in ("image_to_pdf", "pdf_image_to_pdf"):
        try:
            await done_image_to_pdf(update, context)
        finally:
            clear_state(user_id)
        return

    if state == "create_zip":
        try:
            await create_zip(update, context)
        finally:
            clear_state(user_id)
        return

    await update.message.reply_text(
        "Nothing is waiting for /done."
    )


# ============================================================
# ADMIN COMMAND
# ============================================================

async def admin_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message or not update.effective_user:
        return

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(
            "❌ You are not authorized to use the Admin panel."
        )
        return

    await update.message.reply_text(
        "👑 *Admin Panel*\n\nChoose an option:",
        reply_markup=admin_menu(),
        parse_mode="Markdown",
    )


# ============================================================
# CANCEL
# ============================================================

async def cancel_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message or not update.effective_user:
        return

    user_id = update.effective_user.id

    clear_state(user_id)

    await update.message.reply_text(
        "❌ Current operation cancelled.",
        reply_markup=main_menu(),
    )


# ============================================================
# ERROR HANDLER
# ============================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):
    logger.exception(
        "Unhandled exception:",
        exc_info=context.error,
    )


# ============================================================
# MAIN
# ============================================================

def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable is missing."
        )

    logger.info("All-in-One Telegram Bot starting...")

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # ========================================================
    # COMMANDS
    # ========================================================

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_handler(
        CommandHandler("admin", admin_command)
    )

    application.add_handler(
        CommandHandler("done", done_command)
    )

    application.add_handler(
        CommandHandler("cancel", cancel_command)
    )

    # ========================================================
    # CALLBACK BUTTONS
    # ========================================================

    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    # ========================================================
    # PHOTOS
    # ========================================================

    application.add_handler(
        MessageHandler(
            filters.PHOTO,
            photo_handler,
        )
    )

    # ========================================================
    # AUDIO
    # ========================================================

    application.add_handler(
        MessageHandler(
            filters.AUDIO,
            audio_handler,
        )
    )

    # ========================================================
    # VOICE
    # ========================================================

    application.add_handler(
        MessageHandler(
            filters.VOICE,
            voice_handler,
        )
    )

    # ========================================================
    # DOCUMENTS
    # ========================================================

    application.add_handler(
        MessageHandler(
            filters.Document.ALL,
            document_handler,
        )
    )

    # ========================================================
    # TEXT
    # ========================================================

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler,
        )
    )

    # ========================================================
    # ERROR
    # ========================================================

    application.add_error_handler(error_handler)

    logger.info("Bot polling started.")

    application.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES,
    )


if __name__ == "__main__":
    main()
