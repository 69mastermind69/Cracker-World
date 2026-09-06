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
)

from services.file_service import (
    create_zip,
    extract_zip,
)

from utils.files import (
    create_temp_dir,
    cleanup_temp_folder,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    context.user_data.clear()

    await update.message.reply_text(
        f"🤖 <b>{BOT_NAME}</b>\n\n"
        "Welcome! 👋\n\n"
        "নিচের menu থেকে একটি tool select করো 👇",
        parse_mode="HTML",
        reply_markup=main_menu(),
    )


async def maintenance_check(update: Update) -> bool:
    if not MAINTENANCE_MODE:
        return False

    user = update.effective_user

    if user and user.id == ADMIN_ID:
        return False

    text = (
        "🔧 <b>Maintenance Mode</b>\n\n"
        "Bot বর্তমানে maintenance mode-এ আছে।"
    )

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text,
            parse_mode="HTML",
        )
    elif update.message:
        await update.message.reply_text(
            text,
            parse_mode="HTML",
        )

    return True


async def show_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            f"🤖 <b>{BOT_NAME}</b>\n\n"
            "Choose a tool 👇",
            parse_mode="HTML",
            reply_markup=main_menu(),
        )

    elif update.message:
        await update.message.reply_text(
            f"🤖 <b>{BOT_NAME}</b>\n\n"
            "Choose a tool 👇",
            parse_mode="HTML",
            reply_markup=main_menu(),
        )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if not query:
        return

    data = query.data or ""

    if await maintenance_check(update):
        return

    if data == "home":
        await show_home(update, context)
        return

    # ---------------- PDF ----------------

    if data == "pdf_menu":
        await query.answer()
        await query.edit_message_text(
            "📄 <b>PDF Tools</b>\n\n"
            "একটি option select করো 👇",
            parse_mode="HTML",
            reply_markup=pdf_menu(),
        )
        return

    if data == "text_to_pdf":
        await start_text_to_pdf(update, context)
        return

    if data == "pdf_image_to_pdf":
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

    # ---------------- IMAGE ----------------

    if data == "image_menu":
        await query.answer()
        await query.edit_message_text(
            "🖼️ <b>Image Tools</b>\n\n"
            "একটি option select করো 👇",
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

    if data == "image_to_pdf":
        await start_image_to_pdf(update, context)
        return

    if data == "image_info":
        await start_image_info(update, context)
        return

    if data.startswith("convert_"):
        fmt = data.replace("convert_", "")
        await handle_convert_format(update, context, fmt)
        return

    # ---------------- QR ----------------

    if data == "qr_menu":
        await query.answer()
        await query.edit_message_text(
            "🔳 <b>QR Tools</b>\n\n"
            "একটি option select করো 👇",
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

    # ---------------- AUDIO ----------------

    if data == "audio_menu":
        await query.answer()
        await query.edit_message_text(
            "🎙️ <b>Audio Tools</b>\n\n"
            "একটি option select করো 👇",
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

    if data.startswith("audio_") and data in {
        "audio_mp3",
        "audio_wav",
        "audio_ogg",
        "audio_flac",
    }:
        fmt = data.replace("audio_", "")
        await handle_audio_format(update, context, fmt)
        return

    # ---------------- FILE ----------------

    if data == "file_menu":
        await query.answer()
        await query.edit_message_text(
            "🛠️ <b>File Tools</b>\n\n"
            "একটি option select করো 👇",
            parse_mode="HTML",
            reply_markup=file_menu(),
        )
        return

    if data == "create_zip":
        context.user_data.clear()
        context.user_data["file_action"] = "create_zip"
        context.user_data["zip_files"] = []

        await query.answer()
        await query.edit_message_text(
            "🗜️ <b>Create ZIP</b>\n\n"
            "যে files ZIP করতে চাও সেগুলো একে একে পাঠাও।\n\n"
            "সবশেষে /done লিখো।",
            parse_mode="HTML",
        )
        return

    if data == "extract_zip":
        context.user_data.clear()
        context.user_data["file_action"] = "extract_zip"

        await query.answer()
        await query.edit_message_text(
            "📦 <b>Extract ZIP</b>\n\n"
            "একটি ZIP file পাঠাও।",
            parse_mode="HTML",
        )
        return

    if data == "file_info":
        context.user_data.clear()
        context.user_data["file_action"] = "file_info"

        await query.answer()
        await query.edit_message_text(
            "ℹ️ <b>File Info</b>\n\n"
            "একটি file পাঠাও।",
            parse_mode="HTML",
        )
        return

    if data == "file_converter":
        await query.answer(
            "File Converter এখনো active নয়।",
            show_alert=True,
        )
        return

    # ---------------- DEVELOPER ----------------

    if data == "developer":
        await query.answer()

        await query.edit_message_text(
            "👨‍💻 <b>Developer</b>\n\n"
            f"Name: <b>{DEVELOPER_NAME}</b>\n"
            f"Telegram: <b>{DEVELOPER_USERNAME}</b>\n\n"
            "Thanks for using the bot ❤️",
            parse_mode="HTML",
            reply_markup=developer_menu(DEVELOPER_USERNAME),
        )
        return

    # ---------------- HELP ----------------

    if data == "help":
        await query.answer()

        await query.edit_message_text(
            "ℹ️ <b>Help</b>\n\n"
            "📄 PDF Tools\n"
            "• Text → PDF\n"
            "• Image → PDF\n"
            "• Merge / Split PDF\n"
            "• PDF → Image / Text\n"
            "• Protect PDF\n\n"
            "🖼️ Image Tools\n"
            "• Resize / Compress\n"
            "• Convert\n"
            "• Image → PDF\n"
            "• Image Info\n\n"
            "🔳 QR Tools\n"
            "• Text / URL / Wi-Fi\n"
            "• Contact / Email / Phone\n"
            "• Scan QR\n"
            "• QR → PDF\n\n"
            "🎙️ Audio Tools\n"
            "• Text → Voice\n"
            "• Voice processing\n"
            "• Cutter / Converter\n"
            "• Volume / Info\n\n"
            "🛠️ File Tools\n"
            "• Create ZIP\n"
            "• Extract ZIP\n"
            "• File Info",
            parse_mode="HTML",
            reply_markup=help_menu(),
        )
        return

    # ---------------- ADMIN ----------------

    if data.startswith("admin_"):
        user = update.effective_user

        if not user or user.id != ADMIN_ID:
            await query.answer(
                "⛔ Admin only.",
                show_alert=True,
            )
            return

        await query.answer(
            "এই admin feature এখনো active নয়।",
            show_alert=True,
        )
        return

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
            "Admin tools এখানে থাকবে।",
            parse_mode="HTML",
            reply_markup=admin_menu(),
        )
        return

    await query.answer(
        "Unknown option.",
        show_alert=True,
    )


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    if await maintenance_check(update):
        return

    if context.user_data.get("pdf_action") == "text_to_pdf":
        await handle_pdf_text(update, context)
        return

    if (
        context.user_data.get("pdf_action") == "protect_pdf"
        and context.user_data.get("waiting_password")
    ):
        await handle_protect_password(update, context)
        return

    if context.user_data.get("image_waiting_dimensions"):
        await handle_image_text(update, context)
        return

    if context.user_data.get("audio_action") in {
        "text_to_voice",
        "audio_cutter_waiting",
        "volume_waiting",
    }:
        await handle_audio_text(update, context)
        return

    if context.user_data.get("qr_action"):
        await handle_qr_text(update, context)
        return

    if context.user_data.get("file_action") == "create_zip":
        await update.message.reply_text(
            "📎 File হিসেবে send করো।\nসবশেষে /done লিখো।"
        )
        return

    await update.message.reply_text(
        "🤖 Menu থেকে একটি tool select করো।",
        reply_markup=main_menu(),
    )


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    if await maintenance_check(update):
        return

    if context.user_data.get("qr_action") in {
        "qr_scan",
        "qr_to_pdf",
    }:
        await handle_qr_image(update, context)
        return

    if context.user_data.get("image_action"):
        await handle_image(update, context)
        return

    if context.user_data.get("pdf_action") == "image_to_pdf":
        await handle_pdf_image(update, context)
        return

    await update.message.reply_text(
        "🖼️ আগে একটি image tool select করো।"
    )


async def document_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    if await maintenance_check(update):
        return

    # PDF
    if context.user_data.get("pdf_action") == "pdf_to_image":
        await handle_pdf_to_image(update, context)
        return

    if context.user_data.get("pdf_action"):
        await handle_pdf_document(update, context)
        return

    # Audio sent as document
    if context.user_data.get("audio_action"):
        await handle_audio_file(update, context)
        return

    action = context.user_data.get("file_action")

    if action == "file_info":
        document = update.message.document

        await update.message.reply_text(
            "ℹ️ <b>File Info</b>\n\n"
            f"📄 Name: <code>{document.file_name or 'unknown'}</code>\n"
            f"💾 Size: {(document.file_size or 0) / 1024:.2f} KB\n"
            f"🗂️ MIME: {document.mime_type or 'unknown'}",
            parse_mode="HTML",
        )
        return

    if action == "extract_zip":
        document = update.message.document

        folder = create_temp_dir()
        zip_path = os.path.join(
            folder,
            document.file_name or "archive.zip",
        )

        try:
            telegram_file = await document.get_file()
            await telegram_file.download_to_drive(zip_path)

            extracted = extract_zip(
                zip_path,
                folder,
            )

            if not extracted:
                await update.message.reply_text(
                    "❌ ZIP-এর ভিতরে কোনো file পাওয়া যায়নি।"
                )
                return

            await update.message.reply_text(
                f"📦 Extract complete: {len(extracted)} file"
            )

            for path in extracted:
                with open(path, "rb") as file:
                    await update.message.reply_document(
                        document=file,
                        filename=os.path.basename(path),
                    )

        except Exception as error:
            await update.message.reply_text(
                f"❌ ZIP extract করা যায়নি:\n{error}"
            )

        finally:
            cleanup_temp_folder(folder)
            context.user_data.clear()

        return

    if action == "create_zip":
        document = update.message.document

        folder = context.user_data.get("zip_folder")

        if not folder:
            folder = create_temp_dir()
            context.user_data["zip_folder"] = folder

        filename = document.file_name or "file"

        path = os.path.join(
            folder,
            os.path.basename(filename),
        )

        try:
            telegram_file = await document.get_file()
            await telegram_file.download_to_drive(path)

            files = context.user_data.setdefault(
                "zip_files",
                [],
            )

            files.append(path)

            await update.message.reply_text(
                f"✅ {filename} added.\n"
                "আরও file পাঠাতে পারো।\n"
                "শেষ হলে /done লিখো।"
            )

        except Exception as error:
            await update.message.reply_text(
                f"❌ File save করা যায়নি:\n{error}"
            )

        return

    await update.message.reply_text(
        "📄 File received.\n"
        "Menu থেকে একটি file tool select করো।"
    )


async def audio_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    if await maintenance_check(update):
        return

    await handle_audio_file(update, context)


async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    if await maintenance_check(update):
        return

    await handle_audio_file(update, context)


async def video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "🎥 Video processing বর্তমানে available নয়।"
        )


async def done_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    if await maintenance_check(update):
        return

    if context.user_data.get("pdf_action"):
        await done_pdf(update, context)
        return

    if context.user_data.get("image_action") == "image_to_pdf":
        await done_image_to_pdf(update, context)
        return

    if context.user_data.get("file_action") == "create_zip":
        files = context.user_data.get("zip_files", [])

        if not files:
            await update.message.reply_text(
                "❌ কোনো file যোগ করা হয়নি।"
            )
            return

        folder = context.user_data.get("zip_folder")

        if not folder:
            await update.message.reply_text(
                "❌ ZIP folder পাওয়া যায়নি।"
            )
            return

        output = os.path.join(
            folder,
            "files.zip",
        )

        try:
            create_zip(files, output)

            with open(output, "rb") as file:
                await update.message.reply_document(
                    document=file,
                    filename="files.zip",
                    caption="🗜️ ZIP তৈরি হয়েছে!",
                )

        except Exception as error:
            await update.message.reply_text(
                f"❌ ZIP তৈরি করা যায়নি:\n{error}"
            )

        finally:
            cleanup_temp_folder(folder)
            context.user_data.clear()

        return

    await update.message.reply_text(
        "ℹ️ কোনো active process নেই।"
    )


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    context.user_data.clear()

    await update.message.reply_text(
        "❌ Process cancelled.",
        reply_markup=main_menu(),
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.exception(
        "Unhandled exception",
        exc_info=context.error,
    )

    try:
        if isinstance(update, Update) and update.message:
            await update.message.reply_text(
                "❌ Process করতে সমস্যা হয়েছে। আবার চেষ্টা করো।"
            )
    except Exception:
        logger.exception("Failed to send error message")


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

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("done", done_command)
    )

    application.add_handler(
        CommandHandler("cancel", cancel_command)
    )

    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    application.add_handler(
        MessageHandler(filters.PHOTO, photo_handler)
    )

    application.add_handler(
        MessageHandler(filters.Document.ALL, document_handler)
    )

    application.add_handler(
        MessageHandler(filters.AUDIO, audio_handler)
    )

    application.add_handler(
        MessageHandler(filters.VOICE, voice_handler)
    )

    application.add_handler(
        MessageHandler(filters.VIDEO, video_handler)
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler,
        )
    )

    application.add_error_handler(error_handler)

    logger.info("%s starting...", BOT_NAME)

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
