import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
WEBAPP_URL = os.getenv("WEBAPP_URL", "").strip()

ADMIN_IDS = set()

for value in os.getenv("ADMIN_IDS", "").split(","):
    value = value.strip()
    if value.isdigit():
        ADMIN_IDS.add(int(value))


APP_NAME = "Cracker World"
APP_VERSION = "1.0.0"


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS
