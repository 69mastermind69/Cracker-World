import os
import re

from telegram import Update
from telegram.ext import ContextTypes

from services.qr_service import (
    generate_qr,
    generate_qr_wifi,
    generate_qr_contact,
    generate_qr_email,
    generate_qr_phone,
)

from services.qr_scanner import scan_qr

from utils.files import (
    create_temp_dir,
    cleanup_temp_folder,
)


# ============================================================
# HELPERS
# ============================================================

def get_query_message(update):
    """Return the callback message safely."""
    if update.callback_query:
        return update.callback_query.message

    return update.message


def set_qr_action(context, action):
    context.user_data.clear()
    context.user_data["qr_action"] = action


# ============================================================
# TEXT → QR
# ============================================================

async def start_qr_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    set_qr_action(context, "qr_text")

    await get_query_message(update).reply_text(
        "📝 *Text → QR*\n\n"
        "যে text-টি QR code বানাতে চাও সেটি পাঠাও।",
        parse_mode="Markdown",
    )


# ============================================================
# URL → QR
# ============================================================

async def start_qr_url(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    set_qr_action(context, "qr_url")

    await get_query_message(update).reply_text(
        "🌐 *URL → QR*\n\n"
        "একটি website URL পাঠাও।\n\n"
        "উদাহরণ:\n"
        "https://example.com",
        parse_mode="Markdown",
    )


# ============================================================
# WIFI → QR
# ============================================================

async def start_qr_wifi(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    set_qr_action(context, "qr_wifi")

    await get_query_message(update).reply_text(
        "📶 *Wi-Fi → QR*\n\n"
        "এই format-এ পাঠাও:\n\n"
        "SSID | PASSWORD | WPA\n\n"
        "উদাহরণ:\n"
        "MyWifi | 12345678 | WPA\n\n"
        "Password না থাকলে:\n"
        "MyWifi | | nopass",
        parse_mode="Markdown",
    )


# ============================================================
# CONTACT → QR
# ============================================================

async def start_qr_contact(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    set_qr_action(context, "qr_contact")

    await get_query_message(update).reply_text(
        "👤 *Contact → QR*\n\n"
        "এই format-এ পাঠাও:\n\n"
        "Name | Phone | Email\n\n"
        "উদাহরণ:\n"
        "John Doe | +8801712345678 | john@example.com",
        parse_mode="Markdown",
    )


# ============================================================
# EMAIL → QR
# ============================================================

async def start_qr_email(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    set_qr_action(context, "qr_email")

    await get_query_message(update).reply_text(
        "📧 *Email → QR*\n\n"
        "এই format-এ পাঠাও:\n\n"
        "Email | Subject | Message\n\n"
        "উদাহরণ:\n"
        "test@example.com | Hello | This is a message.",
        parse_mode="Markdown",
    )


# ============================================================
# PHONE → QR
# ============================================================

async def start_qr_phone(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    set_qr_action(context, "qr_phone")

    await get_query_message(update).reply_text(
        "📱 *Phone → QR*\n\n"
        "একটি phone number পাঠাও।\n\n"
        "উদাহরণ:\n"
        "+8801712345678",
        parse_mode="Markdown",
    )


# ============================================================
# QR SCANNER
# ============================================================

async def start_qr_scan(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    set_qr_action(context, "qr_scan")

    await get_query_message(update).reply_text(
        "🔍 *Scan QR*\n\n"
        "একটি QR code-এর image পাঠাও।"
    )


# ============================================================
# QR → PDF
# ============================================================

async def start_qr_to_pdf(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    set_qr_action(context, "qr_to_pdf")

    await get_query_message(update).reply_text(
        "📄 *QR → PDF*\n\n"
        "একটি QR image পাঠাও।"
    )


# ============================================================
# QR GENERATION
# ============================================================

async def generate_and_send_qr(
    update,
    context,
    data,
    filename="qr.png",
):
    folder = create_temp_dir()

    try:
        output_path = os.path.join(
            folder,
            filename,
        )

        generate_qr(
            data,
            output_path,
        )

        with open(output_path, "rb") as image:
            await update.message.reply_photo(
                photo=image,
                caption="✅ QR code তৈরি হয়েছে!",
            )

        # Also provide PNG file
        with open(output_path, "rb") as image:
            await update.message.reply_document(
                document=image,
                filename=filename,
            )

    except Exception as error:
        await update.message.reply_text(
            f"❌ QR তৈরি করা যায়নি:\n{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()


# ============================================================
# QR TEXT HANDLER
# ============================================================

async def handle_qr_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message or not update.message.text:
        return

    action = context.user_data.get("qr_action")

    if not action:
        return

    text = update.message.text.strip()

    if not text:
        await update.message.reply_text(
            "⚠️ Empty input দেওয়া যাবে না।"
        )
        return

    # ========================================================
    # TEXT
    # ========================================================

    if action == "qr_text":
        await generate_and_send_qr(
            update,
            context,
            text,
            "text_qr.png",
        )
        return

    # ========================================================
    # URL
    # ========================================================

    if action == "qr_url":
        if not re.match(
            r"^https?://",
            text,
            re.IGNORECASE,
        ):
            await update.message.reply_text(
                "⚠️ Valid URL দাও।\n\n"
                "উদাহরণ:\n"
                "https://example.com"
            )
            return

        await generate_and_send_qr(
            update,
            context,
            text,
            "url_qr.png",
        )
        return

    # ========================================================
    # WIFI
    # ========================================================

    if action == "qr_wifi":
        parts = [
            part.strip()
            for part in text.split("|")
        ]

        if len(parts) < 2:
            await update.message.reply_text(
                "❌ Format ভুল।\n\n"
                "SSID | PASSWORD | WPA"
            )
            return

        ssid = parts[0]
        password = parts[1]

        security = (
            parts[2]
            if len(parts) >= 3 and parts[2]
            else "WPA"
        )

        if not ssid:
            await update.message.reply_text(
                "❌ SSID দিতে হবে।"
            )
            return

        try:
            folder = create_temp_dir()

            output_path = os.path.join(
                folder,
                "wifi_qr.png",
            )

            generate_qr_wifi(
                ssid,
                password,
                security,
                output_path,
            )

            with open(output_path, "rb") as image:
                await update.message.reply_photo(
                    photo=image,
                    caption="✅ Wi-Fi QR তৈরি হয়েছে!",
                )

            with open(output_path, "rb") as image:
                await update.message.reply_document(
                    document=image,
                    filename="wifi_qr.png",
                )

        except Exception as error:
            await update.message.reply_text(
                f"❌ Wi-Fi QR তৈরি করা যায়নি:\n{error}"
            )

        finally:
            if "folder" in locals():
                cleanup_temp_folder(folder)

            context.user_data.clear()

        return

    # ========================================================
    # CONTACT
    # ========================================================

    if action == "qr_contact":
        parts = [
            part.strip()
            for part in text.split("|")
        ]

        if len(parts) < 2:
            await update.message.reply_text(
                "❌ Format ভুল।\n\n"
                "Name | Phone | Email"
            )
            return

        name = parts[0]
        phone = parts[1]
        email = parts[2] if len(parts) >= 3 else ""

        if not name or not phone:
            await update.message.reply_text(
                "❌ Name এবং Phone অবশ্যই দিতে হবে।"
            )
            return

        try:
            folder = create_temp_dir()

            output_path = os.path.join(
                folder,
                "contact_qr.png",
            )

            generate_qr_contact(
                name,
                phone,
                email,
                output_path,
            )

            with open(output_path, "rb") as image:
                await update.message.reply_photo(
                    photo=image,
                    caption="✅ Contact QR তৈরি হয়েছে!",
                )

            with open(output_path, "rb") as image:
                await update.message.reply_document(
                    document=image,
                    filename="contact_qr.png",
                )

        except Exception as error:
            await update.message.reply_text(
                f"❌ Contact QR তৈরি করা যায়নি:\n{error}"
            )

        finally:
            if "folder" in locals():
                cleanup_temp_folder(folder)

            context.user_data.clear()

        return

    # ========================================================
    # EMAIL
    # ========================================================

    if action == "qr_email":
        parts = [
            part.strip()
            for part in text.split("|")
        ]

        if not parts or not parts[0]:
            await update.message.reply_text(
                "❌ Email address দিতে হবে।"
            )
            return

        email = parts[0]
        subject = parts[1] if len(parts) >= 2 else ""
        message = parts[2] if len(parts) >= 3 else ""

        if "@" not in email:
            await update.message.reply_text(
                "❌ Valid email address দাও।"
            )
            return

        try:
            folder = create_temp_dir()

            output_path = os.path.join(
                folder,
                "email_qr.png",
            )

            generate_qr_email(
                email,
                subject,
                message,
                output_path,
            )

            with open(output_path, "rb") as image:
                await update.message.reply_photo(
                    photo=image,
                    caption="✅ Email QR তৈরি হয়েছে!",
                )

            with open(output_path, "rb") as image:
                await update.message.reply_document(
                    document=image,
                    filename="email_qr.png",
                )

        except Exception as error:
            await update.message.reply_text(
                f"❌ Email QR তৈরি করা যায়নি:\n{error}"
            )

        finally:
            if "folder" in locals():
                cleanup_temp_folder(folder)

            context.user_data.clear()

        return

    # ========================================================
    # PHONE
    # ========================================================

    if action == "qr_phone":
        phone = text

        if not re.match(
            r"^\+?[0-9][0-9\s\-()]{5,20}$",
            phone,
        ):
            await update.message.reply_text(
                "❌ Valid phone number দাও।"
            )
            return

        try:
            folder = create_temp_dir()

            output_path = os.path.join(
                folder,
                "phone_qr.png",
            )

            generate_qr_phone(
                phone,
                output_path,
            )

            with open(output_path, "rb") as image:
                await update.message.reply_photo(
                    photo=image,
                    caption="✅ Phone QR তৈরি হয়েছে!",
                )

            with open(output_path, "rb") as image:
                await update.message.reply_document(
                    document=image,
                    filename="phone_qr.png",
                )

        except Exception as error:
            await update.message.reply_text(
                f"❌ Phone QR তৈরি করা যায়নি:\n{error}"
            )

        finally:
            if "folder" in locals():
                cleanup_temp_folder(folder)

            context.user_data.clear()

        return


# ============================================================
# QR IMAGE HANDLER
# ============================================================

async def handle_qr_image(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    action = context.user_data.get("qr_action")

    if action not in (
        "qr_scan",
        "qr_to_pdf",
    ):
        return

    photo = None

    if update.message.photo:
        photo = update.message.photo[-1]

    elif update.message.document:
        document = update.message.document

        filename = document.file_name or ""

        if (
            filename.lower().endswith(
                (".jpg", ".jpeg", ".png", ".webp")
            )
        ):
            folder = create_temp_dir()

            try:
                file_path = os.path.join(
                    folder,
                    filename,
                )

                telegram_file = await document.get_file()

                await telegram_file.download_to_drive(
                    file_path
                )

                await process_qr_image(
                    update,
                    context,
                    file_path,
                    action,
                    folder,
                )

            except Exception as error:
                cleanup_temp_folder(folder)

                await update.message.reply_text(
                    f"❌ Image process করা যায়নি:\n{error}"
                )

            return

    if not photo:
        await update.message.reply_text(
            "⚠️ একটি QR image পাঠাও।"
        )
        return

    folder = create_temp_dir()

    try:
        image_path = os.path.join(
            folder,
            "qr_input.jpg",
        )

        telegram_file = await photo.get_file()

        await telegram_file.download_to_drive(
            image_path
        )

        await process_qr_image(
            update,
            context,
            image_path,
            action,
            folder,
        )

    except Exception as error:
        cleanup_temp_folder(folder)

        await update.message.reply_text(
            f"❌ Image process করা যায়নি:\n{error}"
        )


# ============================================================
# PROCESS QR IMAGE
# ============================================================

async def process_qr_image(
    update,
    context,
    image_path,
    action,
    folder,
):
    try:
        # ====================================================
        # SCAN QR
        # ====================================================

        if action == "qr_scan":
            result = scan_qr(image_path)

            if not result:
                await update.message.reply_text(
                    "❌ কোনো QR code পাওয়া যায়নি।"
                )
                return

            if isinstance(result, list):
                text = "\n\n".join(
                    str(item)
                    for item in result
                )
            else:
                text = str(result)

            await update.message.reply_text(
                f"✅ QR Scan Result:\n\n{text}"
            )

            return

        # ====================================================
        # QR → PDF
        # ====================================================

        if action == "qr_to_pdf":
            from reportlab.lib.utils import ImageReader
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas

            output_path = os.path.join(
                folder,
                "qr.pdf",
            )

            page_width, page_height = A4

            pdf = canvas.Canvas(
                output_path,
                pagesize=A4,
            )

            image = ImageReader(image_path)

            image_width, image_height = (
                image.getSize()
            )

            margin = 40

            max_width = (
                page_width - 2 * margin
            )

            max_height = (
                page_height - 2 * margin
            )

            scale = min(
                max_width / image_width,
                max_height / image_height,
            )

            draw_width = image_width * scale
            draw_height = image_height * scale

            x = (
                page_width - draw_width
            ) / 2

            y = (
                page_height - draw_height
            ) / 2

            pdf.drawImage(
                image,
                x,
                y,
                width=draw_width,
                height=draw_height,
                preserveAspectRatio=True,
            )

            pdf.save()

            with open(output_path, "rb") as pdf_file:
                await update.message.reply_document(
                    document=pdf_file,
                    filename="qr.pdf",
                    caption="✅ QR image → PDF complete!",
                )

    except Exception as error:
        await update.message.reply_text(
            f"❌ QR process failed:\n{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()
