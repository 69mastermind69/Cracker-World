import os
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)


# =========================================================
# CONFIG
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

DEVELOPER_NAME = os.getenv("DEVELOPER_NAME", "Your Name")
DEVELOPER_USERNAME = os.getenv("DEVELOPER_USERNAME", "@yourusername")
DEVELOPER_CHANNEL = os.getenv("DEVELOPER_CHANNEL", "")


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# =========================================================
# START
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    text = (
        f"👋 Hello {user.first_name}!\n\n"
        "🤖 Welcome to our All-in-One Utility Bot.\n\n"
        "Choose a category below:"
    )

    await update.effective_message.reply_text(
        text,
        reply_markup=main_menu(),
    )


# =========================================================
# MAIN MENU
# =========================================================

def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("📄 PDF Tools", callback_data="pdf_menu"),
            InlineKeyboardButton("🖼️ Image Tools", callback_data="image_menu"),
        ],
        [
            InlineKeyboardButton("🔳 QR Tools", callback_data="qr_menu"),
            InlineKeyboardButton("🎙️ Audio Tools", callback_data="audio_menu"),
        ],
        [
            InlineKeyboardButton("🛠️ File Tools", callback_data="file_menu"),
        ],
        [
            InlineKeyboardButton("👨‍💻 Developer", callback_data="developer"),
            InlineKeyboardButton("ℹ️ Help", callback_data="help"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# PDF MENU
# =========================================================

def pdf_menu():
    keyboard = [
        [
            InlineKeyboardButton(
                "📝 Text → PDF",
                callback_data="text_to_pdf",
            )
        ],
        [
            InlineKeyboardButton(
                "🖼️ Image → PDF",
                callback_data="image_to_pdf",
            )
        ],
        [
            InlineKeyboardButton(
                "🔗 Merge PDF",
                callback_data="merge_pdf",
            ),
            InlineKeyboardButton(
                "✂️ Split PDF",
                callback_data="split_pdf",
            ),
        ],
        [
            InlineKeyboardButton(
                "🖼️ PDF → Image",
                callback_data="pdf_to_image",
            ),
            InlineKeyboardButton(
                "📝 PDF → Text",
                callback_data="pdf_to_text",
            ),
        ],
        [
            InlineKeyboardButton(
                "🔐 Protect PDF",
                callback_data="protect_pdf",
            )
        ],
        [
            InlineKeyboardButton("⬅️ Back", callback_data="home"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# IMAGE MENU
# =========================================================

def image_menu():
    keyboard = [
        [
            InlineKeyboardButton(
                "📐 Resize Image",
                callback_data="resize_image",
            )
        ],
        [
            InlineKeyboardButton(
                "🗜️ Compress Image",
                callback_data="compress_image",
            )
        ],
        [
            InlineKeyboardButton(
                "🔄 Convert Image",
                callback_data="convert_image",
            )
        ],
        [
            InlineKeyboardButton(
                "🖼️ Image → PDF",
                callback_data="image_to_pdf",
            )
        ],
        [
            InlineKeyboardButton(
                "ℹ️ Image Info",
                callback_data="image_info",
            )
        ],
        [
            InlineKeyboardButton("⬅️ Back", callback_data="home"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# QR MENU
# =========================================================

def qr_menu():
    keyboard = [
        [
            InlineKeyboardButton(
                "📝 Text → QR",
                callback_data="qr_text",
            ),
            InlineKeyboardButton(
                "🔗 URL → QR",
                callback_data="qr_url",
            ),
        ],
        [
            InlineKeyboardButton(
                "📶 WiFi → QR",
                callback_data="qr_wifi",
            ),
            InlineKeyboardButton(
                "👤 Contact → QR",
                callback_data="qr_contact",
            ),
        ],
        [
            InlineKeyboardButton(
                "📧 Email → QR",
                callback_data="qr_email",
            ),
            InlineKeyboardButton(
                "📞 Phone → QR",
                callback_data="qr_phone",
            ),
        ],
        [
            InlineKeyboardButton(
                "📷 Scan QR",
                callback_data="qr_scan",
            )
        ],
        [
            InlineKeyboardButton(
                "📄 QR → PDF",
                callback_data="qr_to_pdf",
            )
        ],
        [
            InlineKeyboardButton("⬅️ Back", callback_data="home"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# AUDIO MENU
# =========================================================

def audio_menu():
    keyboard = [
        [
            InlineKeyboardButton(
                "🔊 Text → Voice",
                callback_data="text_to_voice",
            )
        ],
        [
            InlineKeyboardButton(
                "🎚️ Voice Changer",
                callback_data="voice_changer",
            )
        ],
        [
            InlineKeyboardButton(
                "✂️ Audio Cutter",
                callback_data="audio_cutter",
            )
        ],
        [
            InlineKeyboardButton(
                "🔄 Audio Converter",
                callback_data="audio_converter",
            )
        ],
        [
            InlineKeyboardButton(
                "🔉 Volume Changer",
                callback_data="volume_changer",
            )
        ],
        [
            InlineKeyboardButton(
                "ℹ️ Audio Info",
                callback_data="audio_info",
            )
        ],
        [
            InlineKeyboardButton("⬅️ Back", callback_data="home"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# FILE MENU
# =========================================================

def file_menu():
    keyboard = [
        [
            InlineKeyboardButton(
                "📦 Create ZIP",
                callback_data="create_zip",
            ),
            InlineKeyboardButton(
                "📂 Extract ZIP",
                callback_data="extract_zip",
            ),
        ],
        [
            InlineKeyboardButton(
                "🔄 File Converter",
                callback_data="file_converter",
            )
        ],
        [
            InlineKeyboardButton(
                "ℹ️ File Info",
                callback_data="file_info",
            )
        ],
        [
            InlineKeyboardButton("⬅️ Back", callback_data="home"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# DEVELOPER MENU
# =========================================================

def developer_menu():
    keyboard = []

    if DEVELOPER_USERNAME:
        keyboard.append(
            [
                InlineKeyboardButton(
                    "💬 Contact Developer",
                    url=f"https://t.me/{DEVELOPER_USERNAME.lstrip('@')}",
                )
            ]
        )

    if DEVELOPER_CHANNEL:
        keyboard.append(
            [
                InlineKeyboardButton(
                    "📢 Developer Channel",
                    url=DEVELOPER_CHANNEL,
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton("⬅️ Back", callback_data="home"),
        ]
    )

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# ADMIN MENU
# =========================================================

def admin_menu():
    keyboard = [
        [
            InlineKeyboardButton(
                "📊 Statistics",
                callback_data="admin_stats",
            )
        ],
        [
            InlineKeyboardButton(
                "👥 Users",
                callback_data="admin_users",
            )
        ],
        [
            InlineKeyboardButton(
                "📢 Broadcast",
                callback_data="admin_broadcast",
            )
        ],
        [
            InlineKeyboardButton(
                "🚫 Ban User",
                callback_data="admin_ban",
            ),
            InlineKeyboardButton(
                "✅ Unban User",
                callback_data="admin_unban",
            ),
        ],
        [
            InlineKeyboardButton(
                "🛠️ Maintenance",
                callback_data="admin_maintenance",
            )
        ],
        [
            InlineKeyboardButton(
                "⬅️ Back",
                callback_data="home",
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# BUTTON HANDLER
# =========================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query

    await query.answer()

    data = query.data

    # -------------------------
    # MAIN NAVIGATION
    # -------------------------

    if data == "home":
        await query.edit_message_text(
            "🏠 Main Menu\n\nChoose a category:",
            reply_markup=main_menu(),
        )
        return

    if data == "pdf_menu":
        await query.edit_message_text(
            "📄 PDF TOOLS\n\nChoose an option:",
            reply_markup=pdf_menu(),
        )
        return

    if data == "image_menu":
        await query.edit_message_text(
            "🖼️ IMAGE TOOLS\n\nChoose an option:",
            reply_markup=image_menu(),
        )
        return

    if data == "qr_menu":
        await query.edit_message_text(
            "🔳 QR TOOLS\n\nChoose an option:",
            reply_markup=qr_menu(),
        )
        return

    if data == "audio_menu":
        await query.edit_message_text(
            "🎙️ AUDIO TOOLS\n\nChoose an option:",
            reply_markup=audio_menu(),
        )
        return

    if data == "file_menu":
        await query.edit_message_text(
            "🛠️ FILE TOOLS\n\nChoose an option:",
            reply_markup=file_menu(),
        )
        return

    # -------------------------
    # DEVELOPER
    # -------------------------

    if data == "developer":
        text = (
            "👨‍💻 DEVELOPER\n\n"
            f"👤 Name: {DEVELOPER_NAME}\n"
            f"📱 Telegram: {DEVELOPER_USERNAME}\n\n"
            "⚡ All-in-One Utility Bot"
        )

        await query.edit_message_text(
            text,
            reply_markup=developer_menu(),
        )
        return

    # -------------------------
    # HELP
    # -------------------------

    if data == "help":
        text = (
            "ℹ️ HELP\n\n"
            "1️⃣ Select a category.\n"
            "2️⃣ Select the feature you need.\n"
            "3️⃣ Send the required file/text.\n"
            "4️⃣ The bot will process it.\n"
            "5️⃣ You will receive the result.\n\n"
            "🏠 You can always use the Back button "
            "to return to the main menu."
        )

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🏠 Home",
                            callback_data="home",
                        )
                    ]
                ]
            ),
        )
        return

    # -------------------------
    # ADMIN
    # -------------------------

    if data == "admin":
        if query.from_user.id != ADMIN_ID:
            await query.answer(
                "❌ You are not authorized.",
                show_alert=True,
            )
            return

        await query.edit_message_text(
            "👑 ADMIN PANEL\n\nChoose an option:",
            reply_markup=admin_menu(),
        )
        return

    # -------------------------
    # FUTURE FEATURES
    # -------------------------

    feature_names = {
        "text_to_pdf": "📝 Text → PDF",
        "image_to_pdf": "🖼️ Image → PDF",
        "merge_pdf": "🔗 Merge PDF",
        "split_pdf": "✂️ Split PDF",
        "pdf_to_image": "🖼️ PDF → Image",
        "pdf_to_text": "📝 PDF → Text",
        "protect_pdf": "🔐 Protect PDF",
        "resize_image": "📐 Resize Image",
        "compress_image": "🗜️ Compress Image",
        "convert_image": "🔄 Convert Image",
        "image_info": "ℹ️ Image Info",
        "qr_text": "📝 Text → QR",
        "qr_url": "🔗 URL → QR",
        "qr_wifi": "📶 WiFi → QR",
        "qr_contact": "👤 Contact → QR",
        "qr_email": "📧 Email → QR",
        "qr_phone": "📞 Phone → QR",
        "qr_scan": "📷 Scan QR",
        "qr_to_pdf": "📄 QR → PDF",
        "text_to_voice": "🔊 Text → Voice",
        "voice_changer": "🎚️ Voice Changer",
        "audio_cutter": "✂️ Audio Cutter",
        "audio_converter": "🔄 Audio Converter",
        "volume_changer": "🔉 Volume Changer",
        "audio_info": "ℹ️ Audio Info",
        "create_zip": "📦 Create ZIP",
        "extract_zip": "📂 Extract ZIP",
        "file_converter": "🔄 File Converter",
        "file_info": "ℹ️ File Info",
    }

    if data in feature_names:
        await query.edit_message_text(
            f"{feature_names[data]}\n\n"
            "⏳ This feature will be connected in the next step.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "⬅️ Back",
                            callback_data="home",
                        )
                    ]
                ]
            ),
        )
        return

    # -------------------------
    # UNKNOWN CALLBACK
    # -------------------------

    await query.edit_message_text(
        "❌ Unknown option.",
        reply_markup=main_menu(),
    )


# =========================================================
# ADMIN COMMAND
# =========================================================

async def admin_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if update.effective_user.id != ADMIN_ID:
        await update.effective_message.reply_text(
            "❌ You are not authorized."
        )
        return

    await update.effective_message.reply_text(
        "👑 ADMIN PANEL\n\nChoose an option:",
        reply_markup=admin_menu(),
    )


# =========================================================
# ERROR HANDLER
# =========================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):
    logger.error(
        "Exception while handling update:",
        exc_info=context.error,
    )


# =========================================================
# MAIN
# =========================================================

def main():
    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN environment variable is missing."
        )

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # Commands
    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("admin", admin_command)
    )

    # Inline buttons
    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    # Errors
    application.add_error_handler(error_handler)

    logger.info("Bot started successfully.")

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
