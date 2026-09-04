from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .tools import TOOLS


CATEGORIES = {
    "🧮 Math": [
        "calc",
        "percent",
        "average",
        "minmax",
        "evenodd",
        "prime",
        "gcd",
        "lcm",
        "factorial",
        "fibonacci",
        "tobinary",
        "frombinary",
        "tohex",
        "fromhex",
        "square",
        "cube",
        "sqrt",
        "power",
        "abs",
        "round",
        "sum",
        "product",
        "median",
        "range",
    ],

    "🔤 Text": [
        "upper",
        "lower",
        "title",
        "sentence",
        "reverse",
        "spaces",
        "emptylines",
        "numberlines",
        "count",
        "chars",
        "lines",
        "stats",
        "dedupe",
        "sortlines",
        "trim",
        "nodigits",
        "nopunctuation",
        "digits",
        "letters",
        "altcase",
        "repeat",
    ],

    "🔐 Hash & Encoding": [
        "ascii",
        "asciidecode",
        "binary",
        "binarydecode",
        "hex",
        "hexdecode",
        "rot13",
        "base64",
        "base64decode",
        "urlencode",
        "urldecode",
        "md5",
        "sha1",
        "sha224",
        "sha256",
        "sha384",
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


def tools_keyboard():
    keyboard = []

    for category_name in CATEGORIES:
        keyboard.append([
            InlineKeyboardButton(
                text=category_name,
                callback_data=f"category:{category_name}"
            )
        ])

    return InlineKeyboardMarkup(keyboard)


def category_keyboard(category_name):
    tool_ids = CATEGORIES.get(category_name, [])

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
