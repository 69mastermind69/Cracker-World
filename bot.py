import logging

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
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
    handle_image,
)


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# =========================================================
# START COMMAND
# =========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    context.user_data.clear()

    await update.message.reply_text(
        "🤖 Welcome to All-in-One Bot!\n\n"
        "একটি feature নির্বাচন করো:",
        reply_markup=main_menu(),
    )


# =========================================================
# ADMIN COMMAND
# =========================================================

async def admin(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not update.effective_user:
        return

    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text(
            "❌ এই panel শুধু Admin-এর জন্য।"
        )
        return

    await update.message.reply_text(
        "👑 Admin Panel\n\n"
        "নিচের option থেকে নির্বাচন করো:",
        reply_markup=admin_menu(),
    )


# =========================================================
# BUTTON HANDLER
# =========================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    if not query:
        return

    await query.answer()

    data = query.data

    # =====================================================
    # HOME
    # =====================================================

    if data == "home":
        context.user_data.clear()

        await query.edit_message_text(
            "🏠 Main Menu\n\n"
            "একটি category নির্বাচন করো:",
            reply_markup=main_menu(),
        )
        return

    # =====================================================
    # PDF MENU
    # =====================================================

    if data == "pdf_menu":
        await query.edit_message_text(
            "📄 PDF Tools\n\n"
            "যে PDF tool দরকার সেটি নির্বাচন করো:",
            reply_markup=pdf_menu(),
        )
        return

    # =====================================================
    # IMAGE MENU
    # =====================================================

    if data == "image_menu":
        await query.edit_message_text(
            "🖼️ Image Tools\n\n"
            "যে image tool দরকার সেটি নির্বাচন করো:",
            reply_markup=image_menu(),
        )
        return

    # =====================================================
    # QR MENU
    # =====================================================

    if data == "qr_menu":
        await query.edit_message_text(
            "🔳 QR Tools\n\n"
            "যে QR tool দরকার সেটি নির্বাচন করো:",
            reply_markup=qr_menu(),
        )
        return

    # =====================================================
    # AUDIO MENU
    # =====================================================

    if data == "audio_menu":
        await query.edit_message_text(
            "🎙️ Audio Tools\n\n"
            "যে audio tool দরকার সেটি নির্বাচন করো:",
            reply_markup=audio_menu(),
        )
        return

    # =====================================================
    # FILE MENU
    # =====================================================

    if data == "file_menu":
        await query.edit_message_text(
            "🛠️ File Tools\n\n"
            "যে file tool দরকার সেটি নির্বাচন করো:",
            reply_markup=file_menu(),
        )
        return

    # =====================================================
    # PDF FEATURES
    # =====================================================

    if data == "text_to_pdf":
        await start_text_to_pdf(
            update,
            context
        )
        return

    if data == "image_to_pdf":
        await start_image_to_pdf(
            update,
            context
        )
        return

    if data == "merge_pdf":
        await start_merge_pdf(
            update,
            context
        )
        return

    if data == "split_pdf":
        await start_split_pdf(
            update,
            context
        )
        return

    if data == "pdf_to_text":
        await start_pdf_to_text(
            update,
            context
        )
        return

    if data == "protect_pdf":
        await start_protect_pdf(
            update,
            context
        )
        return

    # =====================================================
    # DEVELOPER
    # =====================================================

    if data == "developer":

        text = (
            "👨‍💻 Developer\n\n"
            f"Name: {DEVELOPER_NAME}\n"
        )

        if DEVELOPER_USERNAME:
            text += (
                f"Telegram: {DEVELOPER_USERNAME}\n"
            )

        if DEVELOPER_CHANNEL:
            text += (
                f"Channel: {DEVELOPER_CHANNEL}\n"
            )

        await query.edit_message_text(
            text,
            reply_markup=developer_menu(
                DEVELOPER_USERNAME,
                DEVELOPER_CHANNEL,
            ),
        )

        return

    # =====================================================
    # HELP
    # =====================================================

    if data == "help":

        help_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data="home"
                )
            ]
        ])

        await query.edit_message_text(
            "ℹ️ Help\n\n"
            "🤖 এই bot দিয়ে বিভিন্ন ধরনের file "
            "processing করা যাবে।\n\n"
            "📄 PDF Tools\n"
            "• Text → PDF\n"
            "• Image → PDF\n"
            "• Merge PDF\n"
            "• Split PDF\n"
            "• PDF → Text\n"
            "• Protect PDF\n\n"
            "🖼️ Image Tools\n"
            "• Resize\n"
            "• Compress\n"
            "• Convert\n\n"
            "🔳 QR Tools\n"
            "• QR Generator\n"
            "• QR Scanner\n\n"
            "🎙️ Audio Tools\n"
            "• Text → Voice\n"
            "• Voice Changer\n"
            "• Audio Converter\n\n"
            "⚠️ কিছু feature এখনো development-এ আছে।",
            reply_markup=help_keyboard,
        )

        return

    # =====================================================
    # ADMIN FEATURES
    # =====================================================

    admin_features = {
        "admin_stats": "📊 Statistics",
        "admin_users": "👥 Users",
        "admin_broadcast": "📢 Broadcast",
        "admin_ban": "🚫 Ban User",
        "admin_unban": "✅ Unban User",
        "admin_maintenance": "🔧 Maintenance",
    }

    if data in admin_features:

        if not update.effective_user:
            return

        if update.effective_user.id != ADMIN_ID:
            await query.edit_message_text(
                "❌ Unauthorized."
            )
            return

        await query.edit_message_text(
            f"{admin_features[data]}\n\n"
            "🔨 এই admin feature পরবর্তী ধাপে "
            "database-এর সাথে connect করা হবে।",
            reply_markup=admin_menu(),
        )

        return

    # =====================================================
    # FUTURE FEATURES
    # =====================================================

    future_features = {

        # Image
        "resize_image": "📐 Resize Image",
        "compress_image": "🗜️ Compress Image",
        "convert_image": "🔄 Convert Image",
        "image_info": "ℹ️ Image Info",

        # QR
        "qr_text": "📝 Text → QR",
        "qr_url": "🌐 URL → QR",
        "qr_wifi": "📶 Wi-Fi → QR",
        "qr_contact": "👤 Contact → QR",
        "qr_email": "📧 Email → QR",
        "qr_phone": "📱 Phone → QR",
        "qr_scan": "🔍 Scan QR",
        "qr_to_pdf": "📄 QR → PDF",

        # Audio
        "text_to_voice": "🗣️ Text → Voice",
        "voice_changer": "🎭 Voice Changer",
        "audio_cutter": "✂️ Audio Cutter",
        "audio_converter": "🔄 Audio Converter",
        "volume_changer": "🔊 Volume Changer",
        "audio_info": "ℹ️ Audio Info",

        # Files
        "create_zip": "🗜️ Create ZIP",
        "extract_zip": "📦 Extract ZIP",
        "file_converter": "🔄 File Converter",
        "file_info": "ℹ️ File Info",
    }

    if data in future_features:

        back_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data="home"
                )
            ]
        ])

        await query.edit_message_text(
            f"{future_features[data]}\n\n"
            "🔨 এই feature-এর processing module "
            "এখনো connect করা হয়নি।\n\n"
            "পরবর্তী ধাপে এটি তৈরি করা হবে।",
            reply_markup=back_keyboard,
        )

        return


# =========================================================
# TEXT MESSAGE HANDLER
# =========================================================

async def text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not update.message:
        return

    # Text → PDF
    if context.user_data.get("pdf_action") == "text_to_pdf":

        await handle_pdf_text(
            update,
            context
        )

        return

    # Protect PDF password
    if context.user_data.get("protect_pdf_path"):

        await handle_protect_password(
            update,
            context
        )

        return


# =========================================================
# PHOTO HANDLER
# =========================================================

async def photo_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not update.message:
        return

    if context.user_data.get("pdf_action") == "image_to_pdf":

        await handle_image(
            update,
            context
        )

        return


# =========================================================
# DOCUMENT HANDLER
# =========================================================

async def document_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not update.message:
        return

    await handle_pdf_document(
        update,
        context
    )


# =========================================================
# DONE COMMAND
# =========================================================

async def done_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await done_pdf(
        update,
        context
    )


# =========================================================
# CANCEL COMMAND
# =========================================================

async def cancel_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    context.user_data.clear()

    await update.message.reply_text(
        "❌ Current task cancel করা হয়েছে।",
        reply_markup=main_menu(),
    )


# =========================================================
# ERROR HANDLER
# =========================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):
    logger.error(
        "Exception while handling update:",
        exc_info=context.error,
    )


# =========================================================
# MAIN
# =========================================================

def main():

    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable পাওয়া যায়নি।"
        )

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # -----------------------------------------------------
    # Commands
    # -----------------------------------------------------

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        CommandHandler(
            "admin",
            admin
        )
    )

    application.add_handler(
        CommandHandler(
            "done",
            done_command
        )
    )

    application.add_handler(
        CommandHandler(
            "cancel",
            cancel_command
        )
    )

    # -----------------------------------------------------
    # Buttons
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    # -----------------------------------------------------
    # Photos
    # -----------------------------------------------------

    application.add_handler(
        MessageHandler(
            filters.PHOTO,
            photo_handler
        )
    )

    # -----------------------------------------------------
    # Documents
    # -----------------------------------------------------

    application.add_handler(
        MessageHandler(
            filters.Document.ALL,
            document_handler
        )
    )

    # -----------------------------------------------------
    # Text
    # -----------------------------------------------------

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler
        )
    )

    # -----------------------------------------------------
    # Errors
    # -----------------------------------------------------

    application.add_error_handler(
        error_handler
    )

    logger.info(
        "🚀 Telegram bot started successfully."
    )

    # -----------------------------------------------------
    # Start polling
    # -----------------------------------------------------

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    main()
