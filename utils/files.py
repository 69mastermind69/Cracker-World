import os

from telegram import Update
from telegram.ext import ContextTypes

from config import MAX_FILE_SIZE_MB
from services.file_service import (
    create_zip,
    extract_zip,
    get_file_info,
)
from utils.files import (
    create_temp_dir,
    cleanup_temp_folder,
)


def _too_large(size_bytes):
    return (
        size_bytes
        and size_bytes > MAX_FILE_SIZE_MB * 1024 * 1024
    )


async def start_create_zip(update, context):
    context.user_data.clear()

    folder = create_temp_dir()

    context.user_data["file_action"] = "create_zip"
    context.user_data["zip_folder"] = folder
    context.user_data["zip_files"] = []

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🗜️ <b>Create ZIP</b>\n\n"
        "যে files ZIP করতে চাও সেগুলো একে একে পাঠাও।\n\n"
        "শেষ হলে /done লিখো।",
        parse_mode="HTML",
    )


async def start_extract_zip(update, context):
    context.user_data.clear()

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "📦 <b>Extract ZIP</b>\n\n"
        "একটি ZIP file পাঠাও।",
        parse_mode="HTML",
    )

    context.user_data["file_action"] = "extract_zip"


async def start_file_info(update, context):
    context.user_data.clear()

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "ℹ️ <b>File Info</b>\n\n"
        "একটি file পাঠাও।",
        parse_mode="HTML",
    )

    context.user_data["file_action"] = "file_info"


async def start_file_converter(update, context):
    context.user_data.clear()

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🔄 <b>File Converter</b>\n\n"
        "এই feature এখনো active করা হয়নি।",
        parse_mode="HTML",
    )


async def handle_file_document(update, context):
    if not update.message:
        return

    document = update.message.document

    if not document:
        return

    data = context.user_data
    action = data.get("file_action")

    if action not in {
        "create_zip",
        "extract_zip",
        "file_info",
    }:
        return

    if _too_large(
        getattr(document, "file_size", 0)
    ):
        await update.message.reply_text(
            f"⚠️ File size "
            f"{MAX_FILE_SIZE_MB}MB-এর বেশি।"
        )
        return

    filename = os.path.basename(
        document.file_name or "file"
    )

    # -------------------------
    # CREATE ZIP
    # -------------------------
    if action == "create_zip":
        folder = data.get("zip_folder")

        if not folder:
            folder = create_temp_dir()
            data["zip_folder"] = folder

        try:
            input_path = os.path.join(
                folder,
                filename,
            )

            telegram_file = await document.get_file()

            await telegram_file.download_to_drive(
                input_path
            )

            files = data.setdefault(
                "zip_files",
                [],
            )

            files.append(input_path)

            count = len(files)

            await update.message.reply_text(
                f"✅ <code>{filename}</code> added.\n\n"
                f"📦 Total files: {count}\n\n"
                "আরও file পাঠাতে পারো।\n"
                "শেষ হলে /done লিখো।",
                parse_mode="HTML",
            )

        except Exception as error:
            await update.message.reply_text(
                f"❌ File save করা যায়নি:\n{error}"
            )

        return

    # -------------------------
    # EXTRACT ZIP
    # -------------------------
    if action == "extract_zip":
        if not filename.lower().endswith(".zip"):
            await update.message.reply_text(
                "⚠️ শুধু ZIP file পাঠাও।"
            )
            return

        folder = create_temp_dir()

        try:
            zip_path = os.path.join(
                folder,
                filename,
            )

            telegram_file = await document.get_file()

            await telegram_file.download_to_drive(
                zip_path
            )

            output_dir = os.path.join(
                folder,
                "extracted",
            )

            extracted_files = extract_zip(
                zip_path,
                output_dir,
            )

            if not extracted_files:
                await update.message.reply_text(
                    "⚠️ ZIP-এর মধ্যে কোনো file পাওয়া যায়নি।"
                )
                return

            await update.message.reply_text(
                f"📦 Extract complete!\n\n"
                f"📄 Files: {len(extracted_files)}"
            )

            for file_path in extracted_files:
                if not os.path.isfile(file_path):
                    continue

                try:
                    with open(
                        file_path,
                        "rb",
                    ) as file:
                        await update.message.reply_document(
                            document=file,
                            filename=os.path.basename(
                                file_path
                            ),
                        )
                except Exception as error:
                    await update.message.reply_text(
                        f"⚠️ {os.path.basename(file_path)} "
                        f"send করা যায়নি:\n{error}"
                    )

        except Exception as error:
            await update.message.reply_text(
                f"❌ ZIP extract করা যায়নি:\n{error}"
            )

        finally:
            cleanup_temp_folder(folder)
            data.clear()

        return

    # -------------------------
    # FILE INFO
    # -------------------------
    if action == "file_info":
        folder = create_temp_dir()

        try:
            input_path = os.path.join(
                folder,
                filename,
            )

            telegram_file = await document.get_file()

            await telegram_file.download_to_drive(
                input_path
            )

            info = get_file_info(
                input_path
            )

            await update.message.reply_text(
                "ℹ️ <b>File Info</b>\n\n"
                f"📄 Name: "
                f"<code>{info['filename']}</code>\n"
                f"🗂️ Extension: "
                f"<code>{info['extension'] or 'none'}</code>\n"
                f"💾 Size: "
                f"{info['size_kb']:.2f} KB\n"
                f"📦 Size: "
                f"{info['size_mb']:.2f} MB",
                parse_mode="HTML",
            )

        except Exception as error:
            await update.message.reply_text(
                f"❌ File info পাওয়া যায়নি:\n{error}"
            )

        finally:
            cleanup_temp_folder(folder)
            data.clear()

        return


async def done_create_zip(update, context):
    if not update.message:
        return False

    data = context.user_data

    if data.get("file_action") != "create_zip":
        return False

    files = data.get(
        "zip_files",
        [],
    )

    folder = data.get(
        "zip_folder"
    )

    if not files:
        await update.message.reply_text(
            "❌ কোনো file যোগ করা হয়নি।"
        )
        return True

    if not folder:
        await update.message.reply_text(
            "❌ Temporary folder পাওয়া যায়নি।"
        )
        data.clear()
        return True

    output_path = os.path.join(
        folder,
        "files.zip",
    )

    try:
        create_zip(
            files,
            output_path,
        )

        with open(
            output_path,
            "rb",
        ) as file:
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
        data.clear()

    return True
