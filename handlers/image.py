import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from services.image_service import (
    resize_image,
    compress_image,
    convert_image,
    get_image_info,
)
from services.pdf_service import images_to_pdf
from utils.files import create_temp_dir, cleanup_temp_folder


def image_format_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("JPG", callback_data="convert_jpg"),
            InlineKeyboardButton("PNG", callback_data="convert_png"),
        ],
        [
            InlineKeyboardButton("WEBP", callback_data="convert_webp"),
            InlineKeyboardButton("BMP", callback_data="convert_bmp"),
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="image_menu"),
        ],
    ])


async def start_resize(update, context):
    context.user_data.clear()
    context.user_data["image_action"] = "resize"

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "📐 <b>Resize Image</b>\n\n"
        "একটি image পাঠাও।",
        parse_mode="HTML",
    )


async def start_compress(update, context):
    context.user_data.clear()
    context.user_data["image_action"] = "compress"

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "🗜️ <b>Compress Image</b>\n\n"
        "একটি image পাঠাও।",
        parse_mode="HTML",
    )


async def start_convert(update, context):
    context.user_data.clear()
    context.user_data["image_action"] = "convert"

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "🔄 <b>Convert Image</b>\n\n"
        "প্রথমে একটি image পাঠাও।\n"
        "তারপর format select করতে পারবে।",
        parse_mode="HTML",
    )


async def start_image_info(update, context):
    context.user_data.clear()
    context.user_data["image_action"] = "info"

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
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

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "📄 <b>Image → PDF</b>\n\n"
        "এক বা একাধিক image পাঠাও।\n"
        "সব শেষ হলে /done লিখো।",
        parse_mode="HTML",
    )


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.photo:
        return

    action = context.user_data.get("image_action")
    if not action:
        return

    photo = update.message.photo[-1]

    # IMAGE → PDF
    if action == "image_to_pdf":
        folder = context.user_data.get("image_pdf_folder")

        if not folder:
            return

        paths = context.user_data.setdefault("image_pdf_paths", [])
        path = os.path.join(folder, f"image_{len(paths) + 1}.jpg")

        try:
            telegram_file = await photo.get_file()
            await telegram_file.download_to_drive(path)

            paths.append(path)

            await update.message.reply_text(
                f"✅ Image {len(paths)} যোগ হয়েছে।\n"
                "আরও image পাঠাতে পারো।\n"
                "সবশেষে /done লিখো।"
            )
        except Exception as error:
            await update.message.reply_text(
                f"❌ Image save করা যায়নি:\n{error}"
            )

        return

    folder = create_temp_dir()
    input_path = os.path.join(folder, "input.jpg")

    try:
        telegram_file = await photo.get_file()
        await telegram_file.download_to_drive(input_path)

        context.user_data["image_processing_folder"] = folder
        context.user_data["image_processing_input"] = input_path

        if action == "resize":
            context.user_data["image_waiting_dimensions"] = True

            await update.message.reply_text(
                "📐 Image received.\n\n"
                "Width এবং height পাঠাও।\n\n"
                "উদাহরণ: <code>800 600</code>",
                parse_mode="HTML",
            )
            return

        if action == "compress":
            output = os.path.join(folder, "compressed.jpg")

            compress_image(
                input_path,
                output,
                quality=70,
            )

            with open(output, "rb") as file:
                await update.message.reply_document(
                    document=file,
                    filename="compressed.jpg",
                    caption="✅ Image compressed হয়েছে!",
                )

            context.user_data.clear()
            cleanup_temp_folder(folder)
            return

        if action == "info":
            info = get_image_info(input_path)

            await update.message.reply_text(
                "ℹ️ <b>Image Information</b>\n\n"
                f"📄 Filename: <code>{info['filename']}</code>\n"
                f"📐 Size: {info['width']} × {info['height']}\n"
                f"🗂️ Format: {info['format']}\n"
                f"🎨 Mode: {info['mode']}\n"
                f"💾 Size: {info['size_kb']} KB",
                parse_mode="HTML",
            )

            context.user_data.clear()
            cleanup_temp_folder(folder)
            return

        if action == "convert":
            await update.message.reply_text(
                "🔄 Image received!\n\n"
                "এখন output format select করো:",
                reply_markup=image_format_keyboard(),
            )
            return

    except Exception as error:
        cleanup_temp_folder(folder)
        context.user_data.clear()

        await update.message.reply_text(
            f"❌ Image process করা যায়নি:\n{error}"
        )


async def handle_image_text(update, context):
    if not update.message:
        return

    if not context.user_data.get("image_waiting_dimensions"):
        return

    folder = context.user_data.get("image_processing_folder")
    input_path = context.user_data.get("image_processing_input")

    if not folder or not input_path:
        return

    parts = (
        update.message.text
        .strip()
        .lower()
        .replace("x", " ")
        .split()
    )

    if len(parts) != 2:
        await update.message.reply_text(
            "⚠️ Format ঠিক রাখো।\n\n"
            "উদাহরণ: 800 600"
        )
        return

    try:
        width = int(parts[0])
        height = int(parts[1])

        if width <= 0 or height <= 0:
            raise ValueError

        output = os.path.join(folder, "resized.jpg")

        resize_image(
            input_path,
            output,
            width,
            height,
            keep_aspect=False,
        )

        with open(output, "rb") as file:
            await update.message.reply_document(
                document=file,
                filename="resized.jpg",
                caption="✅ Image resize হয়েছে!",
            )

    except Exception as error:
        await update.message.reply_text(
            f"❌ Resize করা যায়নি:\n{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()


async def handle_convert_format(update, context, output_format):
    if not update.callback_query:
        return

    folder = context.user_data.get("image_processing_folder")
    input_path = context.user_data.get("image_processing_input")

    await update.callback_query.answer()

    if not folder or not input_path:
        await update.callback_query.message.reply_text(
            "⚠️ আগে একটি image পাঠাও।"
        )
        return

    extension = output_format.lower()
    output = os.path.join(folder, f"converted.{extension}")

    try:
        convert_image(
            input_path,
            output,
            extension,
        )

        with open(output, "rb") as file:
            await update.callback_query.message.reply_document(
                document=file,
                filename=f"converted.{extension}",
                caption=f"✅ Image → {extension.upper()} conversion হয়েছে!",
            )

    except Exception as error:
        await update.callback_query.message.reply_text(
            f"❌ Convert করা যায়নি:\n{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()


async def done_image_to_pdf(update, context):
    if not update.message:
        return False

    if context.user_data.get("image_action") != "image_to_pdf":
        return False

    folder = context.user_data.get("image_pdf_folder")
    paths = context.user_data.get("image_pdf_paths", [])

    if not folder:
        return True

    if not paths:
        await update.message.reply_text(
            "❌ অন্তত একটি image পাঠাতে হবে।"
        )
        return True

    output = os.path.join(folder, "images.pdf")

    try:
        images_to_pdf(paths, output)

        with open(output, "rb") as file:
            await update.message.reply_document(
                document=file,
                filename="images.pdf",
                caption="✅ Image → PDF complete!",
            )

    except Exception as error:
        await update.message.reply_text(
            f"❌ PDF তৈরি করা যায়নি:\n{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()

    return True


# Compatibility aliases
start_resize_image = start_resize
start_compress_image = start_compress
start_convert_image = start_convert
start_image_info = start_image_info
handle_image_document = handle_image
