import os


BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

DEVELOPER_NAME = os.getenv("DEVELOPER_NAME", "Your Name")
DEVELOPER_USERNAME = os.getenv("DEVELOPER_USERNAME", "@yourusername")
DEVELOPER_CHANNEL = os.getenv("DEVELOPER_CHANNEL", "")


# Temporary file settings
MAX_FILE_SIZE_MB = 20
TEMP_DIR = "/tmp/telegram_bot"

# Bot settings
BOT_NAME = "All-in-One Telegram Bot"
MAINTENANCE_MODE = False
