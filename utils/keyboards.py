from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu():
    return InlineKeyboardMarkup([
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
    ])


def back_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="home")]
    ])


def pdf_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📝 Text → PDF", callback_data="text_to_pdf"),
            InlineKeyboardButton("🖼️ Image → PDF", callback_data="pdf_image_to_pdf"),
        ],
        [
            InlineKeyboardButton("📚 Merge PDF", callback_data="merge_pdf"),
            InlineKeyboardButton("✂️ Split PDF", callback_data="split_pdf"),
        ],
        [
            InlineKeyboardButton("🖼️ PDF → Image", callback_data="pdf_to_image"),
            InlineKeyboardButton("📄 PDF → Text", callback_data="pdf_to_text"),
        ],
        [
            InlineKeyboardButton("🔐 Protect PDF", callback_data="protect_pdf"),
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="home"),
        ],
    ])


def image_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📐 Resize", callback_data="resize_image"),
            InlineKeyboardButton("🗜️ Compress", callback_data="compress_image"),
        ],
        [
            InlineKeyboardButton("🔄 Convert", callback_data="convert_image"),
            InlineKeyboardButton("📄 Image → PDF", callback_data="image_to_pdf"),
        ],
        [
            InlineKeyboardButton("ℹ️ Image Info", callback_data="image_info"),
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="home"),
        ],
    ])


def qr_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📝 Text → QR", callback_data="qr_text"),
            InlineKeyboardButton("🌐 URL → QR", callback_data="qr_url"),
        ],
        [
            InlineKeyboardButton("📶 Wi-Fi → QR", callback_data="qr_wifi"),
            InlineKeyboardButton("👤 Contact → QR", callback_data="qr_contact"),
        ],
        [
            InlineKeyboardButton("📧 Email → QR", callback_data="qr_email"),
            InlineKeyboardButton("📱 Phone → QR", callback_data="qr_phone"),
        ],
        [
            InlineKeyboardButton("🔍 Scan QR", callback_data="qr_scan"),
            InlineKeyboardButton("📄 QR → PDF", callback_data="qr_to_pdf"),
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="home"),
        ],
    ])


def audio_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🗣️ Text → Voice", callback_data="text_to_voice"),
            InlineKeyboardButton("🎭 Voice Changer", callback_data="voice_changer"),
        ],
        [
            InlineKeyboardButton("✂️ Audio Cutter", callback_data="audio_cutter"),
            InlineKeyboardButton("🔄 Audio Converter", callback_data="audio_converter"),
        ],
        [
            InlineKeyboardButton("🔊 Volume Changer", callback_data="volume_changer"),
            InlineKeyboardButton("ℹ️ Audio Info", callback_data="audio_info"),
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="home"),
        ],
    ])


def file_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🗜️ Create ZIP", callback_data="create_zip"),
            InlineKeyboardButton("📦 Extract ZIP", callback_data="extract_zip"),
        ],
        [
            InlineKeyboardButton("🔄 File Converter", callback_data="file_converter"),
            InlineKeyboardButton("ℹ️ File Info", callback_data="file_info"),
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="home"),
        ],
    ])


def developer_menu(username=""):
    buttons = []

    if username:
        buttons.append([
            InlineKeyboardButton(
                "👨‍💻 Contact Developer",
                url=f"https://t.me/{username.lstrip('@')}",
            )
        ])

    buttons.append([
        InlineKeyboardButton("🔙 Back", callback_data="home")
    ])

    return InlineKeyboardMarkup(buttons)


def help_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="home")]
    ])


def admin_menu():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📊 Statistics", callback_data="admin_stats"),
            InlineKeyboardButton("👥 Users", callback_data="admin_users"),
        ],
        [
            InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast"),
        ],
        [
            InlineKeyboardButton("🚫 Ban User", callback_data="admin_ban"),
            InlineKeyboardButton("✅ Unban User", callback_data="admin_unban"),
        ],
        [
            InlineKeyboardButton("🔧 Maintenance", callback_data="admin_maintenance"),
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="home"),
        ],
    ])
