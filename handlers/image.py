import os

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
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


# ============================================================
# IMAGE FORMAT KEYBOARD
# ============================================================

def image_format_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "JPG",
                callback_data="convert_jpg",
            ),
            InlineKeyboardButton(
                "PNG",
                callback_data="convert_png",
            ),
        ],
        [
            InlineKeyboardButton(
                "WEBP",
                callback_data="convert_webp",
            ),
            InlineKeyboardButton(
                "BMP",
                callback_data="convert_bmp",
            ),
        ],
        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="image_menu",
            ),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# ============================================================
# START RESIZE
# ============================================================

async def start_resize_image(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    context.user_data.clear()

    context.user_data["image_action"] = "resize"

    query = update.callback_query

    if query:
        await query.answer()

        await query.message.reply_text(
            "📐 <b>Resize Image</b>\n\n"
            "প্রথমে একটি image পাঠাও।",
            parse_mode="HTML",
        )


# ============================================================
# START COMPRESS
# ============================================================

async def start_compress_image(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    context.user_data.clear()

    context.user_data["image_action"] = "compress"

    query = update.callback_query

    if query:
        await query.answer()

        await query.message.reply_text(
            "🗜️ <b>Compress Image</b>\n\n"
            "প্রথমে একটি image পাঠাও।",
            parse_mode="HTML",
        )


# ============================================================
# START CONVERT
# ============================================================

async def start_convert_image(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    context.user_data.clear()

    context.user_data["image_action"] = "convert"

    query = update.callback_query

    if query:
        await query.answer()

        await query.message.reply_text(
            "🔄 <b>Convert Image</b>\n\n"
            "প্রথমে একটি image পাঠাও।\n\n"
            "তারপর কোন format-এ convert করতে চাও সেটা select করো।",
            parse_mode="HTML",
            reply_markup=image_format_keyboard(),
        )


# ============================================================
# START IMAGE INFO
# ============================================================

async def start_image_info(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    context.user_data.clear()

    context.user_data["image_action"] = "info"

    query = update.callback_query

    if query:
        await query.answer()

        await query.message.reply_text(
            "ℹ️ <b>Image Info</b>\n\n"
            "একটি image পাঠাও।",
            parse_mode="HTML",
        )


# ============================================================
# START IMAGE → PDF
# ============================================================

async def start_image_to_pdf(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    context.user_data.clear()

    folder = create_temp_dir()

    context.user_data["image_action"] = "image_to_pdf"
    context.user_data["image_pdf_folder"] = folder
    context.user_data["image_pdf_paths"] = []

    query = update.callback_query

    if query:
        await query.answer()

        await query.message.reply_text(
            "🖼️ <b>Image → PDF</b>\n\n"
            "এক বা একাধিক image পাঠাও।\n\n"
            "সব image পাঠানো শেষ হলে /done লিখো।",
            parse_mode="HTML",
        )


# ============================================================
# HANDLE IMAGE
# ============================================================

async def handle_image(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if not update.message:
        return

    if not update.message.photo:
        return

    action = context.user_data.get(
        "image_action"
    )

    if not action:
        return

    photo = update.message.photo[-1]

    # --------------------------------------------------------
    # IMAGE → PDF
    # --------------------------------------------------------

    if action == "image_to_pdf":

        folder = context.user_data.get(
            "image_pdf_folder"
        )

        image_paths = context.user_data.get(
            "image_pdf_paths",
            [],
        )

        if not folder:
            await update.message.reply_text(
                "❌ Temporary folder পাওয়া যায়নি। আবার শুরু করো।"
            )
            context.user_data.clear()
            return

        number = len(image_paths) + 1

        file_path = os.path.join(
            folder,
            f"image_{number}.jpg",
        )

        try:
            telegram_file = await photo.get_file()

            await telegram_file.download_to_drive(
                file_path
            )

            image_paths.append(file_path)

            context.user_data[
                "image_pdf_paths"
            ] = image_paths

            await update.message.reply_text(
                f"✅ Image {number} যোগ হয়েছে।\n\n"
                "আরও image পাঠাতে পারো।\n"
                "সব শেষ হলে /done লিখো।"
            )

        except Exception as error:

            await update.message.reply_text(
                "❌ Image save করা যায়নি:\n"
                f"{error}"
            )

        return

    # --------------------------------------------------------
    # OTHER IMAGE TOOLS
    # --------------------------------------------------------

    folder = create_temp_dir()

    input_path = os.path.join(
        folder,
        "input.jpg",
    )

    try:

        telegram_file = await photo.get_file()

        await telegram_file.download_to_drive(
            input_path
        )

        # ----------------------------------------------------
        # RESIZE
        # ----------------------------------------------------

        if action == "resize":

            context.user_data[
                "image_processing_folder"
            ] = folder

            context.user_data[
                "image_processing_input"
            ] = input_path

            context.user_data[
                "image_waiting_dimensions"
            ] = True

            await update.message.reply_text(
                "📐 <b>Image received!</b>\n\n"
                "এখন width এবং height পাঠাও।\n\n"
                "উদাহরণ:\n"
                "<code>800 600</code>",
                parse_mode="HTML",
            )

            return

        # ----------------------------------------------------
        # COMPRESS
        # ----------------------------------------------------

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

            with open(
                output_path,
                "rb",
            ) as image:

                await update.message.reply_document(
                    document=image,
                    filename="compressed.jpg",
                    caption="✅ Image compressed হয়েছে!",
                )

            return

        # ----------------------------------------------------
        # CONVERT
        # ----------------------------------------------------

        if action == "convert":

            context.user_data[
                "image_processing_folder"
            ] = folder

            context.user_data[
                "image_processing_input"
            ] = input_path

            await update.message.reply_text(
                "🔄 Image received!\n\n"
                "এখন output format select করো:",
                reply_markup=image_format_keyboard(),
            )

            return

        # ----------------------------------------------------
        # IMAGE INFO
        # ----------------------------------------------------

        if action == "info":

            info = get_image_info(
                input_path
            )

            text = (
                "ℹ️ <b>Image Information</b>\n\n"
                f"📄 Filename: <code>{info['filename']}</code>\n"
                f"📐 Size: {info['width']} × {info['height']}\n"
                f"🗂️ Format: {info['format']}\n"
                f"🎨 Mode: {info['mode']}\n"
                f"💾 File Size: {info['size_kb']} KB"
            )

            await update.message.reply_text(
                text,
                parse_mode="HTML",
            )

            return

    except Exception as error:

        await update.message.reply_text(
            "❌ Image process করা যায়নি:\n"
            f"{error}"
        )

        cleanup_temp_folder(folder)

        context.user_data.clear()


    # Resize/Convert-এর জন্য folder পরে ব্যবহার হবে।
    # অন্য action-এর folder এখানে cleanup করা যাবে।

    if action not in (
        "resize",
        "convert",
    ):
        cleanup_temp_folder(folder)


# ============================================================
# HANDLE IMAGE TEXT
# ============================================================

async def handle_image_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if not update.message:
        return

    if not context.user_data.get(
        "image_waiting_dimensions"
    ):
        return

    folder = context.user_data.get(
        "image_processing_folder"
    )

    input_path = context.user_data.get(
        "image_processing_input"
    )

    if not folder or not input_path:

        await update.message.reply_text(
            "❌ Resize process পাওয়া যায়নি। আবার চেষ্টা করো।"
        )

        context.user_data.clear()
        return

    text = update.message.text.strip()

    # Supports:
    # 800 600
    # 800x600
    # 800 X 600

    parts = (
        text.lower()
        .replace("×", " ")
        .replace("x", " ")
        .split()
    )

    if len(parts) != 2:

        await update.message.reply_text(
            "⚠️ সঠিক format-এ পাঠাও।\n\n"
            "উদাহরণ:\n"
            "<code>800 600</code>\n"
            "অথবা\n"
            "<code>800x600</code>",
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

        with open(
            output_path,
            "rb",
        ) as image:

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

        cleanup_temp_folder(
            folder
        )

        context.user_data.clear()


# ============================================================
# HANDLE CONVERT FORMAT
# ============================================================

async def handle_convert_format(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    output_format: str,
):

    query = update.callback_query

    # CallbackQuery থেকে function call হচ্ছে।
    # তাই update.message check করা যাবে না।
    if not query:
        return

    await query.answer()

    folder = context.user_data.get(
        "image_processing_folder"
    )

    input_path = context.user_data.get(
        "image_processing_input"
    )

    action = context.user_data.get(
        "image_action"
    )

    if action != "convert":

        await query.message.reply_text(
            "⚠️ আগে Image Tools → Convert ব্যবহার করো।"
        )

        return

    if not folder or not input_path:

        await query.message.reply_text(
            "⚠️ প্রথমে একটি image পাঠাও।"
        )

        return

    extension = output_format.lower()

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

        with open(
            output_path,
            "rb",
        ) as image:

            await query.message.reply_document(
                document=image,
                filename=f"converted.{extension}",
                caption=(
                    f"✅ Image → {output_format.upper()} "
                    "conversion হয়েছে!"
                ),
            )

    except Exception as error:

        await query.message.reply_text(
            "❌ Convert করা যায়নি:\n"
            f"{error}"
        )

    finally:

        cleanup_temp_folder(
            folder
        )

        context.user_data.clear()


# ============================================================
# DONE IMAGE → PDF
# ============================================================

async def done_image_to_pdf(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if not update.message:
        return False

    action = context.user_data.get(
        "image_action"
    )

    if action != "image_to_pdf":
        return False

    folder = context.user_data.get(
        "image_pdf_folder"
    )

    image_paths = context.user_data.get(
        "image_pdf_paths",
        [],
    )

    if not folder:

        await update.message.reply_text(
            "❌ Temporary folder পাওয়া যায়নি।"
        )

        context.user_data.clear()

        return True

    if not image_paths:

        await update.message.reply_text(
            "⚠️ কোনো image পাওয়া যায়নি।"
        )

        cleanup_temp_folder(folder)
        context.user_data.clear()

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

        with open(
            output_path,
            "rb",
        ) as pdf:

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

        cleanup_temp_folder(
            folder
        )

        context.user_data.clear()

    return True


# ============================================================
# COMPATIBILITY ALIASES
# ============================================================

# পুরোনো code কোথাও এই নাম ব্যবহার করলে যাতে crash না করে।
start_resize = start_resize_image
start_compress = start_compress_image
start_convert = start_convert_image
