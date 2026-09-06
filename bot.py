import os
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
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
    DEVELOPER_CHANNEL,
)

from utils.keyboards import (
    main_menu,
    pdf_menu,
    image_menu,
    qr_menu,
    audio_menu,
    file_menu,
    developer_menu,
    admin_menu,
)

from handlers.pdf import (
    start_text_to_pdf,
    start_image_to_pdf,
    start_merge_pdf,
    start_split_pdf,
    start_pdf_to_text,
    start_protect_pdf,
    handle_pdf_text,
    handle_pdf_document,
    handle_protect_password,
    done_pdf,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    await update.message.reply_text(
        "🤖 Welcome to All-in-One Bot!\n\n"
        "নিচের menu থেকে একটি feature নির্বাচন করো:",
        reply_markup=main_menu(),
    )


# =========================
# ADMIN
# =========================

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(
            "❌ এই command শুধু admin-এর জন্য।"
        )
        return

    await update.message.reply_text(
        "👑 Admin Panel",
        reply_markup=admin_menu(),
    )


# =========================
# CALLBACK HANDLER
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    data = query.data

    # -------------------------
    # Main menu
    # -------------------------

    if data == "home":
        await query.edit_message_text(
            "🏠 Main Menu\n\nএকটি category নির্বাচন করো:",
            reply_markup=main_menu(),
        )
        return

    # -------------------------
    # Category menus
    # -------------------------

    if data == "pdf_menu":
        await query.edit_message_text(
            "📄 PDF Tools",
            reply_markup=pdf_menu(),
        )
        return

    if data == "image_menu":
        await query.edit_message_text(
            "🖼️ Image Tools",
            reply_markup=image_menu(),
        )
        return

    if data == "qr_menu":
        await query.edit_message_text(
            "🔳 QR Tools",
            reply_markup=qr_menu(),
        )
        return

    if data == "audio_menu":
        await query.edit_message_text(
            "🎙️ Audio Tools",
            reply_markup=audio_menu(),
        )
        return

    if data == "file_menu":
        await query.edit_message_text(
            "🛠️ File Tools",
            reply_markup=file_menu(),
        )
        return

    # -------------------------
    # PDF features
    # -------------------------

    if data == "text_to_pdf":
        await start_text_to_pdf(update, context)
        return

    if data == "image_to_pdf":
        await start_image_to_pdf(update, context)
        return

    if data == "merge_pdf":
        await start_merge_pdf(update, context)
        return

    if data == "split_pdf":
        await start_split_pdf(update, context)
        return

    if data == "pdf_to_text":
        await start_pdf_to_text(update, context)
        return

    if data == "protect_pdf":
        await start_protect_pdf(update, context)
        return

    # -------------------------
    # Developer
    # -------------------------

    if data == "developer":
        text = (
            "👨‍💻 Developer\n\n"
            f"Name: {DEVELOPER_NAME}\n"
        )

        if DEVELOPER_USERNAME:
            text += f"Telegram: {DEVELOPER_USERNAME}\n"

        if DEVELOPER_CHANNEL:
            text += f"Channel: {DEVELOPER_CHANNEL}\n"

        await query.edit_message_text(
            text,
            reply_markup=developer_menu(
                DEVELOPER_USERNAME,
                DEVELOPER_CHANNEL,
            ),
        )
        return

    # -------------------------
    # Help
    # -------------------------

    if data == "help":
        await query.edit_message_text(
            "ℹ️ Help\n\n"
            "1️⃣ একটি category নির্বাচন করো।\n"
            "2️⃣ যে tool দরকার সেটি নির্বাচন করো।\n"
            "3️⃣ Bot যা চাইবে সেই file/text পাঠাও।\n\n"
            "⚠️ বড় file process করতে বেশি সময় লাগতে পারে।",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔙 Back",
                        callback_data="home"
                    )
                ]
            ]),
        )
        return

    # -------------------------
    # Admin buttons
    # -------------------------

    admin_callbacks = {
        "admin_stats": "📊 Statistics",
        "admin_users": "👥 Users",
        "admin_broadcast": "📢 Broadcast",
        "admin_ban": "🚫 Ban User",
        "admin_unban": "✅ Unban User",
        "admin_maintenance": "🔧 Maintenance",
    }

    if data in admin_callbacks:
        if update.effective_user.id != ADMIN_ID:
            await query.edit_message_text(
                "❌ Unauthorized."
            )
            return

        await query.edit_message_text(
            f"{admin_callbacks[data]}\n\n"
            "এই admin feature পরবর্তী ধাপে connect করা হবে।",
            reply_markup=admin_menu(),
        )
        return

    # -------------------------
    # Future features
    # -------------------------

    future_features = {
        "resize_image": "📐 Resize",
        "compress_image": "🗜️ Compress",
        "convert_image": "🔄 Convert Image",
        "image_info": "ℹ️ Image Info",

        "qr_text": "📝 Text → QR",
        "qr_url": "🌐 URL → QR",
        "qr_wifi": "📶 Wi-Fi → QR",
        "qr_contact": "👤 Contact → QR",
        "qr_email": "📧 Email → QR",
        "qr_phone": "📱 Phone → QR",
        "qr_scan": "🔍 Scan QR",
        "qr_to_pdf": "📄 QR → PDF",

        "text_to_voice": "🗣️ Text → Voice",
        "voice_changer": "🎭 Voice Changer",
        "audio_cutter": "✂️ Audio Cutter",
        "audio_converter": "🔄 Audio Converter",
        "volume_changer": "🔊 Volume Changer",
        "audio_info": "ℹ️ Audio Info",

        "create_zip": "🗜️ Create ZIP",
        "extract_zip": "📦 Extract ZIP",
        "file_converter": "🔄 File Converter",
        "file_info": "ℹ️ File Info",
    }

    if data in future_features:
        await query.edit_message_text(
            f"{future_features[data]}\n\n"
            "🔨 এই feature-এর processing module "
            "পরবর্তী ধাপে যুক্ত করা হবে।",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔙 Back",
                        callback_data="home"
                    )
                ]
            ]),
        )
        return


# =========================
# TEXT HANDLER
# =========================

async def text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    action = context.user_data.get("pdf_action")

    if action == "text_to_pdf":
        await handle_pdf_text(update, context)
        return

    if context.user_data.get("protect_pdf_path"):
        await handle_protect_password(update, context)
        return


# =========================
# DOCUMENT HANDLER
# =========================

async def document_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await handle_pdf_document(update, context)


# =========================
# DONE COMMAND
# =========================

async def done_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await done_pdf(update, context)


# =========================
# ERROR HANDLER
# =========================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):
    logger.error(
        "Exception while handling update:",
        exc_info=context.error,
    )


# =========================
# MAIN
# =========================

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
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("admin", admin)
    )

    application.add_handler(
        CommandHandler("done", done_command)
    )

    # Buttons
    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    # Text messages
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler,
        )
    )

    # Documents
    application.add_handler(
        MessageHandler(
            filters.Document.ALL,
            document_handler,
        )
    )

    application.add_error_handler(error_handler)

    logger.info("Bot started.")

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
