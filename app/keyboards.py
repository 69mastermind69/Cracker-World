from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .tools import TOOLS as OLD_TOOLS
from .free_tools import FREE_TOOLS


TOOLS = {
    **OLD_TOOLS,
    **FREE_TOOLS,
}


CATEGORIES = {
    "🧮 Math": [
        "calc", "percent", "average", "minmax",
        "evenodd", "prime", "gcd", "lcm",
        "factorial", "fibonacci", "tobinary",
        "frombinary", "tohex", "fromhex",
        "square", "cube", "sqrt", "power",
        "abs", "round", "sum", "product",
        "median", "range",
    ],

    "🔤 Text": [
        "upper", "lower", "title", "sentence",
        "reverse", "spaces", "emptylines",
        "numberlines", "count", "chars", "lines",
        "stats", "dedupe", "sortlines", "trim",
        "nodigits", "nopunctuation", "digits",
        "letters", "altcase", "repeat",

        "textlen", "vowels", "consonants",
        "digitcount", "spacecount", "punctcount",
        "uppercount", "lowercount", "capitalize",
        "swapcase", "center", "wrap",
        "duplicatewords", "uniquewords",
        "reversewords", "sortwords",
        "wordfreq", "longestword", "shortestword",
        "palindrome", "isogram", "anagram",
        "removevowels", "removeconsonants",
        "alphanumeric", "asciionly",
        "newlinesto", "tabs",
        "reverselines", "sortlines2",
        "linelengths",
    ],

    "🔐 Hash & Encoding": [
        "ascii", "asciidecode",
        "binary", "binarydecode",
        "hex", "hexdecode",
        "rot13",
        "base64", "base64decode",
        "urlencode", "urldecode",
        "md5", "sha1", "sha224",
        "sha256", "sha384", "sha512",

        "base32",
        "base16",
        "urlcomponent",
        "unicode",
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
        "leapyear",
        "daysinmonth",
        "addhours",
        "addminutes",
    ],

    "🔢 Free Numbers": [
        "decimalbin",
        "decimaloct",
        "decimalhex",
        "bindecimal",
        "binoctal",
        "binhex",
        "octdecimal",
        "octbinary",
        "octhex",
        "hexdecimal",
        "hexbinary",
        "hexoctal",
        "digitsum",
        "digitalroot",
        "factors",
        "primefactors",
        "distance",
        "percentchange",
        "proportion",
        "mean",
        "mode",
        "variance",
        "stdev",
        "percentageof",
        "addnumbers",
        "multiplynumbers",
    ],

    "🎨 Free Color": [
        "rgbhsl",
        "hslrgb",
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
