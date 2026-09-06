import os

from telegram import Update
from telegram.ext import ContextTypes

from config import MAX_FILE_SIZE_MB
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


def _file_too_large(size_bytes):
    return (
        size_bytes
        and size_bytes
        > MAX_FILE_SIZE_MB * 1024 * 1024
    )


async def _download_document(
    update,
    document,
    folder,
):
    filename = os.path.basename(
        document.file_name or "file"
    )

    path = os.path.join(
        folder,
        filename,
    )

    telegram_file = await document.get_file()
    await telegram_file.download_to_drive(path)

    return path


async def start_text_to_pdf(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()
    context.user_data["pdf_action"] = (
        "text_to_pdf"
    )

    query = update.callback_query

    await query.answer()
    await query.edit_message_text(
        "📝 <b>Text → PDF</b>\n\n"
        "যে text PDF করতে চাও সেটা পাঠাও।",
        parse_mode="HTML",
    )


async def handle_pdf_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    text = update.message.text or ""

    if not text.strip():
        await update.message.reply_text(
            "⚠️ Empty text পাঠানো যাবে না।"
        )
        return

    folder = create_temp_dir()
    output = os.path.join(
        folder,
        "document.pdf",
    )

    try:
        text_to_pdf(
            text,
            output,
            title="Document",
        )

        with open(
            output,
            "rb",
        ) as file:
            await update.message.reply_document(
                document=file,
                filename="document.pdf",
                caption="📄 PDF তৈরি হয়েছে!",
            )

    except Exception as error:
        await update.message.reply_text(
            f"❌ PDF তৈরি করা যায়নি:\n{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()


async def start_image_to_pdf(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()

    folder = create_temp_dir()

    context.user_data["pdf_action"] = (
        "image_to_pdf"
    )
    context.user_data["pdf_image_folder"] = (
        folder
    )
    context.user_data["pdf_image_paths"] = []

    query = update.callback_query

    await query.answer()
    await query.edit_message_text(
        "🖼️ <b>Image → PDF</b>\n\n"
        "এক বা একাধিক image পাঠাও।\n\n"
        "সবশেষে /done লিখো।",
        parse_mode="HTML",
    )


async def handle_image_to_pdf(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    if not update.message.photo:
        return

    data = context.user_data

    if data.get("pdf_action") != "image_to_pdf":
        return

    folder = data.get(
        "pdf_image_folder"
    )

    if not folder:
        folder = create_temp_dir()
        data["pdf_image_folder"] = folder

    photo = update.message.photo[-1]

    if _file_too_large(
        getattr(photo, "file_size", 0)
    ):
        await update.message.reply_text(
            f"⚠️ File size {MAX_FILE_SIZE_MB}MB-এর বেশি।"
        )
        return

    filename = (
        f"image_"
        f"{len(data.get('pdf_image_paths', [])) + 1}"
        f".jpg"
    )

    path = os.path.join(
        folder,
        filename,
    )

    try:
        telegram_file = await photo.get_file()
        await telegram_file.download_to_drive(
            path
        )

        data.setdefault(
            "pdf_image_paths",
            [],
        ).append(path)

        count = len(
            data["pdf_image_paths"]
        )

        await update.message.reply_text(
            f"✅ Image {count} added.\n"
            "আরও image পাঠাতে পারো।\n"
            "শেষ হলে /done লিখো।"
        )

    except Exception as error:
        await update.message.reply_text(
            f"❌ Image save করা যায়নি:\n{error}"
        )


async def done_pdf(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    data = context.user_data

    if data.get("pdf_action") != "image_to_pdf":
        return

    image_paths = data.get(
        "pdf_image_paths",
        [],
    )

    folder = data.get(
        "pdf_image_folder"
    )

    if not image_paths:
        await update.message.reply_text(
            "❌ কোনো image যোগ করা হয়নি।"
        )
        return

    if not folder:
        await update.message.reply_text(
            "❌ Temporary folder পাওয়া যায়নি।"
        )
        context.user_data.clear()
        return

    output = os.path.join(
        folder,
        "images.pdf",
    )

    try:
        images_to_pdf(
            image_paths,
            output,
        )

        with open(
            output,
            "rb",
        ) as file:
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
        context.user_data.clear()


async def start_merge_pdf(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()

    folder = create_temp_dir()

    context.user_data["pdf_action"] = "merge"
    context.user_data["merge_folder"] = folder
    context.user_data["merge_files"] = []

    query = update.callback_query

    await query.answer()
    await query.edit_message_text(
        "📚 <b>Merge PDF</b>\n\n"
        "যে PDF files merge করতে চাও "
        "সেগুলো একে একে পাঠাও।\n\n"
        "শেষ হলে /done লিখো।",
        parse_mode="HTML",
    )


async def start_split_pdf(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()
    context.user_data["pdf_action"] = "split"

    query = update.callback_query

    await query.answer()
    await query.edit_message_text(
        "✂️ <b>Split PDF</b>\n\n"
        "একটি PDF file পাঠাও।",
        parse_mode="HTML",
    )


async def start_pdf_to_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()
    context.user_data["pdf_action"] = (
        "pdf_to_text"
    )

    query = update.callback_query

    await query.answer()
    await query.edit_message_text(
        "📄 <b>PDF → Text</b>\n\n"
        "একটি PDF file পাঠাও।",
        parse_mode="HTML",
    )


async def start_pdf_to_image(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()
    context.user_data["pdf_action"] = (
        "pdf_to_image"
    )

    query = update.callback_query

    await query.answer()
    await query.edit_message_text(
        "🖼️ <b>PDF → Image</b>\n\n"
        "একটি PDF file পাঠাও।",
        parse_mode="HTML",
    )


async def start_protect_pdf(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()

    folder = create_temp_dir()

    context.user_data["pdf_action"] = "protect"
    context.user_data["protect_folder"] = folder
    context.user_data["protect_waiting_pdf"] = True

    query = update.callback_query

    await query.answer()
    await query.edit_message_text(
        "🔐 <b>Protect PDF</b>\n\n"
        "প্রথমে একটি PDF file পাঠাও।",
        parse_mode="HTML",
    )


async def handle_pdf_document(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    document = update.message.document

    if not document:
        return

    filename = (
        document.file_name or ""
    )

    if not filename.lower().endswith(
        ".pdf"
    ):
        await update.message.reply_text(
            "⚠️ শুধু PDF file পাঠাও।"
        )
        return

    if _file_too_large(
        getattr(document, "file_size", 0)
    ):
        await update.message.reply_text(
            f"⚠️ File size {MAX_FILE_SIZE_MB}MB-এর বেশি।"
        )
        return

    data = context.user_data
    action = data.get("pdf_action")

    if action == "merge":
        folder = data.get(
            "merge_folder"
        )

        if not folder:
            folder = create_temp_dir()
            data["merge_folder"] = folder

        try:
            path = await _download_document(
                update,
                document,
                folder,
            )

            files = data.setdefault(
                "merge_files",
                [],
            )

            files.append(path)

            await update.message.reply_text(
                f"✅ {filename} added.\n"
                "আরও PDF পাঠাতে পারো।\n"
                "শেষ হলে /done লিখো।"
            )

        except Exception as error:
            await update.message.reply_text(
                f"❌ PDF save করা যায়নি:\n{error}"
            )

        return

    if action == "split":
        folder = create_temp_dir()

        try:
            input_path = (
                await _download_document(
                    update,
                    document,
                    folder,
                )
            )

            output_dir = os.path.join(
                folder,
                "pages",
            )

            pages = split_pdf(
                input_path,
                output_dir,
            )

            await update.message.reply_text(
                f"✂️ PDF split হয়েছে: "
                f"{len(pages)} page"
            )

            for page_path in pages:
                with open(
                    page_path,
                    "rb",
                ) as file:
                    await update.message.reply_document(
                        document=file,
                        filename=os.path.basename(
                            page_path
                        ),
                    )

        except Exception as error:
            await update.message.reply_text(
                f"❌ PDF split করা যায়নি:\n{error}"
            )

        finally:
            cleanup_temp_folder(folder)
            context.user_data.clear()

        return

    if action == "pdf_to_text":
        folder = create_temp_dir()

        try:
            input_path = (
                await _download_document(
                    update,
                    document,
                    folder,
                )
            )

            output_path = os.path.join(
                folder,
                "extracted.txt",
            )

            pdf_to_text(
                input_path,
                output_path,
            )

            with open(
                output_path,
                "rb",
            ) as file:
                await update.message.reply_document(
                    document=file,
                    filename="extracted.txt",
                    caption="📄 PDF → Text complete!",
                )

        except Exception as error:
            await update.message.reply_text(
                f"❌ Text extract করা যায়নি:\n{error}"
            )

        finally:
            cleanup_temp_folder(folder)
            context.user_data.clear()

        return

    if action == "pdf_to_image":
        folder = create_temp_dir()

        try:
            input_path = (
                await _download_document(
                    update,
                    document,
                    folder,
                )
            )

            output_dir = os.path.join(
                folder,
                "images",
            )

            images = pdf_to_images(
                input_path,
                output_dir,
                "png",
            )

            await update.message.reply_text(
                f"🖼️ {len(images)} image তৈরি হয়েছে।"
            )

            for image_path in images:
                with open(
                    image_path,
                    "rb",
                ) as file:
                    await update.message.reply_document(
                        document=file,
                        filename=os.path.basename(
                            image_path
                        ),
                    )

        except Exception as error:
            await update.message.reply_text(
                f"❌ PDF → Image করা যায়নি:\n{error}"
            )

        finally:
            cleanup_temp_folder(folder)
            context.user_data.clear()

        return

    if action == "protect":
        folder = data.get(
            "protect_folder"
        )

        if not folder:
            folder = create_temp_dir()
            data["protect_folder"] = folder

        try:
            input_path = (
                await _download_document(
                    update,
                    document,
                    folder,
                )
            )

            data["protect_input"] = input_path
            data["protect_waiting_pdf"] = False
            data["protect_waiting_password"] = True

            await update.message.reply_text(
                "🔑 এখন PDF-এর জন্য password পাঠাও।"
            )

        except Exception as error:
            await update.message.reply_text(
                f"❌ PDF save করা যায়নি:\n{error}"
            )

        return

    await update.message.reply_text(
        "ℹ️ PDF action active নেই।"
    )


async def handle_protect_password(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    data = context.user_data

    if data.get("pdf_action") != "protect":
        return

    input_path = data.get(
        "protect_input"
    )

    password = (
        update.message.text or ""
    ).strip()

    if not input_path:
        await update.message.reply_text(
            "❌ PDF file পাওয়া যায়নি।"
        )
        context.user_data.clear()
        return

    if not password:
        await update.message.reply_text(
            "⚠️ Password empty হতে পারবে না।"
        )
        return

    folder = data.get(
        "protect_folder"
    )

    if not folder:
        folder = create_temp_dir()

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

        with open(
            output_path,
            "rb",
        ) as file:
            await update.message.reply_document(
                document=file,
                filename="protected.pdf",
                caption="🔐 PDF protected হয়েছে!",
            )

    except Exception as error:
        await update.message.reply_text(
            f"❌ PDF protect করা যায়নি:\n{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()


async def done_merge_pdf(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return True

    data = context.user_data

    if data.get("pdf_action") != "merge":
        return True

    files = data.get(
        "merge_files",
        [],
    )

    folder = data.get(
        "merge_folder"
    )

    if not files:
        await update.message.reply_text(
            "❌ কোনো PDF যোগ করা হয়নি।"
        )
        return True

    if not folder:
        await update.message.reply_text(
            "❌ Temporary folder পাওয়া যায়নি।"
        )
        context.user_data.clear()
        return True

    output = os.path.join(
        folder,
        "merged.pdf",
    )

    try:
        merge_pdfs(
            files,
            output,
        )

        with open(
            output,
            "rb",
        ) as file:
            await update.message.reply_document(
                document=file,
                filename="merged.pdf",
                caption="📚 PDF merge complete!",
            )

    except Exception as error:
        await update.message.reply_text(
            f"❌ PDF merge করা যায়নি:\n{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()

    return True


# Compatibility alias
handle_image = handle_image_to_pdf
