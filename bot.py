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
    handle_image as handle_pdf_image,
)

from handlers.image import (
    start_resize_image,
    start_compress_image,
    start_convert_image,
    start_image_info,
    start_image_to_pdf as start_image_tools_pdf,
    handle_image as handle_image_tools,
    handle_image_text,
    handle_convert_format,
    done_image_to_pdf,
)

from handlers.qr import (
    start_qr_text,
    start_qr_url,
    start_qr_phone,
    start_qr_email,
    start_qr_wifi,
    start_qr_contact,
    start_qr_to_pdf,
    start_qr_scan,
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
)


logging.basicConfig(
    format=(
        "%(asctime)s - "
        "%(name)s - "
        "%(levelname)s - "
        "%(message)s"
    ),
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# =========================================================
# START
# =========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()

    await update.message.reply_text(
        "🤖 Welcome to All-in-One Bot!\n\n"
        "একটি feature নির্বাচন করো:",
        reply_markup=main_menu(),
    )


# =========================================================
# ADMIN
# =========================================================

async def admin(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
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
    context: ContextTypes.DEFAULT_TYPE,
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
            context,
        )
        return

    if data == "image_to_pdf":
        await start_image_tools_pdf(
            update,
            context,
        )
        return

    if data == "merge_pdf":
        await start_merge_pdf(
            update,
            context,
        )
        return

    if data == "split_pdf":
        await start_split_pdf(
            update,
            context,
        )
        return

    if data == "pdf_to_text":
        await start_pdf_to_text(
            update,
            context,
        )
        return

    if data == "protect_pdf":
        await start_protect_pdf(
            update,
            context,
        )
        return

    # =====================================================
    # IMAGE FEATURES
    # =====================================================

    if data == "resize_image":
        await start_resize_image(
            update,
            context,
        )
        return

    if data == "compress_image":
        await start_compress_image(
            update,
            context,
        )
        return

    if data == "convert_image":
        await start_convert_image(
            update,
            context,
        )
        return

    if data == "image_info":
        await start_image_info(
            update,
            context,
        )
        return

    # =====================================================
    # IMAGE CONVERSION
    # =====================================================

    if data == "convert_jpg":
        await handle_convert_format(
            update,
            context,
            "jpg",
        )
        return

    if data == "convert_png":
        await handle_convert_format(
            update,
            context,
            "png",
        )
        return

    if data == "convert_webp":
        await handle_convert_format(
            update,
            context,
            "webp",
        )
        return

    if data == "convert_bmp":
        await handle_convert_format(
            update,
            context,
            "bmp",
        )
        return

    # =====================================================
    # QR FEATURES
    # =====================================================

    if data == "qr_text":
        await start_qr_text(
            update,
            context,
        )
        return

    if data == "qr_url":
        await start_qr_url(
            update,
            context,
        )
        return

    if data == "qr_phone":
        await start_qr_phone(
            update,
            context,
        )
        return

    if data == "qr_email":
        await start_qr_email(
            update,
            context,
        )
        return

    if data == "qr_wifi":
        await start_qr_wifi(
            update,
            context,
        )
        return

    if data == "qr_contact":
        await start_qr_contact(
            update,
            context,
        )
        return

    if data == "qr_to_pdf":
        await start_qr_to_pdf(
            update,
            context,
        )
        return

    if data == "qr_scan":
        await start_qr_scan(
            update,
            context,
        )
        return

    # =====================================================
    # AUDIO FEATURES
    # =====================================================

    if data == "text_to_voice":
        await start_text_to_voice(
            update,
            context,
        )
        return

    if data == "voice_changer":
        await start_voice_changer(
            update,
            context,
        )
        return

    if data == "audio_cutter":
        await start_audio_cutter(
            update,
            context,
        )
        return

    if data == "audio_converter":
        await start_audio_converter(
            update,
            context,
        )
        return

    if data == "volume_changer":
        await start_volume_changer(
            update,
            context,
        )
        return

    if data == "audio_info":
        await start_audio_info(
            update,
            context,
        )
        return

    # =====================================================
    # AUDIO FORMAT
    # =====================================================

    if data == "audio_mp3":
        await handle_audio_format(
            update,
            context,
            "mp3",
        )
        return

    if data == "audio_wav":
        await handle_audio_format(
            update,
            context,
            "wav",
        )
        return

    if data == "audio_ogg":
        await handle_audio_format(
            update,
            context,
            "ogg",
        )
        return

    if data == "audio_flac":
        await handle_audio_format(
            update,
            context,
            "flac",
        )
        return

    # =====================================================
    # DEVELOPER
    # =====================================================

    if data == "developer":
        text = (
            "👨‍💻 Developer\n\n"
            f"Name: {DEVELOPER_NAME}\n"
            f"Telegram: {DEVELOPER_USERNAME}"
        )

        await query.edit_message_text(
            text,
            reply_markup=developer_menu(
                DEVELOPER_USERNAME,
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
                    callback_data="home",
                )
            ]
        ])

        await query.edit_message_text(
            "ℹ️ Help\n\n"

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
            "• Convert\n"
            "• Image Info\n"
            "• Image → PDF\n\n"

            "🔳 QR Tools\n"
            "• Text → QR\n"
            "• URL → QR\n"
            "• Wi-Fi → QR\n"
            "• Contact → QR\n"
            "• Email → QR\n"
            "• Phone → QR\n"
            "• QR → PDF\n"
            "• QR Scan\n\n"

            "🎙️ Audio Tools\n"
            "• Text → Voice\n"
            "• Voice Changer\n"
            "• Audio Cutter\n"
            "• Audio Converter\n"
            "• Volume Changer\n"
            "• Audio Info\n\n"

            "🛠️ File Tools\n"
            "• ZIP\n"
            "• Extract ZIP\n"
            "• File Converter\n"
            "• File Info\n\n"

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
        "pdf_to_image": "🖼️ PDF → Image",
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
                    callback_data="home",
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
# TEXT HANDLER
# =========================================================

async def text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    # PDF Text → PDF
    if context.user_data.get(
        "pdf_action"
    ) == "text_to_pdf":

        await handle_pdf_text(
            update,
            context,
        )
        return

    # PDF Password
    if context.user_data.get(
        "protect_pdf_path"
    ):

        await handle_protect_password(
            update,
            context,
        )
        return

    # Image Resize
    if context.user_data.get(
        "image_waiting_dimensions"
    ):

        await handle_image_text(
            update,
            context,
        )
        return

    # Audio text inputs
    if context.user_data.get(
        "audio_action"
    ):

        await handle_audio_text(
            update,
            context,
        )
        return

    # QR text inputs
    if context.user_data.get(
        "qr_action"
    ):

        await handle_qr_text(
            update,
            context,
        )
        return


# =========================================================
# PHOTO HANDLER
# =========================================================

async def photo_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    # QR Scan / QR → PDF
    if context.user_data.get(
        "qr_action"
    ) in (
        "qr_scan",
        "qr_to_pdf",
    ):

        await handle_qr_image(
            update,
            context,
        )
        return

    # Image Tools
    if context.user_data.get(
        "image_action"
    ):

        await handle_image_tools(
            update,
            context,
        )
        return

    # PDF Image → PDF
    if context.user_data.get(
        "pdf_action"
    ) == "image_to_pdf":

        await handle_pdf_image(
            update,
            context,
        )
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

    # Audio files
    if context.user_data.get(
        "audio_action"
    ):

        await handle_audio_file(
            update,
            context,
        )
        return

    # PDF files
    await handle_pdf_document(
        update,
        context,
    )


# =========================================================
# DONE COMMAND
# =========================================================

async def done_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    # Image → PDF
    if context.user_data.get(
        "image_action"
    ) == "image_to_pdf":

        handled = await done_image_to_pdf(
            update,
            context,
        )

        if handled:
            return

    # PDF tools
    await done_pdf(
        update,
        context,
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
        "❌ Current task cancel করা হয়েছে।",
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
        "Exception while handling update:",
        exc_info=context.error,
    )


# =========================================================
# MAIN
# =========================================================

def main():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable "
            "পাওয়া যায়নি।"
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
            "admin",
            admin,
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

    # Inline buttons
    application.add_handler(
        CallbackQueryHandler(
            button_handler,
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

    # Text
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler,
        )
    )

    # Error handler
    application.add_error_handler(
        error_handler
    )

    logger.info(
        "🚀 Telegram bot started successfully."
    )

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
