import base64
import hashlib
import json
import random
import re
import uuid
from urllib.parse import quote, unquote


def calculator(text):
    text = text.strip()

    if not text:
        return "Example: /calc 25*4+10"

    if not re.fullmatch(r"[0-9+\-*/().% ]+", text):
        return "❌ Only basic math is allowed."

    try:
        result = eval(text, {"__builtins__": {}}, {})
        return f"🧮 Result: {result}"
    except Exception:
        return "❌ Invalid calculation."


def uppercase(text):
    return text.upper() if text else "Give me some text."


def lowercase(text):
    return text.lower() if text else "Give me some text."


def reverse_text(text):
    return text[::-1] if text else "Give me some text."


def word_count(text):
    if not text:
        return "Give me some text."

    words = text.split()

    return (
        f"📝 Words: {len(words)}\n"
        f"🔤 Characters: {len(text)}"
    )


def base64_encode(text):
    if not text:
        return "Give me some text."

    encoded = base64.b64encode(
        text.encode("utf-8")
    ).decode("utf-8")

    return f"🔐 Base64:\n{encoded}"


def base64_decode(text):
    if not text:
        return "Give me Base64 text."

    try:
        decoded = base64.b64decode(
            text.encode("utf-8")
        ).decode("utf-8")

        return f"🔓 Decoded:\n{decoded}"

    except Exception:
        return "❌ Invalid Base64."


def url_encode(text):
    if not text:
        return "Give me some text."

    return quote(text)


def url_decode(text):
    if not text:
        return "Give me encoded URL text."

    return unquote(text)


def json_format(text):
    if not text:
        return "Give me JSON."

    try:
        data = json.loads(text)

        return json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        )

    except Exception:
        return "❌ Invalid JSON."


def random_number(text):
    try:
        parts = text.split()

        minimum = int(parts[0]) if len(parts) > 0 else 1
        maximum = int(parts[1]) if len(parts) > 1 else 100

        if minimum > maximum:
            minimum, maximum = maximum, minimum

        return f"🎲 Random number: {random.randint(minimum, maximum)}"

    except Exception:
        return "Example: 1 100"


def uuid_generator(text):
    return f"🆔 UUID:\n{uuid.uuid4()}"


def md5_hash(text):
    if not text:
        return "Give me some text."

    result = hashlib.md5(
        text.encode("utf-8")
    ).hexdigest()

    return f"MD5:\n{result}"


TOOLS = {
    "calc": ("Calculator", calculator),
    "upper": ("Uppercase", uppercase),
    "lower": ("Lowercase", lowercase),
    "reverse": ("Reverse Text", reverse_text),
    "count": ("Word Counter", word_count),
    "b64encode": ("Base64 Encode", base64_encode),
    "b64decode": ("Base64 Decode", base64_decode),
    "urlencode": ("URL Encode", url_encode),
    "urldecode": ("URL Decode", url_decode),
    "json": ("JSON Formatter", json_format),
    "random": ("Random Number", random_number),
    "uuid": ("UUID Generator", uuid_generator),
    "md5": ("MD5 Hash", md5_hash),
}
