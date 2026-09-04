
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .tools import TOOLS as OLD_TOOLS
from .free_tools import FREE_TOOLS


# =========================================================
# COMBINED TOOL REGISTRY
# =========================================================

TOOLS = {
    **OLD_TOOLS,
    **FREE_TOOLS,
}


# =========================================================
# CATEGORIES
# =========================================================

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

        # Free Text
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

        # Free Encoding
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

        # Free Hash
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
        "coin",
        "dice",
        "dices",
        "randomletter",
        "randomlower",
        "randomupper",
        "randomdigit",
        "randomcolor",
        "randomhex",
        "randombool",
        "uuidshort",
    ],

    "🆔 Generators": [
        "uuid",
        "uuids",
        "password",
        "uuidhex",
    ],

    "📅 Date": [
        "datediff",
        "adddays",
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
        keyboard.append([
            InlineKeyboardButton(
                text=category_name,
                callback_data=f"category:{category_name}",
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

        # Never show a dead button.
        if tool_id not in TOOLS:
            continue

        tool_name = TOOLS[tool_id][0]

        row.append(
            InlineKeyboardButton(
                text=tool_name,
                callback_data=f"tool:{tool_id}",
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
            callback_data="back:tools",
        )
    ])

    return InlineKeyboardMarkup(keyboard)

