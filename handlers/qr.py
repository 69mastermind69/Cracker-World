import os
import re

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import ContextTypes

from services.qr_service import (
    text_to_qr,
    url_to_qr,
    phone_to_qr,
    email_to_qr,
    wifi_to_qr,
    contact_to_qr,
    qr_to_pdf,
)

from services.qr_scanner import scan_qr

from utils.files import (
    create_temp_dir,
    cleanup_temp_folder,
)


def qr_back_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="qr_menu",
            )
        ]
    ])


async def start_qr_text(update, context):
    context.user_data.clear()
    context.user_data["qr_action"] = "text"

    await update.callback_query.message.reply_text(
        "📝 Text → QR\n\n"
        "যে text-এর QR বানাতে চাও সেটি পাঠাও।"
    )


async def start_qr_url(update, context):
    context.user_data.clear()
    context.user_data["qr_action"] = "url"

    await update.callback_query.message.reply_text(
        "🌐 URL → QR\n\n"
        "একটি URL পাঠাও।\n\n"
        "উদাহরণ:\n"
        "https://example.com"
    )


async def start_qr_phone(update, context):
    context.user_data.clear()
    context.user_data["qr_action"] = "phone"

    await update.callback_query.message.reply_text(
        "📱 Phone → QR\n\n"
        "একটি phone number পাঠাও।"
    )


async def start_qr_email(update, context):
    context.user_data.clear()
    context.user_data["qr_action"] = "email"

    await update.callback_query.message.reply_text(
        "📧 Email → QR\n\n"
        "একটি email address পাঠাও।"
    )


async def start_qr_wifi(update, context):
    context.user_data.clear()
    context.user_data["qr_action"] = "wifi"

    await update.callback_query.message.reply_text(
        "📶 Wi-Fi → QR\n\n"
        "এই format-এ পাঠাও:\n\n"
        "SSID | PASSWORD\n\n"
        "উদাহরণ:\n"
        "MyWiFi | 12345678"
    )


async def start_qr_contact(update, context):
    context.user_data.clear()
    context.user_data["qr_action"] = "contact"

    await update.callback_query.message.reply_text(
        "👤 Contact → QR\n\n"
        "এই format-এ পাঠাও:\n\n"
        "Name | Phone | Email\n\n"
        "উদাহরণ:\n"
        "John Doe | 01700000000 | john@example.com"
    )


async def start_qr_to_pdf(update, context):
    context.user_data.clear()
    context.user_data["qr_action"] = "qr_to_pdf"

    await update.callback_query.message.reply_text(
        "📄 QR → PDF\n\n"
        "প্রথমে একটি QR image পাঠাও।"
    )


async def start_qr_scan(update, context):
    context.user_data.clear()
    context.user_data["qr_action"] = "qr_scan"

    await update.callback_query.message.reply_text(
        "🔍 QR Scanner\n\n"
        "একটি QR code-এর image পাঠাও।\n\n"
        "একাধিক QR থাকলেও bot detect করার চেষ্টা করবে।"
    )


async def create_and_send_qr(
    update,
    context,
    creator,
    data_args,
):
    folder = create_temp_dir()
    output_path = os.path.join(
        folder,
        "qr.png",
    )

    try:
        creator(
            *data_args,
            output_path,
        )

        with open(output_path, "rb") as qr_file:
            await update.message.reply_document(
                document=qr_file,
                filename="qr.png",
                caption="✅ QR code তৈরি হয়েছে!",
            )

    except Exception as error:
        await update.message.reply_text(
            "❌ QR তৈরি করা যায়নি:\n"
            f"{error}"
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

    action = context.user_data.get("qr_action")

    if not action:
        return

    text = update.message.text.strip()

    if not text:
        await update.message.reply_text(
            "⚠️ খালি text দেওয়া যাবে না।"
        )
        return

    if action == "text":
        await create_and_send_qr(
            update,
            context,
            text_to_qr,
            [text],
        )
        return

    if action == "url":
        if not (
            text.startswith("http://")
            or text.startswith("https://")
        ):
            await update.message.reply_text(
                "⚠️ সঠিক URL পাঠাও।\n\n"
                "উদাহরণ:\n"
                "https://example.com"
            )
            return

        await create_and_send_qr(
            update,
            context,
            url_to_qr,
            [text],
        )
        return

    if action == "phone":
        await create_and_send_qr(
            update,
            context,
            phone_to_qr,
            [text],
        )
        return

    if action == "email":
        if not re.match(
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
            text,
        ):
            await update.message.reply_text(
                "⚠️ সঠিক email address পাঠাও।"
            )
            return

        await create_and_send_qr(
            update,
            context,
            email_to_qr,
            [text],
        )
        return

    if action == "wifi":
        parts = [
            item.strip()
            for item in text.split("|")
        ]

        if len(parts) < 2:
            await update.message.reply_text(
                "⚠️ Format ঠিক রাখো:\n\n"
                "SSID | PASSWORD"
            )
            return

        ssid = parts[0]
        password = parts[1]

        folder = create_temp_dir()
        output_path = os.path.join(
            folder,
            "wifi_qr.png",
        )

        try:
            wifi_to_qr(
                ssid,
                password,
                "WPA",
                False,
                output_path,
            )

            with open(
                output_path,
                "rb",
            ) as qr_file:
                await update.message.reply_document(
                    document=qr_file,
                    filename="wifi_qr.png",
                    caption="✅ Wi-Fi QR তৈরি হয়েছে!",
                )

        except Exception as error:
            await update.message.reply_text(
                "❌ Wi-Fi QR তৈরি করা যায়নি:\n"
                f"{error}"
            )

        finally:
            cleanup_temp_folder(folder)
            context.user_data.clear()

        return

    if action == "contact":
        parts = [
            item.strip()
            for item in text.split("|")
        ]

        if not parts or not parts[0]:
            await update.message.reply_text(
                "⚠️ Contact name দিতে হবে।"
            )
            return

        name = parts[0]
        phone = parts[1] if len(parts) > 1 else ""
        email = parts[2] if len(parts) > 2 else ""

        folder = create_temp_dir()
        output_path = os.path.join(
            folder,
            "contact_qr.png",
        )

        try:
            contact_to_qr(
                name,
                phone,
                email,
                "",
                output_path,
            )

            with open(
                output_path,
                "rb",
            ) as qr_file:
                await update.message.reply_document(
                    document=qr_file,
                    filename="contact_qr.png",
                    caption="✅ Contact QR তৈরি হয়েছে!",
                )

        except Exception as error:
            await update.message.reply_text(
                "❌ Contact QR তৈরি করা যায়নি:\n"
                f"{error}"
            )

        finally:
            cleanup_temp_folder(folder)
            context.user_data.clear()

        return


async def handle_qr_image(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    action = context.user_data.get("qr_action")

    if action not in (
        "qr_to_pdf",
        "qr_scan",
    ):
        return

    if not update.message.photo:
        return

    folder = create_temp_dir()

    image_path = os.path.join(
        folder,
        "input.jpg",
    )

    try:
        photo = update.message.photo[-1]

        telegram_file = await photo.get_file()

        await telegram_file.download_to_drive(
            image_path
        )

        if action == "qr_scan":
            results = scan_qr(image_path)

            if not results:
                await update.message.reply_text(
                    "❌ কোনো QR code পাওয়া যায়নি।\n\n"
                    "আরেকটি পরিষ্কার QR image পাঠিয়ে চেষ্টা করো।",
                    reply_markup=qr_back_keyboard(),
                )
                return

            message = (
                f"✅ {len(results)}টি QR code পাওয়া গেছে!\n\n"
            )

            for index, result in enumerate(
                results,
                start=1,
            ):
                message += (
                    f"🔳 QR #{index}\n"
                    f"{result}\n\n"
                )

            await update.message.reply_text(
                message,
                reply_markup=qr_back_keyboard(),
            )

            return

        output_path = os.path.join(
            folder,
            "qr.pdf",
        )

        qr_to_pdf(
            image_path,
            output_path,
        )

        with open(
            output_path,
            "rb",
        ) as pdf_file:
            await update.message.reply_document(
                document=pdf_file,
                filename="qr.pdf",
                caption="✅ QR image → PDF হয়েছে!",
            )

    except Exception as error:
        await update.message.reply_text(
            "❌ QR process করা যায়নি:\n"
            f"{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()
