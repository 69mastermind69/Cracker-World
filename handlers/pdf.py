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


# =========================================================
# TEXT → PDF
# =========================================================

async def start_text_to_pdf(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()

    context.user_data[
        "pdf_action"
    ] = "text_to_pdf"

    await update.callback_query.message.reply_text(
        "📝 Text → PDF\n\n"
        "যে লেখাটি PDF করতে চাও সেটি পাঠাও।"
    )


async def handle_pdf_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if context.user_data.get(
        "pdf_action"
    ) != "text_to_pdf":
        return

    if not update.message:
        return

    if not update.message.text:
        return

    text = update.message.text

    if not text.strip():
        await update.message.reply_text(
            "⚠️ খালি text দিয়ে PDF তৈরি করা যাবে না।"
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
            title="Telegram Document",
        )

        with open(
            output_path,
            "rb",
        ) as pdf:

            await update.message.reply_document(
                document=pdf,
                filename="document.pdf",
                caption="✅ তোমার PDF তৈরি হয়েছে!",
            )

    except Exception as error:

        await update.message.reply_text(
            "❌ PDF তৈরি করা যায়নি:\n"
            f"{error}"
        )

    finally:

        cleanup_temp_folder(folder)
        context.user_data.clear()


# =========================================================
# IMAGE → PDF
# =========================================================

async def start_image_to_pdf(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()

    folder = create_temp_dir()

    context.user_data[
        "pdf_action"
    ] = "image_to_pdf"

    context.user_data[
        "image_pdf_folder"
    ] = folder

    context.user_data[
        "image_pdf_paths"
    ] = []

    await update.callback_query.message.reply_text(
        "🖼️ Image → PDF\n\n"
        "এক বা একাধিক ছবি পাঠাও।\n\n"
        "সব ছবি পাঠানো শেষ হলে /done লিখো।"
    )


async def handle_image(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if context.user_data.get(
        "pdf_action"
    ) != "image_to_pdf":
        return

    if not update.message:
        return

    if not update.message.photo:
        return

    folder = context.user_data.get(
        "image_pdf_folder"
    )

    if not folder:
        return

    photo = update.message.photo[-1]

    image_number = (
        len(
            context.user_data.get(
                "image_pdf_paths",
                [],
            )
        )
        + 1
    )

    file_path = os.path.join(
        folder,
        f"image_{image_number}.jpg",
    )

    try:

        telegram_file = await photo.get_file()

        await telegram_file.download_to_drive(
            file_path
        )

        context.user_data[
            "image_pdf_paths"
        ].append(
            file_path
        )

        count = len(
            context.user_data[
                "image_pdf_paths"
            ]
        )

        await update.message.reply_text(
            f"✅ Image {count} যোগ হয়েছে।\n\n"
            "আরও image পাঠাতে পারো।\n"
            "শেষ হলে /done লিখো।"
        )

    except Exception as error:

        await update.message.reply_text(
            "❌ Image save করা যায়নি:\n"
            f"{error}"
        )


# =========================================================
# DONE
# =========================================================

async def done_pdf(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    action = context.user_data.get(
        "pdf_action"
    )

    # -----------------------------------------------------
    # IMAGE → PDF
    # -----------------------------------------------------

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
                "⚠️ Image → PDF task পাওয়া যায়নি।"
            )
            return

        if not image_paths:

            await update.message.reply_text(
                "⚠️ কোনো image পাওয়া যায়নি।"
            )
            return

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
                    caption=(
                        "✅ Images থেকে PDF তৈরি হয়েছে!"
                    ),
                )

        except Exception as error:

            await update.message.reply_text(
                "❌ PDF তৈরি করা যায়নি:\n"
                f"{error}"
            )

        finally:

            cleanup_temp_folder(
                folder
            )

            context.user_data.clear()

        return

    # -----------------------------------------------------
    # MERGE PDF
    # -----------------------------------------------------

    if action == "merge_pdf":

        folder = context.user_data.get(
            "merge_pdf_folder"
        )

        pdf_paths = context.user_data.get(
            "merge_pdf_paths",
            [],
        )

        if not folder:
            await update.message.reply_text(
                "⚠️ Merge PDF task পাওয়া যায়নি।"
            )
            return

        if len(pdf_paths) < 2:

            await update.message.reply_text(
                "⚠️ Merge করার জন্য "
                "অন্তত ২টি PDF পাঠাও।"
            )
            return

        output_path = os.path.join(
            folder,
            "merged.pdf",
        )

        try:

            merge_pdfs(
                pdf_paths,
                output_path,
            )

            with open(
                output_path,
                "rb",
            ) as pdf:

                await update.message.reply_document(
                    document=pdf,
                    filename="merged.pdf",
                    caption=(
                        "✅ PDFs successfully "
                        "merge হয়েছে!"
                    ),
                )

        except Exception as error:

            await update.message.reply_text(
                "❌ PDF merge করা যায়নি:\n"
                f"{error}"
            )

        finally:

            cleanup_temp_folder(
                folder
            )

            context.user_data.clear()

        return

    await update.message.reply_text(
        "⚠️ কোনো active PDF task নেই।"
    )


# =========================================================
# MERGE PDF
# =========================================================

async def start_merge_pdf(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()

    folder = create_temp_dir()

    context.user_data[
        "pdf_action"
    ] = "merge_pdf"

    context.user_data[
        "merge_pdf_folder"
    ] = folder

    context.user_data[
        "merge_pdf_paths"
    ] = []

    await update.callback_query.message.reply_text(
        "📚 Merge PDF\n\n"
        "কমপক্ষে ২টি PDF পাঠাও।\n\n"
        "সব পাঠানো শেষ হলে /done লিখো।"
    )


# =========================================================
# SPLIT PDF
# =========================================================

async def start_split_pdf(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()

    context.user_data[
        "pdf_action"
    ] = "split_pdf"

    await update.callback_query.message.reply_text(
        "✂️ Split PDF\n\n"
        "যে PDF-টি split করতে চাও সেটি পাঠাও।"
    )


# =========================================================
# PDF → TEXT
# =========================================================

async def start_pdf_to_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()

    context.user_data[
        "pdf_action"
    ] = "pdf_to_text"

    await update.callback_query.message.reply_text(
        "📄 PDF → Text\n\n"
        "একটি PDF পাঠাও।"
    )


# =========================================================
# PDF → IMAGE
# =========================================================

async def start_pdf_to_image(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()

    context.user_data[
        "pdf_action"
    ] = "pdf_to_image"

    await update.callback_query.message.reply_text(
        "🖼️ PDF → Image\n\n"
        "একটি PDF file পাঠাও।\n\n"
        "প্রতিটি page আলাদা PNG image "
        "হিসেবে পাবে।"
    )


async def handle_pdf_to_image(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    document = update.message.document

    if not document:
        return

    filename = (
        document.file_name
        or "input.pdf"
    )

    if not filename.lower().endswith(
        ".pdf"
    ):

        await update.message.reply_text(
            "❌ দয়া করে একটি PDF file পাঠাও।"
        )
        return

    folder = create_temp_dir()

    input_path = os.path.join(
        folder,
        "input.pdf",
    )

    image_dir = os.path.join(
        folder,
        "images",
    )

    try:

        telegram_file = (
            await document.get_file()
        )

        await telegram_file.download_to_drive(
            input_path
        )

        output_files = pdf_to_images(
            input_path,
            image_dir,
            dpi=150,
        )

        if not output_files:

            raise RuntimeError(
                "PDF থেকে কোনো page image "
                "তৈরি করা যায়নি।"
            )

        for index, image_path in enumerate(
            output_files,
            start=1,
        ):

            with open(
                image_path,
                "rb",
            ) as image_file:

                await update.message.reply_document(
                    document=image_file,
                    filename=f"page_{index}.png",
                )

        await update.message.reply_text(
            "✅ PDF → Image complete!\n\n"
            f"📄 মোট {len(output_files)}টি "
            "page image হিসেবে তৈরি হয়েছে।"
        )

    except Exception as error:

        await update.message.reply_text(
            "❌ PDF → Image করা যায়নি:\n"
            f"{error}"
        )

    finally:

        cleanup_temp_folder(
            folder
        )

        context.user_data.clear()


# =========================================================
# PROTECT PDF
# =========================================================

async def start_protect_pdf(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()

    context.user_data[
        "pdf_action"
    ] = "protect_pdf"

    await update.callback_query.message.reply_text(
        "🔐 Protect PDF\n\n"
        "প্রথমে PDF পাঠাও।\n"
        "তারপর password দিতে বলব।"
    )


# =========================================================
# PDF DOCUMENT HANDLER
# =========================================================

async def handle_pdf_document(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    action = context.user_data.get(
        "pdf_action"
    )

    if action not in (
        "split_pdf",
        "pdf_to_text",
        "protect_pdf",
        "merge_pdf",
    ):
        return

    document = update.message.document

    if not document:
        return

    filename = (
        document.file_name
        or ""
    )

    if not filename.lower().endswith(
        ".pdf"
    ):

        await update.message.reply_text(
            "❌ দয়া করে একটি PDF file পাঠাও।"
        )
        return

    # -----------------------------------------------------
    # MERGE PDF
    # -----------------------------------------------------

    if action == "merge_pdf":

        folder = context.user_data.get(
            "merge_pdf_folder"
        )

        if not folder:
            return

        number = (
            len(
                context.user_data.get(
                    "merge_pdf_paths",
                    [],
                )
            )
            + 1
        )

        file_path = os.path.join(
            folder,
            f"pdf_{number}.pdf",
        )

        try:

            telegram_file = (
                await document.get_file()
            )

            await telegram_file.download_to_drive(
                file_path
            )

            context.user_data[
                "merge_pdf_paths"
            ].append(
                file_path
            )

            count = len(
                context.user_data[
                    "merge_pdf_paths"
                ]
            )

            await update.message.reply_text(
                f"✅ PDF {count} যোগ হয়েছে।\n\n"
                "আরও PDF পাঠাতে পারো।\n"
                "সব শেষ হলে /done লিখো।"
            )

        except Exception as error:

            await update.message.reply_text(
                "❌ PDF save করা যায়নি:\n"
                f"{error}"
            )

        return

    # -----------------------------------------------------
    # OTHER PDF OPERATIONS
    # -----------------------------------------------------

    folder = create_temp_dir()

    input_path = os.path.join(
        folder,
        "input.pdf",
    )

    try:

        telegram_file = (
            await document.get_file()
        )

        await telegram_file.download_to_drive(
            input_path
        )

        # -------------------------------------------------
        # SPLIT
        # -------------------------------------------------

        if action == "split_pdf":

            output_dir = os.path.join(
                folder,
                "pages",
            )

            files = split_pdf(
                input_path,
                output_dir,
            )

            await update.message.reply_text(
                "✅ PDF split হয়েছে!\n"
                f"মোট {len(files)}টি page পাওয়া গেছে।"
            )

            for file_path in files:

                with open(
                    file_path,
                    "rb",
                ) as pdf:

                    await update.message.reply_document(
                        document=pdf,
                        filename=os.path.basename(
                            file_path
                        ),
                    )

        # -------------------------------------------------
        # PDF → TEXT
        # -------------------------------------------------

        elif action == "pdf_to_text":

            text = pdf_to_text(
                input_path
            )

            if not text.strip():

                await update.message.reply_text(
                    "⚠️ এই PDF থেকে text পাওয়া যায়নি।"
                )

            else:

                await update.message.reply_text(
                    "✅ PDF থেকে text বের করা হয়েছে:"
                )

                chunk_size = 3500

                for i in range(
                    0,
                    len(text),
                    chunk_size,
                ):

                    await update.message.reply_text(
                        text[
                            i:i + chunk_size
                        ]
                    )

        # -------------------------------------------------
        # PROTECT PDF
        # -------------------------------------------------

        elif action == "protect_pdf":

            context.user_data[
                "protect_pdf_path"
            ] = input_path

            context.user_data[
                "protect_pdf_folder"
            ] = folder

            await update.message.reply_text(
                "🔐 এখন একটি password পাঠাও।"
            )

            return

    except Exception as error:

        await update.message.reply_text(
            "❌ PDF process করা যায়নি:\n"
            f"{error}"
        )

    finally:

        if action != "protect_pdf":

            cleanup_temp_folder(
                folder
            )

            context.user_data.clear()


# =========================================================
# PASSWORD HANDLER
# =========================================================

async def handle_protect_password(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    input_path = context.user_data.get(
        "protect_pdf_path"
    )

    folder = context.user_data.get(
        "protect_pdf_folder"
    )

    if not input_path or not folder:
        return

    password = (
        update.message.text.strip()
    )

    if len(password) < 4:

        await update.message.reply_text(
            "⚠️ Password কমপক্ষে "
            "৪টি character দাও।"
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

        with open(
            output_path,
            "rb",
        ) as pdf:

            await update.message.reply_document(
                document=pdf,
                filename="protected.pdf",
                caption=(
                    "✅ PDF password protected হয়েছে!"
                ),
            )

    except Exception as error:

        await update.message.reply_text(
            "❌ PDF protect করা যায়নি:\n"
            f"{error}"
        )

    finally:

        cleanup_temp_folder(
            folder
        )

        context.user_data.clear()
