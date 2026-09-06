import os


BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

try:
    ADMIN_ID = int(os.getenv("ADMIN_ID", "0").strip() or "0")
except ValueError:
    ADMIN_ID = 0


DEVELOPER_NAME = "MASTERMIND"
DEVELOPER_USERNAME = "@Do_x_Die"

BOT_NAME = "All-in-One Telegram Bot"

MAX_FILE_SIZE_MB = 20
TEMP_DIR = "/tmp/telegram_bot"

MAINTENANCE_MODE = False


def is_admin(user_id: int) -> bool:
    return bool(ADMIN_ID) and user_id == ADMIN_ID
