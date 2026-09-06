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

from utils.files import (
    create_temp_dir,
    cleanup_temp_folder,
)


def image_format_keyboard():
    keyboard = [
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
    ]

    return InlineKeyboardMarkup(keyboard)


async def start_resize_image(update, context):
    context.user_data.clear()
    context.user_data["image_action"] = "resize"

    await update.callback_query.message.reply_text(
        "📐 Resize Image\n\n"
        "প্রথমে একটি image পাঠাও।"
    )


async def start_compress_image(update, context):
    context.user_data.clear()
    context.user_data["image_action"] = "compress"

    await update.callback_query.message.reply_text(
        "🗜️ Compress Image\n\n"
        "প্রথমে একটি image পাঠাও।"
    )


async def start_convert_image(update, context):
    context.user_data.clear()
    context.user_data["image_action"] = "convert"

    await update.callback_query.message.reply_text(
        "🔄 Convert Image\n\n"
        "কোন format-এ convert করতে চাও?",
        reply_markup=image_format_keyboard(),
    )


async def start_image_info(update, context):
    context.user_data.clear()
    context.user_data["image_action"] = "info"

    await update.callback_query.message.reply_text(
        "ℹ️ Image Info\n\n"
        "একটি image পাঠাও।"
    )


async def start_image_to_pdf(update, context):
    context.user_data.clear()

    folder = create_temp_dir()

    context.user_data["image_action"] = "image_to_pdf"
    context.user_data["image_pdf_folder"] = folder
    context.user_data["image_pdf_paths"] = []

    await update.callback_query.message.reply_text(
        "🖼️ Image → PDF\n\n"
        "এক বা একাধিক image পাঠাও।\n\n"
        "সব image পাঠানো শেষ হলে /done লিখো।"
    )


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    action = context.user_data.get("image_action")

    if not action:
        return

    if not update.message.photo:
        return

    photo = update.message.photo[-1]

    # Image → PDF
    if action == "image_to_pdf":
        folder = context.user_data.get("image_pdf_folder")
        image_paths = context.user_data.get("image_pdf_paths", [])

        if not folder:
            return

        number = len(image_paths) + 1

        file_path = os.path.join(
            folder,
            f"image_{number}.jpg",
        )

        try:
            telegram_file = await photo.get_file()
            await telegram_file.download_to_drive(file_path)

            image_paths.append(file_path)
            context.user_data["image_pdf_paths"] = image_paths

            await update.message.reply_text(
                f"✅ Image {number} যোগ হয়েছে.\n\n"
                "আরও image পাঠাতে পারো।\n"
                "সব শেষ হলে /done লিখো।"
            )

        except Exception as error:
            await update.message.reply_text(
                "❌ Image save করা যায়নি:\n"
                f"{error}"
            )

        return

    folder = create_temp_dir()

    input_path = os.path.join(
        folder,
        "input.jpg",
    )

    try:
        telegram_file = await photo.get_file()
        await telegram_file.download_to_drive(input_path)

        # Resize
        if action == "resize":
            context.user_data["image_processing_folder"] = folder
            context.user_data["image_processing_input"] = input_path
            context.user_data["image_waiting_dimensions"] = True

            await update.message.reply_text(
                "📐 Image পাওয়া গেছে!\n\n"
                "এখন width এবং height পাঠাও।\n\n"
                "উদাহরণ:\n"
                "800 600"
            )
            return

        # Compress
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

            with open(output_path, "rb") as image:
                await update.message.reply_document(
                    document=image,
                    filename="compressed.jpg",
                    caption="✅ Image compressed হয়েছে!",
                )

            context.user_data.clear()
            return

        # Convert
        if action == "convert":
            context.user_data["image_processing_folder"] = folder
            context.user_data["image_processing_input"] = input_path

            await update.message.reply_text(
                "🔄 এখন নিচের format থেকে একটি select করো:",
                reply_markup=image_format_keyboard(),
            )
            return

        # Image Info
        if action == "info":
            info = get_image_info(input_path)

            text = (
                "ℹ️ Image Information\n\n"
                f"📄 Filename: {info['filename']}\n"
                f"📐 Size: {info['width']} × {info['height']}\n"
                f"🗂️ Format: {info['format']}\n"
                f"🎨 Mode: {info['mode']}\n"
                f"💾 File Size: {info['size_kb']} KB"
            )

            await update.message.reply_text(text)
            context.user_data.clear()
            return

    except Exception as error:
        await update.message.reply_text(
            "❌ Image process করা যায়নি:\n"
            f"{error}"
        )

    finally:
        if action not in ("resize", "convert", "image_to_pdf"):
            cleanup_temp_folder(folder)


async def handle_image_text(update, context):
    if not update.message:
        return

    if not context.user_data.get("image_waiting_dimensions"):
        return

    folder = context.user_data.get("image_processing_folder")
    input_path = context.user_data.get("image_processing_input")

    if not folder or not input_path:
        return

    text = update.message.text.strip()

    parts = text.replace("x", " ").replace("X", " ").split()

    if len(parts) != 2:
        await update.message.reply_text(
            "⚠️ সঠিক format-এ পাঠাও।\n\n"
            "উদাহরণ:\n"
            "800 600"
        )
        return

    try:
        width = int(parts[0])
        height = int(parts[1])

        if width <= 0 or height <= 0:
            raise ValueError

    except ValueError:
        await update.message.reply_text(
            "⚠️ Width এবং height positive number হতে হবে।"
        )
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

        with open(output_path, "rb") as image:
            await update.message.reply_document(
                document=image,
                filename="resized.jpg",
                caption="✅ Image resize হয়েছে!",
            )

    except Exception as error:
        await update.message.reply_text(
            "❌ Resize করা যায়নি:\n"
            f"{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()


async def handle_convert_format(
    update,
    context,
    output_format,
):
    query = update.callback_query

    if query:
        await query.answer()

    folder = context.user_data.get("image_processing_folder")
    input_path = context.user_data.get("image_processing_input")

    if not folder or not input_path:
        if query:
            await query.message.reply_text(
                "⚠️ প্রথমে একটি image পাঠাও।"
            )
        return

    extension = output_format.lower().replace(".", "")

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

        target = query.message if query else update.message

        with open(output_path, "rb") as image:
            await target.reply_document(
                document=image,
                filename=f"converted.{extension}",
                caption=(
                    f"✅ Image → {output_format.upper()} "
                    "conversion হয়েছে!"
                ),
            )

    except Exception as error:
        target = query.message if query else update.message

        await target.reply_text(
            "❌ Convert করা যায়নি:\n"
            f"{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()


async def done_image_to_pdf(update, context):
    action = context.user_data.get("image_action")

    if action != "image_to_pdf":
        return False

    folder = context.user_data.get("image_pdf_folder")
    image_paths = context.user_data.get(
        "image_pdf_paths",
        [],
    )

    if not folder:
        return True

    if not image_paths:
        await update.message.reply_text(
            "⚠️ কোনো image পাওয়া যায়নি।"
        )
        return True

    output_path = os.path.join(
        folder,
        "images.pdf",
    )

    try:
        images_to_pdf(
            image_paths,
            output_path,
        )

        with open(output_path, "rb") as pdf:
            await update.message.reply_document(
                document=pdf,
                filename="images.pdf",
                caption="✅ Images থেকে PDF তৈরি হয়েছে!",
            )

    except Exception as error:
        await update.message.reply_text(
            "❌ Image → PDF করা যায়নি:\n"
            f"{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()

    return True


# Backward-compatible aliases
start_resize = start_resize_image
start_compress = start_compress_image
start_convert = start_convert_image
start_image_info_tool = start_image_info
start_image_to_pdf_tool = start_image_to_pdf
