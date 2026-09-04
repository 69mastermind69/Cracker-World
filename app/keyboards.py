from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .tools import TOOLS


def tools_keyboard():
    keyboard = []

    categories = {
        "🧮 Math": [
            "calc",
            "percent",
            "average",
            "minmax",
        ],
        "🔤 Text": [
            "upper",
            "lower",
            "reverse",
            "count",
            "chars",
            "lines",
            "dedupe",
            "sortlines",
        ],
        "🔐 Hash & Encoding": [
            "b64encode",
            "b64decode",
            "urlencode",
            "urldecode",
            "md5",
            "sha256",
            "sha512",
        ],
        "📊 JSON & Data": [
            "json",
            "jsonmin",
            "jsoncheck",
        ],
        "🎲 Random": [
            "random",
            "choose",
        ],
        "🆔 Generators": [
            "uuid",
            "uuids",
            "password",
        ],
        "📅 Date": [
            "datediff",
            "adddays",
        ],
    }

    for category_name, tool_ids in categories.items():
        keyboard.append([
            InlineKeyboardButton(
                text=category_name,
                callback_data=f"category:{category_name}"
            )
        ])

    return InlineKeyboardMarkup(keyboard)


def category_keyboard(category_name):
    categories = {
        "🧮 Math": [
            "calc",
            "percent",
            "average",
            "minmax",
        ],
        "🔤 Text": [
            "upper",
            "lower",
            "reverse",
            "count",
            "chars",
            "lines",
            "dedupe",
            "sortlines",
        ],
        "🔐 Hash & Encoding": [
            "b64encode",
            "b64decode",
            "urlencode",
            "urldecode",
            "md5",
            "sha256",
            "sha512",
        ],
        "📊 JSON & Data": [
            "json",
            "jsonmin",
            "jsoncheck",
        ],
        "🎲 Random": [
            "random",
            "choose",
        ],
        "🆔 Generators": [
            "uuid",
            "uuids",
            "password",
        ],
        "📅 Date": [
            "datediff",
            "adddays",
        ],
    }

    tool_ids = categories.get(category_name, [])

    keyboard = []
    row = []

    for tool_id in tool_ids:
        if tool_id not in TOOLS:
            continue

        tool_name = TOOLS[tool_id][0]

        row.append(
            InlineKeyboardButton(
                text=tool_name,
                callback_data=f"tool:{tool_id}"
            )
        )

        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    keyboard.append([
        InlineKeyboardButton(
            text="⬅️ Back",
            callback_data="back:tools"
        )
    ])

    return InlineKeyboardMarkup(keyboard)
