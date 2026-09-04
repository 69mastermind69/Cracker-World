```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .tools import TOOLS as OLD_TOOLS
from .free_tools import FREE_TOOLS


# =========================================================
# ALL TOOLS
# =========================================================

TOOLS = {
    **OLD_TOOLS,
    **FREE_TOOLS,
}


# =========================================================
# TOOL CATEGORIES
# =========================================================

CATEGORIES = {

    # -----------------------------------------------------
    # EXISTING CATEGORIES
    # -----------------------------------------------------

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

        # New free/offline hash & encoding tools
        "base32",
        "base32decode",
        "base16",
        "base16decode",
        "urlcomponent",
        "urlcomponentdecode",
        "htmlescape2",
        "htmlunescape2",
        "codepoints",
        "unicodechars",
        "sha3_224",
        "sha3_256",
        "sha3_384",
        "sha3_512",
        "blake2b",
        "blake2s",
        "crc32",
    ],

    "🧑‍💻 Developer": [
        "regex",
        "findall",
        "htmlescape",
        "htmlunescape",
        "jsonescape",
        "jsonunescape",
        "pyrepr",
        "pyliteral",
        "queryencode",
        "querydecode",
        "nowts",
        "tstodate",
        "datetots",
        "hextorgb",
        "rgbtohex",
        "csvsplit",
    ],

    "📊 JSON & Data": [
        "json",
        "jsonmin",
        "jsoncheck",

        # New free/offline data tools
        "jsonsort",
        "jsoncompact",
        "jsontype",
        "jsonkeys",
        "jsonlength",
        "csvjson",
        "csvcolumns",
    ],

    "🎲 Random": [
        "random",
        "choose",

        # New free/offline random tools
        "coin",
        "dice",
        "dices",
        "randomletter",
        "randomlower",
        "randomupper",
        "randomdigit",
        "randomcolor",
        "randomhex",
        "uuidshort",
        "randombool",
    ],

    "🆔 Generators": [
        "uuid",
        "uuids",
        "password",

        # New harmless generators
        "uuidshort",
    ],

    "📅 Date": [
        "datediff",
        "adddays",

        # New free/offline date tools
        "today",
        "datetime",
        "year",
        "month",
        "day",
        "weekday",
        "leap",
        "monthdays",
        "addhours",
        "addminutes",
    ],

    # -----------------------------------------------------
    # NEW FREE CATEGORIES
    # -----------------------------------------------------

    "🆓 Free Text": [
        "textlen",
        "wordcount2",
        "vowels",
        "consonants",
        "digitcount",
        "spacecount",
        "punctcount",
        "uppercount",
        "lowercount",
        "capitalize",
        "swapcase",
        "center",
        "wrap",
        "duplicatewords",
        "uniquewords",
        "reversewords",
        "sortwords",
        "alphabetical",
        "wordfreq",
        "longestword",
        "shortestword",
        "palindrome",
        "isogram",
        "anagram",
        "removevowels",
        "removeconsonants",
        "alphanumeric",
        "keepascii",
        "nonascii",
        "normalizenewline",
        "tabspace",
        "spacetab",
        "collapselines",
        "reverselines",
        "sortuniquelines",
        "linelengths",
    ],

    "🔢 Free Numbers": [
        "decbinary",
        "decoctal",
        "dechex",
        "bindec",
        "octdec",
        "hexdec",
        "binhex",
        "hexbin",
        "digitsum",
        "root",
        "factors",
        "primefactors",
        "lcm2",
        "gcd2",
        "distance",
        "percentchange",
        "proportion",
        "mean2",
        "median2",
        "mode2",
        "variance",
        "stdev",
        "percentageof",
        "addnums",
        "mulnums",
    ],

    "📅 Free Date & Time": [
        "today",
        "datetime",
        "year",
        "month",
        "day",
        "weekday",
        "leap",
        "monthdays",
        "addhours",
        "addminutes",
    ],

    "🎨 Free Color": [
        "rgbtohsl",
        "hsltorgb",
    ],
}


# =========================================================
# MAIN TOOLS KEYBOARD
# =========================================================

def tools_keyboard():
    keyboard = []

    for category_name in CATEGORIES:

        # Only show category if it contains
        # at least one currently registered tool.
        valid_tools = [
            tool_id
            for tool_id in CATEGORIES[category_name]
            if tool_id in TOOLS
        ]

        if not valid_tools:
            continue

        keyboard.append([
            InlineKeyboardButton(
                text=category_name,
                callback_data=f"category:{category_name}"
            )
        ])

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# CATEGORY KEYBOARD
# =========================================================

def category_keyboard(category_name):

    tool_ids = CATEGORIES.get(
        category_name,
        []
    )

    keyboard = []
    row = []

    for tool_id in tool_ids:

        # Skip tools that aren't registered.
        if tool_id not in TOOLS:
            continue

        tool_name = TOOLS[tool_id][0]

        row.append(
            InlineKeyboardButton(
                text=tool_name,
                callback_data=f"tool:{tool_id}"
            )
        )

        # Two buttons per row.
        if len(row) == 2:
            keyboard.append(row)
            row = []

    # Add remaining button.
    if row:
        keyboard.append(row)

    # Back button.
    keyboard.append([
        InlineKeyboardButton(
            text="⬅️ Back",
            callback_data="back:tools"
        )
    ])

    return InlineKeyboardMarkup(keyboard)
```
