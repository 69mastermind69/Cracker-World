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
    BOT_NAME,
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
    start_image_to_pdf,
    start_pdf_to_image,
    start_merge_pdf,
    start_split_pdf,
    start_pdf_to_text,
    start_protect_pdf,
    handle_pdf_text,
    handle_pdf_document,
    handle_pdf_to_image,
    handle_protect_password,
    done_pdf,
    handle_image as handle_pdf_image,
)

from handlers.image import (
    start_resize,
    start_compress,
    start_convert,
    start_image_to_pdf,
    start_image_info,
    handle_image_document,
)

from handlers.qr import (
    start_text_qr,
    start_url_qr,
    start_wifi_qr,
    start_contact_qr,
    start_email_qr,
    start_phone_qr,
    start_scan_qr,
    start_qr_to_pdf,
    handle_qr_text,
    handle_qr_photo,
)

from handlers.audio import (
    start_text_to_voice,
    start_voice_changer,
    start_audio_cutter,
    start_audio_converter,
    start_volume_changer,
    start_audio_info,
    handle_audio_file,
)

from services.file_service import (
    create_zip,
    extract_zip,
    get_file_info,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ============================================================
# START
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    context.user_data.clear()

    text = (
        f"🤖 <b>{BOT_NAME}</b>\n\n"
        "Welcome! 👋\n\n"
        "এক জায়গায় অনেকগুলো useful tools ব্যবহার করতে পারবে।\n\n"
        "নিচের menu থেকে একটি option select করো 👇"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=main_menu(),
    )


# ============================================================
# HOME
# ============================================================

async def show_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query:
        await query.answer()

        context.user_data.clear()

        await query.edit_message_text(
            f"🤖 <b>{BOT_NAME}</b>\n\n"
            "Choose a tool from the menu 👇",
            parse_mode="HTML",
            reply_markup=main_menu(),
        )

    elif update.message:
        context.user_data.clear()

        await update.message.reply_text(
            f"🤖 <b>{BOT_NAME}</b>\n\n"
            "Choose a tool from the menu 👇",
            parse_mode="HTML",
            reply_markup=main_menu(),
        )


# ============================================================
# MAINTENANCE
# ============================================================

async def maintenance_check(update: Update) -> bool:
    if not MAINTENANCE_MODE:
        return False

    user = update.effective_user

    if user and user.id == ADMIN_ID:
        return False

    message = (
        "🔧 <b>Maintenance Mode</b>\n\n"
        "Bot বর্তমানে maintenance mode-এ আছে।\n"
        "কিছুক্ষণ পরে আবার চেষ্টা করো।"
    )

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            message,
            parse_mode="HTML",
        )

    elif update.message:
        await update.message.reply_text(
            message,
            parse_mode="HTML",
        )

    return True


# ============================================================
# CALLBACK HANDLER
# ============================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query

    if not query:
        return

    data = query.data

    if await maintenance_check(update):
        return

    # --------------------------------------------------------
    # HOME
    # --------------------------------------------------------

    if data == "home":
        await show_home(update, context)
        return

    # --------------------------------------------------------
    # PDF MENU
    # --------------------------------------------------------

    if data == "pdf_tools":
        await query.answer()

        await query.edit_message_text(
            "📄 <b>PDF Tools</b>\n\n"
            "একটি PDF tool select করো 👇",
            parse_mode="HTML",
            reply_markup=pdf_menu(),
        )
        return

    if data == "text_to_pdf":
        await start_text_to_pdf(update, context)
        return

    if data == "image_to_pdf":
        await start_image_to_pdf(update, context)
        return

    if data == "pdf_to_image":
        await start_pdf_to_image(update, context)
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

    # --------------------------------------------------------
    # IMAGE MENU
    # --------------------------------------------------------

    if data == "image_tools":
        await query.answer()

        await query.edit_message_text(
            "🖼️ <b>Image Tools</b>\n\n"
            "একটি image tool select করো 👇",
            parse_mode="HTML",
            reply_markup=image_menu(),
        )
        return

    if data == "resize_image":
        await start_resize(update, context)
        return

    if data == "compress_image":
        await start_compress(update, context)
        return

    if data == "convert_image":
        await start_convert(update, context)
        return

    if data == "image_to_pdf_tool":
        await start_image_to_pdf(update, context)
        return

    if data == "image_info":
        await start_image_info(update, context)
        return

    # --------------------------------------------------------
    # QR MENU
    # --------------------------------------------------------

    if data == "qr_tools":
        await query.answer()

        await query.edit_message_text(
            "🔳 <b>QR Tools</b>\n\n"
            "একটি QR tool select করো 👇",
            parse_mode="HTML",
            reply_markup=qr_menu(),
        )
        return

    if data == "text_to_qr":
        await start_text_qr(update, context)
        return

    if data == "url_to_qr":
        await start_url_qr(update, context)
        return

    if data == "wifi_to_qr":
        await start_wifi_qr(update, context)
        return

    if data == "contact_to_qr":
        await start_contact_qr(update, context)
        return

    if data == "email_to_qr":
        await start_email_qr(update, context)
        return

    if data == "phone_to_qr":
        await start_phone_qr(update, context)
        return

    if data == "scan_qr":
        await start_scan_qr(update, context)
        return

    if data == "qr_to_pdf":
        await start_qr_to_pdf(update, context)
        return

    # --------------------------------------------------------
    # AUDIO MENU
    # --------------------------------------------------------

    if data == "audio_tools":
        await query.answer()

        await query.edit_message_text(
            "🎙️ <b>Audio Tools</b>\n\n"
            "একটি audio tool select করো 👇",
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

    # --------------------------------------------------------
    # FILE MENU
    # --------------------------------------------------------

    if data == "file_tools":
        await query.answer()

        await query.edit_message_text(
            "🛠️ <b>File Tools</b>\n\n"
            "একটি file tool select করো 👇",
            parse_mode="HTML",
            reply_markup=file_menu(),
        )
        return

    # --------------------------------------------------------
    # FILE FEATURES
    # --------------------------------------------------------

    if data == "create_zip":
        context.user_data["file_action"] = "create_zip"

        await query.answer()

        await query.edit_message_text(
            "🗜️ <b>Create ZIP</b>\n\n"
            "যে files গুলো ZIP করতে চাও সেগুলো একে একে send করো।\n\n"
            "সবশেষে /done লিখো।",
            parse_mode="HTML",
        )
        return

    if data == "extract_zip":
        context.user_data["file_action"] = "extract_zip"

        await query.answer()

        await query.edit_message_text(
            "📦 <b>Extract ZIP</b>\n\n"
            "একটি ZIP file send করো।",
            parse_mode="HTML",
        )
        return

    if data == "file_converter":
        context.user_data["file_action"] = "file_converter"

        await query.answer()

        await query.edit_message_text(
            "🔄 <b>File Converter</b>\n\n"
            "এই feature বর্তমানে inactive।",
            parse_mode="HTML",
        )
        return

    if data == "file_info":
        context.user_data["file_action"] = "file_info"

        await query.answer()

        await query.edit_message_text(
            "ℹ️ <b>File Info</b>\n\n"
            "একটি file send করো।",
            parse_mode="HTML",
        )
        return

    # --------------------------------------------------------
    # DEVELOPER
    # --------------------------------------------------------

    if data == "developer":
        await query.answer()

        developer_text = (
            "👨‍💻 <b>Developer</b>\n\n"
            f"Name: <b>{DEVELOPER_NAME}</b>\n"
            f"Telegram: <b>{DEVELOPER_USERNAME}</b>\n\n"
            "Thanks for using the bot ❤️"
        )

        await query.edit_message_text(
            developer_text,
            parse_mode="HTML",
            reply_markup=developer_menu(
                DEVELOPER_USERNAME
            ),
        )
        return

    # --------------------------------------------------------
    # HELP
    # --------------------------------------------------------

    if data == "help":
        await query.answer()

        help_text = (
            "ℹ️ <b>Help</b>\n\n"
            "📄 PDF Tools\n"
            "• Text → PDF\n"
            "• Image → PDF\n"
            "• PDF → Image\n"
            "• Merge PDF\n"
            "• Split PDF\n"
            "• PDF → Text\n"
            "• Protect PDF\n\n"
            "🖼️ Image Tools\n"
            "• Resize\n"
            "• Compress\n"
            "• Convert\n"
            "• Image → PDF\n"
            "• Image Info\n\n"
            "🔳 QR Tools\n"
            "• Text → QR\n"
            "• URL → QR\n"
            "• Wi-Fi → QR\n"
            "• Contact → QR\n"
            "• Email → QR\n"
            "• Phone → QR\n"
            "• Scan QR\n"
            "• QR → PDF\n\n"
            "🎙️ Audio Tools\n"
            "• Text → Voice\n"
            "• Voice Changer\n"
            "• Audio Cutter\n"
            "• Audio Converter\n"
            "• Volume Changer\n"
            "• Audio Info\n\n"
            "🛠️ File Tools\n"
            "• Create ZIP\n"
            "• Extract ZIP\n"
            "• File Info"
        )

        await query.edit_message_text(
            help_text,
            parse_mode="HTML",
            reply_markup=help_menu(),
        )
        return

    # --------------------------------------------------------
    # ADMIN
    # --------------------------------------------------------

    if data == "admin":
        user = update.effective_user

        if not user or user.id != ADMIN_ID:
            await query.answer(
                "⛔ Admin only.",
                show_alert=True,
            )
            return

        await query.answer()

        await query.edit_message_text(
            "🛡️ <b>Admin Panel</b>\n\n"
            "এই admin feature এখনো active নয়।",
            parse_mode="HTML",
            reply_markup=admin_menu(),
        )
        return

    # --------------------------------------------------------
    # ADMIN PLACEHOLDERS
    # --------------------------------------------------------

    admin_features = {
        "statistics": "📊 Statistics",
        "users": "👥 Users",
        "broadcast": "📢 Broadcast",
        "ban": "🚫 Ban",
        "unban": "✅ Unban",
        "maintenance": "🔧 Maintenance",
    }

    if data in admin_features:
        user = update.effective_user

        if not user or user.id != ADMIN_ID:
            await query.answer(
                "⛔ Admin only.",
                show_alert=True,
            )
            return

        await query.answer()

        await query.edit_message_text(
            f"{admin_features[data]}\n\n"
            "এই feature বর্তমানে inactive।",
            parse_mode="HTML",
            reply_markup=admin_menu(),
        )
        return

    # --------------------------------------------------------
    # UNKNOWN CALLBACK
    # --------------------------------------------------------

    await query.answer(
        "Unknown option.",
        show_alert=True,
    )


# ============================================================
# TEXT HANDLER
# ============================================================

async def text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    if await maintenance_check(update):
        return

    text = update.message.text or ""

    # --------------------------------------------------------
    # PDF TEXT
    # --------------------------------------------------------

    if context.user_data.get("pdf_action") == "text_to_pdf":
        await handle_pdf_text(update, context)
        return

    # --------------------------------------------------------
    # PDF PASSWORD
    # --------------------------------------------------------

    if context.user_data.get("pdf_action") == "protect_pdf":
        if context.user_data.get("waiting_password"):
            await handle_protect_password(update, context)
            return

    # --------------------------------------------------------
    # IMAGE
    # --------------------------------------------------------

    if context.user_data.get("image_action"):
        action = context.user_data.get("image_action")

        if action in (
            "resize",
            "compress",
            "convert",
            "image_info",
        ):
            await handle_image_document(
                update,
                context,
            )
            return

    # --------------------------------------------------------
    # AUDIO TEXT
    # --------------------------------------------------------

    if context.user_data.get("audio_action") == "text_to_voice":
        from handlers.audio import handle_text_to_voice

        await handle_text_to_voice(
            update,
            context,
        )
        return

    # --------------------------------------------------------
    # QR TEXT
    # --------------------------------------------------------

    if context.user_data.get("qr_action"):
        await handle_qr_text(
            update,
            context,
        )
        return

    # --------------------------------------------------------
    # DEFAULT
    # --------------------------------------------------------

    await update.message.reply_text(
        "🤖 Menu থেকে একটি tool select করো।",
        reply_markup=main_menu(),
    )


# ============================================================
# PHOTO HANDLER
# ============================================================

async def photo_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    if await maintenance_check(update):
        return

    # --------------------------------------------------------
    # QR SCANNER / QR PDF
    # --------------------------------------------------------

    if context.user_data.get("qr_action") in (
        "scan_qr",
        "qr_to_pdf",
    ):
        await handle_qr_photo(
            update,
            context,
        )
        return

    # --------------------------------------------------------
    # IMAGE TOOLS
    # --------------------------------------------------------

    if context.user_data.get("image_action"):
        await handle_image_document(
            update,
            context,
        )
        return

    # --------------------------------------------------------
    # IMAGE TO PDF
    # --------------------------------------------------------

    if context.user_data.get("pdf_action") == "image_to_pdf":
        await handle_pdf_image(
            update,
            context,
        )
        return

    await update.message.reply_text(
        "🖼️ Image received.\n"
        "আগে একটি image tool select করো।"
    )


# ============================================================
# DOCUMENT HANDLER
# ============================================================

async def document_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    if await maintenance_check(update):
        return

    # --------------------------------------------------------
    # PDF → IMAGE
    # --------------------------------------------------------

    if context.user_data.get(
        "pdf_action"
    ) == "pdf_to_image":
        await handle_pdf_to_image(
            update,
            context,
        )
        return

    # --------------------------------------------------------
    # PDF
    # --------------------------------------------------------

    if context.user_data.get(
        "pdf_action"
    ):
        await handle_pdf_document(
            update,
            context,
        )
        return

    # --------------------------------------------------------
    # AUDIO
    # --------------------------------------------------------

    if context.user_data.get(
        "audio_action"
    ):
        await handle_audio_file(
            update,
            context,
        )
        return

    # --------------------------------------------------------
    # FILE
    # --------------------------------------------------------

    if context.user_data.get(
        "file_action"
    ):
        action = context.user_data.get(
            "file_action"
        )

        try:
            telegram_file = await update.message.document.get_file()

            file_name = (
                update.message.document.file_name
                or "file"
            )

            file_size = (
                update.message.document.file_size
                or 0
            )

            if action == "file_info":
                await update.message.reply_text(
                    "ℹ️ <b>File Info</b>\n\n"
                    f"Name: <code>{file_name}</code>\n"
                    f"Size: {file_size} bytes\n"
                    f"Type: {update.message.document.mime_type or 'Unknown'}",
                    parse_mode="HTML",
                )
                return

            if action == "extract_zip":
                import tempfile
                import os

                temp_dir = tempfile.mkdtemp(
                    prefix="zip_",
                    dir="/tmp",
                )

                zip_path = os.path.join(
                    temp_dir,
                    file_name,
                )

                await telegram_file.download_to_drive(
                    zip_path
                )

                output_dir = extract_zip(
                    zip_path,
                    temp_dir,
                )

                files = []

                for root, _, names in os.walk(
                    output_dir
                ):
                    for name in names:
                        files.append(
                            os.path.join(root, name)
                        )

                if not files:
                    await update.message.reply_text(
                        "❌ ZIP file-এর ভিতরে কোনো file পাওয়া যায়নি।"
                    )
                    return

                await update.message.reply_text(
                    f"📦 Extract complete.\n"
                    f"Files: {len(files)}"
                )

                for path in files:
                    try:
                        await update.message.reply_document(
                            document=open(path, "rb")
                        )
                    except Exception:
                        logger.exception(
                            "Failed sending extracted file"
                        )

                return

        except Exception:
            logger.exception(
                "File processing error"
            )

            await update.message.reply_text(
                "❌ File process করতে সমস্যা হয়েছে।"
            )

        return

    # --------------------------------------------------------
    # DEFAULT PDF FALLBACK
    # --------------------------------------------------------

    await handle_pdf_document(
        update,
        context,
    )


# ============================================================
# AUDIO HANDLER
# ============================================================

async def audio_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    if await maintenance_check(update):
        return

    if context.user_data.get(
        "audio_action"
    ):
        await handle_audio_file(
            update,
            context,
        )
        return

    await update.message.reply_text(
        "🎙️ আগে Audio Tools থেকে একটি option select করো।"
    )


# ============================================================
# VOICE HANDLER
# ============================================================

async def voice_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    if await maintenance_check(update):
        return

    if context.user_data.get(
        "audio_action"
    ):
        await handle_audio_file(
            update,
            context,
        )
        return

    await update.message.reply_text(
        "🎙️ আগে Audio Tools থেকে একটি option select করো।"
    )


# ============================================================
# VIDEO HANDLER
# ============================================================

async def video_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    await update.message.reply_text(
        "🎥 Video processing feature বর্তমানে available নয়।"
    )


# ============================================================
# DONE COMMAND
# ============================================================

async def done_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    if await maintenance_check(update):
        return

    # --------------------------------------------------------
    # PDF
    # --------------------------------------------------------

    if context.user_data.get(
        "pdf_action"
    ):
        await done_pdf(
            update,
            context,
        )
        return

    # --------------------------------------------------------
    # FILE ZIP
    # --------------------------------------------------------

    if context.user_data.get(
        "file_action"
    ) == "create_zip":

        files = context.user_data.get(
            "zip_files",
            [],
        )

        if not files:
            await update.message.reply_text(
                "❌ কোনো file পাওয়া যায়নি।"
            )
            return

        try:
            import tempfile
            import os

            temp_dir = tempfile.mkdtemp(
                prefix="zip_create_",
                dir="/tmp",
            )

            zip_path = os.path.join(
                temp_dir,
                "files.zip",
            )

            create_zip(
                files,
                zip_path,
            )

            with open(zip_path, "rb") as f:
                await update.message.reply_document(
                    document=f,
                    filename="files.zip",
                    caption="🗜️ ZIP তৈরি হয়েছে!",
                )

            context.user_data.pop(
                "zip_files",
                None,
            )

        except Exception:
            logger.exception(
                "ZIP creation failed"
            )

            await update.message.reply_text(
                "❌ ZIP তৈরি করতে সমস্যা হয়েছে।"
            )

        return

    await update.message.reply_text(
        "ℹ️ বর্তমানে কোনো active process নেই।"
    )


# ============================================================
# CANCEL
# ============================================================

async def cancel_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    context.user_data.clear()

    await update.message.reply_text(
        "❌ Process cancelled.",
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

    try:
        if isinstance(update, Update):

            if update.callback_query:
                await update.callback_query.answer(
                    "❌ Something went wrong.",
                    show_alert=True,
                )

            elif update.message:
                await update.message.reply_text(
                    "❌ Something went wrong.\n"
                    "Please try again."
                )

    except Exception:
        logger.exception(
            "Error while sending error message"
        )


# ============================================================
# MAIN
# ============================================================

def main():
    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN environment variable is missing."
        )

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # --------------------------------------------------------
    # COMMANDS
    # --------------------------------------------------------

    application.add_handler(
        CommandHandler(
            "start",
            start,
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
            "done",
            done_command,
        )
    )

    # --------------------------------------------------------
    # CALLBACK BUTTONS
    # --------------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    # --------------------------------------------------------
    # PHOTOS
    # --------------------------------------------------------

    application.add_handler(
        MessageHandler(
            filters.PHOTO,
            photo_handler,
        )
    )

    # --------------------------------------------------------
    # DOCUMENTS
    # --------------------------------------------------------

    application.add_handler(
        MessageHandler(
            filters.Document.ALL,
            document_handler,
        )
    )

    # --------------------------------------------------------
    # AUDIO
    # --------------------------------------------------------

    application.add_handler(
        MessageHandler(
            filters.AUDIO,
            audio_handler,
        )
    )

    # --------------------------------------------------------
    # VOICE
    # --------------------------------------------------------

    application.add_handler(
        MessageHandler(
            filters.VOICE,
            voice_handler,
        )
    )

    # --------------------------------------------------------
    # VIDEO
    # --------------------------------------------------------

    application.add_handler(
        MessageHandler(
            filters.VIDEO,
            video_handler,
        )
    )

    # --------------------------------------------------------
    # TEXT
    # --------------------------------------------------------

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler,
        )
    )

    # --------------------------------------------------------
    # ERROR
    # --------------------------------------------------------

    application.add_error_handler(
        error_handler
    )

    logger.info(
        "%s is starting...",
        BOT_NAME,
    )

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
