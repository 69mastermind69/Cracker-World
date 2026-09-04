import base64
import hashlib
import json
import random
import re
import string
import uuid
from datetime import datetime, timedelta
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
        f"🔤 Characters: {len(text)}\n"
        f"📄 Lines: {len(text.splitlines())}"
    )


def char_count(text):
    if not text:
        return "Give me some text."

    return f"🔤 Characters: {len(text)}"


def line_count(text):
    if not text:
        return "Give me some text."

    return f"📄 Lines: {len(text.splitlines())}"


def percentage(text):
    try:
        parts = text.split()

        if len(parts) != 2:
            return "Example: /percent 25 200"

        value = float(parts[0])
        total = float(parts[1])

        if total == 0:
            return "❌ Total cannot be zero."

        result = (value / total) * 100

        return f"📊 Percentage: {result:.2f}%"

    except Exception:
        return "❌ Invalid numbers."


def average(text):
    try:
        numbers = [float(x) for x in text.split()]

        if not numbers:
            return "Example: /average 10 20 30"

        result = sum(numbers) / len(numbers)

        return f"📊 Average: {result:.2f}"

    except Exception:
        return "❌ Enter numbers separated by spaces."


def min_max(text):
    try:
        numbers = [float(x) for x in text.split()]

        if not numbers:
            return "Example: /minmax 5 10 2 8"

        return (
            f"⬇️ Minimum: {min(numbers)}\n"
            f"⬆️ Maximum: {max(numbers)}"
        )

    except Exception:
        return "❌ Enter numbers separated by spaces."


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


def json_minify(text):
    if not text:
        return "Give me JSON."

    try:
        data = json.loads(text)

        return json.dumps(
            data,
            ensure_ascii=False,
            separators=(",", ":")
        )

    except Exception:
        return "❌ Invalid JSON."


def json_validate(text):
    if not text:
        return "Give me JSON."

    try:
        json.loads(text)
        return "✅ Valid JSON."

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
        return "Example: /random 1 100"


def random_choice(text):
    if not text:
        return "Example: /choose Apple Banana Orange"

    choices = text.split()

    return f"🎲 Selected: {random.choice(choices)}"


def uuid_generator(text):
    return f"🆔 UUID:\n{uuid.uuid4()}"


def uuid_multiple(text):
    try:
        count = int(text.strip()) if text.strip() else 5

        if count < 1:
            return "❌ Count must be at least 1."

        if count > 20:
            return "❌ Maximum 20 UUIDs at once."

        result = "\n".join(
            str(uuid.uuid4())
            for _ in range(count)
        )

        return f"🆔 UUIDs:\n{result}"

    except Exception:
        return "Example: /uuids 5"


def md5_hash(text):
    if not text:
        return "Give me some text."

    result = hashlib.md5(
        text.encode("utf-8")
    ).hexdigest()

    return f"MD5:\n{result}"


def sha256_hash(text):
    if not text:
        return "Give me some text."

    result = hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()

    return f"SHA-256:\n{result}"


def sha512_hash(text):
    if not text:
        return "Give me some text."

    result = hashlib.sha512(
        text.encode("utf-8")
    ).hexdigest()

    return f"SHA-512:\n{result}"


def duplicate_lines(text):
    if not text:
        return "Give me multiple lines."

    lines = text.splitlines()
    seen = set()
    result = []

    for line in lines:
        if line not in seen:
            seen.add(line)
            result.append(line)

    return "\n".join(result)


def sort_lines(text):
    if not text:
        return "Give me multiple lines."

    lines = text.splitlines()

    return "\n".join(
        sorted(lines, key=str.lower)
    )


def random_password(text):
    try:
        length = int(text.strip()) if text.strip() else 12

        if length < 4:
            return "❌ Minimum length is 4."

        if length > 64:
            return "❌ Maximum length is 64."

        characters = (
            string.ascii_letters
            + string.digits
            + string.punctuation
        )

        password = "".join(
            random.choice(characters)
            for _ in range(length)
        )

        return f"🔑 Random password:\n{password}"

    except Exception:
        return "Example: /password 16"


def date_difference(text):
    try:
        parts = text.split()

        if len(parts) != 2:
            return "Example: /datediff 2026-01-01 2026-12-31"

        date1 = datetime.strptime(
            parts[0],
            "%Y-%m-%d"
        )

        date2 = datetime.strptime(
            parts[1],
            "%Y-%m-%d"
        )

        difference = abs((date2 - date1).days)

        return f"📅 Difference: {difference} days"

    except Exception:
        return "❌ Use YYYY-MM-DD format."


def add_days(text):
    try:
        parts = text.split()

        if len(parts) != 2:
            return "Example: /adddays 2026-01-01 30"

        date = datetime.strptime(
            parts[0],
            "%Y-%m-%d"
        )

        days = int(parts[1])

        result = date + timedelta(days=days)

        return f"📅 Result: {result.strftime('%Y-%m-%d')}"

    except Exception:
        return "❌ Example: /adddays 2026-01-01 30"


TOOLS = {
    "calc": ("Calculator", calculator),
    "upper": ("Uppercase", uppercase),
    "lower": ("Lowercase", lowercase),
    "reverse": ("Reverse Text", reverse_text),
    "count": ("Word Counter", word_count),
    "chars": ("Character Counter", char_count),
    "lines": ("Line Counter", line_count),
    "percent": ("Percentage Calculator", percentage),
    "average": ("Average Calculator", average),
    "minmax": ("Min Max Finder", min_max),
    "b64encode": ("Base64 Encode", base64_encode),
    "b64decode": ("Base64 Decode", base64_decode),
    "urlencode": ("URL Encode", url_encode),
    "urldecode": ("URL Decode", url_decode),
    "json": ("JSON Formatter", json_format),
    "jsonmin": ("JSON Minifier", json_minify),
    "jsoncheck": ("JSON Validator", json_validate),
    "random": ("Random Number", random_number),
    "choose": ("Random Choice", random_choice),
    "uuid": ("UUID Generator", uuid_generator),
    "uuids": ("Multiple UUID Generator", uuid_multiple),
    "md5": ("MD5 Hash", md5_hash),
    "sha256": ("SHA-256 Hash", sha256_hash),
    "sha512": ("SHA-512 Hash", sha512_hash),
    "dedupe": ("Duplicate Line Remover", duplicate_lines),
    "sortlines": ("Text Sorter", sort_lines),
    "password": ("Random Password Generator", random_password),
    "datediff": ("Date Difference", date_difference),
    "adddays": ("Add Days To Date", add_days),
}
