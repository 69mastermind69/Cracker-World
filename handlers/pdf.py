import os

from telegram import Update
from telegram.ext import ContextTypes

from services.pdf_service import (
    text_to_pdf,
    images_to_pdf,
    merge_pdfs,
    split_pdf,
    pdf_to_text,
    protect_pdf,
    pdf_to_images,
)

from utils.files import (
    create_temp_dir,
    cleanup_temp_folder,
)


async def start_text_to_pdf(update, context):
    context.user_data.clear()
    context.user_data["pdf_action"] = "text_to_pdf"

    await update.callback_query.message.reply_text(
        "📝 Text → PDF\n\n"
        "যে text-টা PDF করতে চাও সেটা পাঠাও।"
    )


async def handle_pdf_text(update, context):
    if not update.message or not update.message.text:
        return

    if context.user_data.get("pdf_action") != "text_to_pdf":
        return

    text = update.message.text.strip()

    if not text:
        await update.message.reply_text(
            "⚠️ কিছু text পাঠাও।"
        )
        return

    folder = create_temp_dir()
    output_path = os.path.join(
        folder,
        "document.pdf",
    )

    try:
        text_to_pdf(
            text,
            output_path,
        )

        with open(output_path, "rb") as pdf:
            await update.message.reply_document(
                document=pdf,
                filename="document.pdf",
                caption="✅ Text → PDF complete!",
            )

    except Exception as error:
        await update.message.reply_text(
            "❌ PDF তৈরি করা যায়নি.\n\n"
            f"{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()


async def start_image_to_pdf(update, context):
    context.user_data.clear()

    folder = create_temp_dir()

    context.user_data["pdf_action"] = "image_to_pdf"
    context.user_data["pdf_image_folder"] = folder
    context.user_data["pdf_image_paths"] = []

    await update.callback_query.message.reply_text(
        "🖼️ Image → PDF\n\n"
        "এক বা একাধিক image পাঠাও।\n\n"
        "সব image পাঠানো শেষ হলে /done লিখো।"
    )


async def handle_image_to_pdf(update, context):
    if not update.message:
        return

    if context.user_data.get("pdf_action") != "image_to_pdf":
        return

    if not update.message.photo:
        return

    folder = context.user_data.get(
        "pdf_image_folder"
    )

    image_paths = context.user_data.get(
        "pdf_image_paths",
        [],
    )

    if not folder:
        return

    photo = update.message.photo[-1]

    number = len(image_paths) + 1

    image_path = os.path.join(
        folder,
        f"image_{number}.jpg",
    )

    try:
        telegram_file = await photo.get_file()

        await telegram_file.download_to_drive(
            image_path
        )

        image_paths.append(image_path)

        context.user_data["pdf_image_paths"] = (
            image_paths
        )

        await update.message.reply_text(
            f"✅ Image {number} যোগ হয়েছে।\n\n"
            "আরও image পাঠাতে পারো।\n"
            "সব শেষ হলে /done লিখো।"
        )

    except Exception as error:
        await update.message.reply_text(
            "❌ Image save করা যায়নি.\n\n"
            f"{error}"
        )


async def done_pdf(update, context):
    action = context.user_data.get(
        "pdf_action"
    )

    if action != "image_to_pdf":
        return False

    folder = context.user_data.get(
        "pdf_image_folder"
    )

    image_paths = context.user_data.get(
        "pdf_image_paths",
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
                caption="✅ Images → PDF complete!",
            )

    except Exception as error:
        await update.message.reply_text(
            "❌ PDF তৈরি করা যায়নি.\n\n"
            f"{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()

    return True


async def start_merge_pdf(update, context):
    context.user_data.clear()

    folder = create_temp_dir()

    context.user_data["pdf_action"] = "merge"
    context.user_data["merge_folder"] = folder
    context.user_data["merge_files"] = []

    await update.callback_query.message.reply_text(
        "📚 Merge PDF\n\n"
        "একাধিক PDF পাঠাও।\n\n"
        "সব পাঠানো শেষ হলে /done লিখো।"
    )


async def start_split_pdf(update, context):
    context.user_data.clear()

    await update.callback_query.message.reply_text(
        "✂️ Split PDF\n\n"
        "একটি PDF পাঠাও।"
    )

    context.user_data["pdf_action"] = "split"


async def start_pdf_to_text(update, context):
    context.user_data.clear()

    await update.callback_query.message.reply_text(
        "📄 PDF → Text\n\n"
        "একটি PDF পাঠাও।"
    )

    context.user_data["pdf_action"] = "pdf_to_text"


async def start_pdf_to_image(update, context):
    context.user_data.clear()

    await update.callback_query.message.reply_text(
        "🖼️ PDF → Image\n\n"
        "একটি PDF পাঠাও।"
    )

    context.user_data["pdf_action"] = "pdf_to_image"


async def start_protect_pdf(update, context):
    context.user_data.clear()

    await update.callback_query.message.reply_text(
        "🔐 Protect PDF\n\n"
        "একটি PDF পাঠাও।"
    )

    context.user_data["pdf_action"] = "protect"
    context.user_data["protect_waiting_pdf"] = True


async def handle_pdf_document(update, context):
    if not update.message or not update.message.document:
        return

    action = context.user_data.get(
        "pdf_action"
    )

    if action not in (
        "merge",
        "split",
        "pdf_to_text",
        "pdf_to_image",
        "protect",
    ):
        return

    document = update.message.document

    filename = document.file_name or "document.pdf"

    if not filename.lower().endswith(".pdf"):
        await update.message.reply_text(
            "⚠️ শুধু PDF file পাঠাও।"
        )
        return

    folder = context.user_data.get(
        "merge_folder"
    )

    if action == "merge":
        if not folder:
            folder = create_temp_dir()
            context.user_data["merge_folder"] = (
                folder
            )

        merge_files = context.user_data.get(
            "merge_files",
            [],
        )

        file_number = len(merge_files) + 1

        file_path = os.path.join(
            folder,
            f"pdf_{file_number}.pdf",
        )

        try:
            telegram_file = await document.get_file()

            await telegram_file.download_to_drive(
                file_path
            )

            merge_files.append(file_path)

            context.user_data["merge_files"] = (
                merge_files
            )

            await update.message.reply_text(
                f"✅ PDF {file_number} যোগ হয়েছে.\n\n"
                "আরও PDF পাঠাও।\n"
                "সব শেষ হলে /done লিখো।"
            )

        except Exception as error:
            await update.message.reply_text(
                "❌ PDF save করা যায়নি.\n\n"
                f"{error}"
            )

        return

    folder = create_temp_dir()

    input_path = os.path.join(
        folder,
        "input.pdf",
    )

    try:
        telegram_file = await document.get_file()

        await telegram_file.download_to_drive(
            input_path
        )

        if action == "split":
            output_dir = os.path.join(
                folder,
                "pages",
            )

            files = split_pdf(
                input_path,
                output_dir,
            )

            for index, path in enumerate(
                files,
                start=1,
            ):
                with open(path, "rb") as page:
                    await update.message.reply_document(
                        document=page,
                        filename=f"page_{index}.pdf",
                    )

            return

        if action == "pdf_to_text":
            text = pdf_to_text(
                input_path
            )

            if not text.strip():
                text = (
                    "⚠️ এই PDF থেকে কোনো text "
                    "extract করা যায়নি।"
                )

            # Telegram message limit এড়ানোর জন্য
            # text file হিসেবে পাঠানো হচ্ছে।
            text_path = os.path.join(
                folder,
                "extracted.txt",
            )

            with open(
                text_path,
                "w",
                encoding="utf-8",
            ) as text_file:
                text_file.write(text)

            with open(
                text_path,
                "rb",
            ) as text_file:
                await update.message.reply_document(
                    document=text_file,
                    filename="extracted.txt",
                    caption="✅ PDF → Text complete!",
                )

            return

        if action == "pdf_to_image":
            output_dir = os.path.join(
                folder,
                "images",
            )

            files = pdf_to_images(
                input_path,
                output_dir,
            )

            for index, path in enumerate(
                files,
                start=1,
            ):
                with open(path, "rb") as image:
                    await update.message.reply_document(
                        document=image,
                        filename=f"page_{index}.png",
                    )

            return

        if action == "protect":
            context.user_data["protect_folder"] = (
                folder
            )
            context.user_data["protect_input"] = (
                input_path
            )

            await update.message.reply_text(
                "🔐 এখন PDF-এর জন্য password পাঠাও।"
            )

            return

    except Exception as error:
        await update.message.reply_text(
            "❌ PDF process করা যায়নি.\n\n"
            f"{error}"
        )

    finally:
        if not context.user_data.get(
            "protect_input"
        ):
            cleanup_temp_folder(folder)
            context.user_data.clear()


async def handle_protect_password(update, context):
    if not update.message or not update.message.text:
        return

    if context.user_data.get(
        "pdf_action"
    ) != "protect":
        return

    input_path = context.user_data.get(
        "protect_input"
    )

    folder = context.user_data.get(
        "protect_folder"
    )

    if not input_path or not folder:
        return

    password = update.message.text.strip()

    if not password:
        await update.message.reply_text(
            "⚠️ Empty password দেওয়া যাবে না।"
        )
        return

    output_path = os.path.join(
        folder,
        "protected.pdf",
    )

    try:
        protect_pdf(
            input_path,
            output_path,
            password,
        )

        with open(output_path, "rb") as pdf:
            await update.message.reply_document(
                document=pdf,
                filename="protected.pdf",
                caption="✅ PDF protected হয়েছে!",
            )

    except Exception as error:
        await update.message.reply_text(
            "❌ PDF protect করা যায়নি.\n\n"
            f"{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()


async def done_merge_pdf(update, context):
    if context.user_data.get(
        "pdf_action"
    ) != "merge":
        return False

    folder = context.user_data.get(
        "merge_folder"
    )

    pdf_files = context.user_data.get(
        "merge_files",
        [],
    )

    if not folder:
        return True

    if not pdf_files:
        await update.message.reply_text(
            "⚠️ কোনো PDF পাওয়া যায়নি।"
        )
        return True

    output_path = os.path.join(
        folder,
        "merged.pdf",
    )

    try:
        merge_pdfs(
            pdf_files,
            output_path,
        )

        with open(output_path, "rb") as pdf:
            await update.message.reply_document(
                document=pdf,
                filename="merged.pdf",
                caption="✅ PDFs merge হয়েছে!",
            )

    except Exception as error:
        await update.message.reply_text(
            "❌ PDF merge করা যায়নি.\n\n"
            f"{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()

    return True


# Compatibility alias
handle_image = handle_image_to_pdf
