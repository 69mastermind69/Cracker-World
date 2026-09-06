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
)
from utils.files import create_temp_dir, cleanup_temp_folder


async def start_text_to_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["pdf_action"] = "text_to_pdf"

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "📝 Text → PDF\n\n"
        "যে লেখাটি PDF করতে চাও, সেটি এখানে পাঠাও।"
    )


async def start_image_to_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["pdf_action"] = "image_to_pdf"
    context.user_data["pdf_images"] = []

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "🖼️ Image → PDF\n\n"
        "এক বা একাধিক ছবি পাঠাও।\n"
        "সব ছবি পাঠানো শেষ হলে /done লিখো।"
    )


async def start_merge_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["pdf_action"] = "merge_pdf"
    context.user_data["pdf_files"] = []

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "📚 Merge PDF\n\n"
        "একাধিক PDF পাঠাও।\n"
        "সব পাঠানো শেষ হলে /done লিখো।"
    )


async def start_split_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["pdf_action"] = "split_pdf"

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "✂️ Split PDF\n\n"
        "যে PDF-টি ভাগ করতে চাও সেটি পাঠাও।"
    )


async def start_pdf_to_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["pdf_action"] = "pdf_to_text"

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "📄 PDF → Text\n\n"
        "একটি PDF পাঠাও।"
    )


async def start_protect_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["pdf_action"] = "protect_pdf"

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "🔐 Protect PDF\n\n"
        "প্রথমে PDF পাঠাও। তারপর password দিতে বলব।"
    )


async def handle_pdf_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    action = context.user_data.get("pdf_action")

    if action != "text_to_pdf":
        return

    text = update.message.text

    folder = create_temp_dir()
    output_path = os.path.join(folder, "document.pdf")

    try:
        text_to_pdf(text, output_path)

        with open(output_path, "rb") as pdf_file:
            await update.message.reply_document(
                document=pdf_file,
                filename="document.pdf",
                caption="✅ তোমার PDF তৈরি হয়েছে!"
            )

    except Exception as error:
        await update.message.reply_text(
            f"❌ PDF তৈরি করা যায়নি:\n{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.pop("pdf_action", None)


async def handle_pdf_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    action = context.user_data.get("pdf_action")

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

    if not document.file_name.lower().endswith(".pdf"):
        await update.message.reply_text(
            "❌ দয়া করে একটি PDF file পাঠাও।"
        )
        return

    folder = create_temp_dir()
    input_path = os.path.join(folder, "input.pdf")

    try:
        telegram_file = await document.get_file()
        await telegram_file.download_to_drive(input_path)

        if action == "split_pdf":
            output_dir = os.path.join(folder, "pages")
            files = split_pdf(input_path, output_dir)

            await update.message.reply_text(
                f"✅ PDF split হয়েছে!\n"
                f"মোট {len(files)}টি page পাওয়া গেছে।"
            )

            for file_path in files:
                with open(file_path, "rb") as file:
                    await update.message.reply_document(
                        document=file,
                        filename=os.path.basename(file_path)
                    )

        elif action == "pdf_to_text":
            text = pdf_to_text(input_path)

            if not text.strip():
                await update.message.reply_text(
                    "⚠️ এই PDF থেকে text পাওয়া যায়নি। "
                    "সম্ভবত এটি scanned/image PDF।"
                )
            else:
                # Telegram message limit এড়াতে ভাগ করে পাঠানো
                chunk_size = 3500

                await update.message.reply_text(
                    "✅ PDF থেকে text বের করা হয়েছে:"
                )

                for i in range(0, len(text), chunk_size):
                    await update.message.reply_text(
                        text[i:i + chunk_size]
                    )

        elif action == "protect_pdf":
            context.user_data["protect_pdf_path"] = input_path

            await update.message.reply_text(
                "🔐 এখন PDF-এর জন্য password পাঠাও।"
            )

            # Cleanup এখানে নয়; password পাওয়ার পর করা হবে।
            return

        elif action == "merge_pdf":
            context.user_data.setdefault("merge_pdf_paths", [])
            context.user_data["merge_pdf_paths"].append(input_path)

            await update.message.reply_text(
                "✅ PDF যোগ করা হয়েছে।\n\n"
                "আরও PDF পাঠাতে পারো।\n"
                "সব শেষ হলে /done লিখো।"
            )

            # Input fileগুলো এখনই delete করা যাবে না।
            return

    except Exception as error:
        await update.message.reply_text(
            f"❌ PDF process করা যায়নি:\n{error}"
        )

    finally:
        if action not in ("protect_pdf", "merge_pdf"):
            cleanup_temp_folder(folder)

        context.user_data.pop("pdf_action", None)


async def handle_protect_password(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    input_path = context.user_data.get("protect_pdf_path")

    if not input_path:
        return

    password = update.message.text

    folder = os.path.dirname(input_path)
    output_path = os.path.join(folder, "protected.pdf")

    try:
        protect_pdf(
            input_path,
            output_path,
            password
        )

        with open(output_path, "rb") as pdf_file:
            await update.message.reply_document(
                document=pdf_file,
                filename="protected.pdf",
                caption="✅ PDF password protected হয়েছে!"
            )

    except Exception as error:
        await update.message.reply_text(
            f"❌ PDF protect করা যায়নি:\n{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.pop("protect_pdf_path", None)
        context.user_data.pop("pdf_action", None)


async def done_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Finish image-to-PDF or merge-PDF collection.
    """

    # Image → PDF
    image_paths = context.user_data.get("pdf_images")

    if image_paths:
        folder = os.path.dirname(image_paths[0])
        output_path = os.path.join(folder, "images.pdf")

        try:
            images_to_pdf(
                image_paths,
                output_path
            )

            with open(output_path, "rb") as pdf_file:
                await update.message.reply_document(
                    document=pdf_file,
                    filename="images.pdf",
                    caption="✅ Images থেকে PDF তৈরি হয়েছে!"
                )

        except Exception as error:
            await update.message.reply_text(
                f"❌ PDF তৈরি করা যায়নি:\n{error}"
            )

        finally:
            cleanup_temp_folder(folder)
            context.user_data.pop("pdf_images", None)
            context.user_data.pop("pdf_action", None)

        return

    # Merge PDF
    pdf_paths = context.user_data.get("merge_pdf_paths")

    if pdf_paths:
        folder = os.path.dirname(pdf_paths[0])
        output_path = os.path.join(folder, "merged.pdf")

        try:
            merge_pdfs(
                pdf_paths,
                output_path
            )

            with open(output_path, "rb") as pdf_file:
                await update.message.reply_document(
                    document=pdf_file,
                    filename="merged.pdf",
                    caption="✅ PDFs merge হয়েছে!"
                )

        except Exception as error:
            await update.message.reply_text(
                f"❌ PDF merge করা যায়নি:\n{error}"
            )

        finally:
            cleanup_temp_folder(folder)
            context.user_data.pop("merge_pdf_paths", None)
            context.user_data.pop("pdf_action", None)

        return

    await update.message.reply_text(
        "⚠️ শেষ করার মতো কোনো PDF task পাওয়া যায়নি।"
    )
