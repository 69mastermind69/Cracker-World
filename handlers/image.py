import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from config import MAX_FILE_SIZE_MB
from services.image_service import (
    resize_image,
    compress_image,
    convert_image,
    get_image_info,
)
from services.pdf_service import images_to_pdf
from utils.files import create_temp_dir, cleanup_temp_folder


def format_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("JPG", callback_data="convert_jpg"),
            InlineKeyboardButton("PNG", callback_data="convert_png"),
        ],
        [
            InlineKeyboardButton("WEBP", callback_data="convert_webp"),
            InlineKeyboardButton("BMP", callback_data="convert_bmp"),
        ],
    ])


async def start_resize_image(update, context):
    context.user_data.clear()
    context.user_data["image_action"] = "resize"

    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "📐 <b>Resize Image</b>\n\n"
        "প্রথমে image পাঠাও।",
        parse_mode="HTML",
    )


start_resize = start_resize_image


async def start_compress_image(update, context):
    context.user_data.clear()
    context.user_data["image_action"] = "compress"

    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🗜️ <b>Compress Image</b>\n\n"
        "প্রথমে image পাঠাও।",
        parse_mode="HTML",
    )


start_compress = start_compress_image


async def start_convert_image(update, context):
    context.user_data.clear()
    context.user_data["image_action"] = "convert"

    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🔄 <b>Convert Image</b>\n\n"
        "প্রথমে image পাঠাও।",
        parse_mode="HTML",
    )


start_convert = start_convert_image


async def start_image_info(update, context):
    context.user_data.clear()
    context.user_data["image_action"] = "info"

    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "ℹ️ <b>Image Info</b>\n\n"
        "একটি image পাঠাও।",
        parse_mode="HTML",
    )


async def start_image_to_pdf(update, context):
    context.user_data.clear()

    folder = create_temp_dir()

    context.user_data["image_action"] = "image_to_pdf"
    context.user_data["image_pdf_folder"] = folder
    context.user_data["image_pdf_paths"] = []

    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🖼️ <b>Image → PDF</b>\n\n"
        "এক বা একাধিক image পাঠাও।\n\n"
        "সবশেষে /done লিখো।",
        parse_mode="HTML",
    )


start_image_info_tool = start_image_info
start_image_to_pdf_tool = start_image_to_pdf


async def handle_image(update, context):
    if not update.message or not update.message.photo:
        return

    data = context.user_data
    action = data.get("image_action")

    if not action:
        return

    photo = update.message.photo[-1]

    if getattr(photo, "file_size", 0) > MAX_FILE_SIZE_MB * 1024 * 1024:
        await update.message.reply_text(
            f"⚠️ Image size {MAX_FILE_SIZE_MB}MB-এর বেশি।"
        )
        return

    folder = create_temp_dir()

    try:
        input_path = os.path.join(folder, "input.jpg")

        telegram_file = await photo.get_file()
        await telegram_file.download_to_drive(input_path)

        if action == "resize":
            data["image_folder"] = folder
            data["image_input"] = input_path
            data["image_waiting_dimensions"] = True

            await update.message.reply_text(
                "📐 এখন width ও height পাঠাও।\n\n"
                "Example: <code>800 600</code>",
                parse_mode="HTML",
            )
            return

        if action == "compress":
            output_path = os.path.join(
                folder,
                "compressed.jpg",
            )

            compress_image(
                input_path,
                output_path,
                quality=70,
            )

            with open(output_path, "rb") as file:
                await update.message.reply_document(
                    document=file,
                    filename="compressed.jpg",
                    caption="🗜️ Image compressed!",
                )

            return

        if action == "convert":
            data["image_processing_folder"] = folder
            data["image_processing_input"] = input_path

            await update.message.reply_text(
                "🔄 কোন format-এ convert করতে চাও?",
                reply_markup=format_keyboard(),
            )
            return

        if action == "info":
            info = get_image_info(input_path)

            await update.message.reply_text(
                "ℹ️ <b>Image Info</b>\n\n"
                f"📄 Name: <code>{info['filename']}</code>\n"
                f"🗂️ Format: {info['format']}\n"
                f"📐 Size: {info['width']} × {info['height']}\n"
                f"🎨 Mode: {info['mode']}\n"
                f"💾 File Size: {info['size_kb']} KB",
                parse_mode="HTML",
            )

            return

        if action == "image_to_pdf":
            pdf_folder = data.get("image_pdf_folder")

            if not pdf_folder:
                pdf_folder = create_temp_dir()
                data["image_pdf_folder"] = pdf_folder

            image_path = os.path.join(
                pdf_folder,
                f"image_{len(data.get('image_pdf_paths', [])) + 1}.jpg",
            )

            telegram_file = await photo.get_file()
            await telegram_file.download_to_drive(image_path)

            data.setdefault(
                "image_pdf_paths",
                [],
            ).append(image_path)

            count = len(data["image_pdf_paths"])

            await update.message.reply_text(
                f"✅ Image {count} added.\n"
                "আরও image পাঠাতে পারো।\n"
                "শেষ হলে /done লিখো।"
            )

            cleanup_temp_folder(folder)
            return

    except Exception as error:
        await update.message.reply_text(
            f"❌ Image process করা যায়নি:\n{error}"
        )

    finally:
        if not data.get("image_waiting_dimensions") and not data.get(
            "image_processing_input"
        ):
            cleanup_temp_folder(folder)


async def handle_image_text(update, context):
    if not update.message:
        return

    data = context.user_data

    if not data.get("image_waiting_dimensions"):
        return

    parts = (update.message.text or "").split()

    if len(parts) != 2:
        await update.message.reply_text(
            "⚠️ এভাবে পাঠাও: <code>800 600</code>",
            parse_mode="HTML",
        )
        return

    try:
        width = int(parts[0])
        height = int(parts[1])

        if width <= 0 or height <= 0:
            raise ValueError

    except ValueError:
        await update.message.reply_text(
            "⚠️ Width ও height positive number হতে হবে।"
        )
        return

    folder = data.get("image_folder")
    input_path = data.get("image_input")

    if not folder or not input_path:
        await update.message.reply_text(
            "❌ Image process-এর data পাওয়া যায়নি।"
        )
        data.clear()
        return

    output_path = os.path.join(
        folder,
        "resized.jpg",
    )

    try:
        resize_image(
            input_path,
            output_path,
            width,
            height,
            keep_aspect=False,
        )

        with open(output_path, "rb") as file:
            await update.message.reply_document(
                document=file,
                filename="resized.jpg",
                caption=f"📐 Resized to {width} × {height}",
            )

    except Exception as error:
        await update.message.reply_text(
            f"❌ Resize করা যায়নি:\n{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        data.clear()


async def handle_convert_format(
    update,
    context,
    output_format,
):
    query = update.callback_query
    data = context.user_data

    if data.get("image_action") != "convert":
        await query.answer(
            "No active image conversion.",
            show_alert=True,
        )
        return

    folder = data.get(
        "image_processing_folder"
    )
    input_path = data.get(
        "image_processing_input"
    )

    if not folder or not input_path:
        await query.answer(
            "Image data পাওয়া যায়নি।",
            show_alert=True,
        )
        data.clear()
        return

    extension = "jpg" if output_format == "jpeg" else output_format

    output_path = os.path.join(
        folder,
        f"converted.{extension}",
    )

    try:
        convert_image(
            input_path,
            output_path,
            output_format,
        )

        await query.answer("Conversion complete!")

        with open(output_path, "rb") as file:
            await query.message.reply_document(
                document=file,
                filename=f"converted.{extension}",
                caption=f"🔄 Converted to {output_format.upper()}",
            )

    except Exception as error:
        await query.answer(
            "Conversion failed.",
            show_alert=True,
        )
        await query.message.reply_text(
            f"❌ Image convert করা যায়নি:\n{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        data.clear()


async def done_image_to_pdf(update, context):
    if not update.message:
        return

    data = context.user_data

    if data.get("image_action") != "image_to_pdf":
        return

    folder = data.get("image_pdf_folder")
    paths = data.get("image_pdf_paths", [])

    if not paths:
        await update.message.reply_text(
            "❌ কোনো image যোগ করা হয়নি।"
        )
        return

    if not folder:
        await update.message.reply_text(
            "❌ Temporary folder পাওয়া যায়নি।"
        )
        data.clear()
        return

    output_path = os.path.join(
        folder,
        "images.pdf",
    )

    try:
        images_to_pdf(
            paths,
            output_path,
        )

        with open(output_path, "rb") as file:
            await update.message.reply_document(
                document=file,
                filename="images.pdf",
                caption="📄 Image → PDF complete!",
            )

    except Exception as error:
        await update.message.reply_text(
            f"❌ PDF তৈরি করা যায়নি:\n{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        data.clear()
