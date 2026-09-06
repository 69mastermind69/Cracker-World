import os


BOT_TOKEN = os.getenv("BOT_TOKEN", "")

ADMIN_ID = int(
    os.getenv("ADMIN_ID", "0")
)


# =========================
# DEVELOPER
# =========================

DEVELOPER_NAME = "MASTERMIND"

DEVELOPER_USERNAME = "@Do_x_Die"


# =========================
# FILE SETTINGS
# =========================

MAX_FILE_SIZE_MB = 20

TEMP_DIR = "/tmp/telegram_bot"


# =========================
# BOT SETTINGS
# =========================

BOT_NAME = "All-in-One Telegram Bot"

MAINTENANCE_MODE = False
