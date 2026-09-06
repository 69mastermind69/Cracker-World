import os
import urllib.parse

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from services.qr_service import (
    generate_qr_text,
    generate_qr_url,
    generate_qr_wifi,
    generate_qr_contact,
    generate_qr_email,
    generate_qr_phone,
    generate_qr,
)
from services.qr_scanner import scan_qr
from utils.files import create_temp_dir, cleanup_temp_folder


def qr_done_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🏠 Home",
                callback_data="home",
            )
        ]
    ])


async def _start_qr(
    update,
    context,
    action,
    message,
):
    context.user_data.clear()
    context.user_data["qr_action"] = action

    query = update.callback_query

    await query.answer()
    await query.edit_message_text(
        message,
        parse_mode="HTML",
    )


async def start_qr_text(update, context):
    await _start_qr(
        update,
        context,
        "text",
        "📝 <b>Text → QR</b>\n\n"
        "যে text QR করতে চাও সেটা পাঠাও।",
    )


async def start_qr_url(update, context):
    await _start_qr(
        update,
        context,
        "url",
        "🌐 <b>URL → QR</b>\n\n"
        "একটি URL পাঠাও।",
    )


async def start_qr_wifi(update, context):
    await _start_qr(
        update,
        context,
        "wifi",
        "📶 <b>Wi-Fi → QR</b>\n\n"
        "এই format-এ পাঠাও:\n"
        "<code>SSID | PASSWORD</code>\n\n"
        "Example:\n"
        "<code>MyWiFi | 12345678</code>",
    )


async def start_qr_contact(update, context):
    await _start_qr(
        update,
        context,
        "contact",
        "👤 <b>Contact → QR</b>\n\n"
        "এই format-এ পাঠাও:\n"
        "<code>Name | Phone | Email</code>\n\n"
        "Email optional।",
    )


async def start_qr_email(update, context):
    await _start_qr(
        update,
        context,
        "email",
        "📧 <b>Email → QR</b>\n\n"
        "এই format-এ পাঠাও:\n"
        "<code>Email | Subject | Message</code>\n\n"
        "Subject ও Message optional।",
    )


async def start_qr_phone(update, context):
    await _start_qr(
        update,
        context,
        "phone",
        "📱 <b>Phone → QR</b>\n\n"
        "একটি phone number পাঠাও।",
    )


async def start_qr_scan(update, context):
    context.user_data.clear()
    context.user_data["qr_action"] = "qr_scan"

    query = update.callback_query

    await query.answer()
    await query.edit_message_text(
        "🔍 <b>Scan QR</b>\n\n"
        "QR code থাকা একটি image পাঠাও।",
        parse_mode="HTML",
    )


async def start_qr_to_pdf(update, context):
    context.user_data.clear()
    context.user_data["qr_action"] = "qr_to_pdf"

    query = update.callback_query

    await query.answer()
    await query.edit_message_text(
        "📄 <b>QR → PDF</b>\n\n"
        "QR code থাকা একটি image পাঠাও।",
        parse_mode="HTML",
    )


def _safe_url(value):
    value = value.strip()

    if not value:
        raise ValueError(
            "URL cannot be empty."
        )

    parsed = urllib.parse.urlparse(value)

    if parsed.scheme not in {
        "http",
        "https",
    }:
        value = "https://" + value

    return value


async def _send_qr(
    update,
    context,
    generator,
    *args,
    **kwargs,
):
    folder = create_temp_dir()

    try:
        output_path = os.path.join(
            folder,
            "qr.png",
        )

        generator(
            *args,
            output_path=output_path,
            **kwargs,
        )

        with open(
            output_path,
            "rb",
        ) as file:
            await update.message.reply_photo(
                photo=file,
                caption="✅ QR code তৈরি হয়েছে!",
            )

    except Exception as error:
        await update.message.reply_text(
            f"❌ QR তৈরি করা যায়নি:\n{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()


async def handle_qr_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    data = context.user_data
    action = data.get("qr_action")

    if not action:
        return

    text = (
        update.message.text or ""
    ).strip()

    if not text:
        await update.message.reply_text(
            "⚠️ Empty text পাঠানো যাবে না।"
        )
        return

    try:
        if action == "text":
            await _send_qr(
                update,
                context,
                generate_qr_text,
                text,
            )
            return

        if action == "url":
            url = _safe_url(text)

            await _send_qr(
                update,
                context,
                generate_qr_url,
                url,
            )
            return

        if action == "wifi":
            parts = [
                item.strip()
                for item in text.split("|")
            ]

            if len(parts) < 2:
                raise ValueError(
                    "SSID এবং password দুটোই দিতে হবে।"
                )

            ssid = parts[0]
            password = parts[1]

            await _send_qr(
                update,
                context,
                generate_qr_wifi,
                ssid,
                password,
            )
            return

        if action == "contact":
            parts = [
                item.strip()
                for item in text.split("|")
            ]

            if len(parts) < 2:
                raise ValueError(
                    "Name এবং phone দিতে হবে।"
                )

            name = parts[0]
            phone = parts[1]
            email = (
                parts[2]
                if len(parts) > 2
                else ""
            )

            await _send_qr(
                update,
                context,
                generate_qr_contact,
                name,
                phone,
                email,
            )
            return

        if action == "email":
            parts = [
                item.strip()
                for item in text.split("|")
            ]

            email = parts[0]

            if not email:
                raise ValueError(
                    "Email address দিতে হবে।"
                )

            subject = (
                parts[1]
                if len(parts) > 1
                else ""
            )

            message = (
                parts[2]
                if len(parts) > 2
                else ""
            )

            await _send_qr(
                update,
                context,
                generate_qr_email,
                email,
                subject,
                message,
            )
            return

        if action == "phone":
            await _send_qr(
                update,
                context,
                generate_qr_phone,
                text,
            )
            return

        await update.message.reply_text(
            "ℹ️ Unknown QR action."
        )

    except Exception as error:
        await update.message.reply_text(
            f"❌ QR তৈরি করা যায়নি:\n{error}"
        )


async def handle_qr_image(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    data = context.user_data
    action = data.get("qr_action")

    if action not in {
        "qr_scan",
        "qr_to_pdf",
    }:
        return

    photo = None

    if update.message.photo:
        photo = update.message.photo[-1]

    elif update.message.document:
        document = update.message.document

        filename = (
            document.file_name or ""
        ).lower()

        mime = (
            document.mime_type or ""
        ).lower()

        if (
            mime.startswith("image/")
            or filename.endswith(
                (
                    ".jpg",
                    ".jpeg",
                    ".png",
                    ".webp",
                    ".bmp",
                )
            )
        ):
            folder = create_temp_dir()

            try:
                input_path = os.path.join(
                    folder,
                    "qr_input",
                )

                telegram_file = (
                    await document.get_file()
                )

                await telegram_file.download_to_drive(
                    input_path
                )

                await _process_qr_image(
                    update,
                    context,
                    input_path,
                    folder,
                    action,
                )

            except Exception as error:
                await update.message.reply_text(
                    f"❌ Image process করা যায়নি:\n{error}"
                )

            return

        await update.message.reply_text(
            "⚠️ একটি image পাঠাও।"
        )
        return

    if not photo:
        await update.message.reply_text(
            "⚠️ একটি image পাঠাও।"
        )
        return

    folder = create_temp_dir()

    try:
        input_path = os.path.join(
            folder,
            "qr_input.jpg",
        )

        telegram_file = (
            await photo.get_file()
        )

        await telegram_file.download_to_drive(
            input_path
        )

        await _process_qr_image(
            update,
            context,
            input_path,
            folder,
            action,
        )

    except Exception as error:
        await update.message.reply_text(
            f"❌ Image process করা যায়নি:\n{error}"
        )


async def _process_qr_image(
    update,
    context,
    input_path,
    folder,
    action,
):
    try:
        results = scan_qr(input_path)

        if not results:
            await update.message.reply_text(
                "❌ কোনো QR code পাওয়া যায়নি।"
            )
            return

        if action == "qr_scan":
            lines = [
                f"🔳 <b>QR {index}</b>\n"
                f"<code>{value}</code>"
                for index, value
                in enumerate(
                    results,
                    start=1,
                )
            ]

            await update.message.reply_text(
                "\n\n".join(lines),
                parse_mode="HTML",
            )
            return

        if action == "qr_to_pdf":
            pdf_path = os.path.join(
                folder,
                "qr_result.pdf",
            )

            # Create a PDF containing
            # the decoded QR information.
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas

            pdf = canvas.Canvas(
                pdf_path,
                pagesize=A4,
            )

            width, height = A4
            y = height - 60

            pdf.setFont(
                "Helvetica-Bold",
                14,
            )

            pdf.drawString(
                50,
                y,
                "QR Code Result",
            )

            y -= 35

            pdf.setFont(
                "Helvetica",
                10,
            )

            for index, value in enumerate(
                results,
                start=1,
            ):
                text = (
                    f"QR {index}: {value}"
                )

                # Basic wrapping.
                max_chars = 90

                chunks = [
                    text[i:i + max_chars]
                    for i in range(
                        0,
                        len(text),
                        max_chars,
                    )
                ]

                for chunk in chunks:
                    if y < 50:
                        pdf.showPage()
                        y = height - 60
                        pdf.setFont(
                            "Helvetica",
                            10,
                        )

                    pdf.drawString(
                        50,
                        y,
                        chunk,
                    )

                    y -= 16

                y -= 8

            pdf.save()

            with open(
                pdf_path,
                "rb",
            ) as file:
                await update.message.reply_document(
                    document=file,
                    filename="qr_result.pdf",
                    caption="📄 QR → PDF complete!",
                )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()
