import base64
import hashlib
import json
import math
import random
import re
import string
import uuid
from datetime import datetime, timedelta
from urllib.parse import quote, unquote


# =========================
# BASIC CALCULATOR
# =========================

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


# =========================
# TEXT TOOLS
# =========================

def uppercase(text):
    return text.upper() if text else "Give me some text."


def lowercase(text):
    return text.lower() if text else "Give me some text."


def title_case(text):
    return text.title() if text else "Give me some text."


def sentence_case(text):
    if not text:
        return "Give me some text."

    return text[:1].upper() + text[1:].lower()


def reverse_text(text):
    return text[::-1] if text else "Give me some text."


def remove_extra_spaces(text):
    if not text:
        return "Give me some text."

    return re.sub(r"\s+", " ", text).strip()


def remove_empty_lines(text):
    if not text:
        return "Give me some text."

    lines = [
        line for line in text.splitlines()
        if line.strip()
    ]

    return "\n".join(lines)


def number_lines(text):
    if not text:
        return "Give me multiple lines."

    lines = text.splitlines()

    return "\n".join(
        f"{index}. {line}"
        for index, line in enumerate(lines, start=1)
    )


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


def text_statistics(text):
    if not text:
        return "Give me some text."

    words = text.split()
    lines = text.splitlines()
    spaces = text.count(" ")
    digits = sum(char.isdigit() for char in text)
    letters = sum(char.isalpha() for char in text)

    return (
        "📊 Text Statistics\n\n"
        f"Words: {len(words)}\n"
        f"Characters: {len(text)}\n"
        f"Lines: {len(lines)}\n"
        f"Letters: {letters}\n"
        f"Digits: {digits}\n"
        f"Spaces: {spaces}"
    )


def duplicate_lines(text):
    if not text:
        return "Give me multiple lines."

    seen = set()
    result = []

    for line in text.splitlines():
        if line not in seen:
            seen.add(line)
            result.append(line)

    return "\n".join(result)


def sort_lines(text):
    if not text:
        return "Give me multiple lines."

    return "\n".join(
        sorted(text.splitlines(), key=str.lower)
    )


# =========================
# ASCII / BINARY / HEX
# =========================

def ascii_encode(text):
    if not text:
        return "Give me some text."

    return " ".join(
        str(ord(char))
        for char in text
    )


def ascii_decode(text):
    try:
        numbers = [
            int(x)
            for x in text.split()
        ]

        return "".join(
            chr(number)
            for number in numbers
        )

    except Exception:
        return "Example: /asciidecode 72 101 108 108 111"


def binary_encode(text):
    if not text:
        return "Give me some text."

    return " ".join(
        format(byte, "08b")
        for byte in text.encode("utf-8")
    )


def binary_decode(text):
    try:
        bits = text.split()

        data = bytes(
            int(bit, 2)
            for bit in bits
        )

        return data.decode("utf-8")

    except Exception:
        return "❌ Invalid binary."


def hex_encode(text):
    if not text:
        return "Give me some text."

    return text.encode("utf-8").hex()


def hex_decode(text):
    try:
        return bytes.fromhex(text).decode("utf-8")

    except Exception:
        return "❌ Invalid hexadecimal."


def rot13(text):
    if not text:
        return "Give me some text."

    return text.translate(
        str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm"
        )
    )


# =========================
# MATH TOOLS
# =========================

def percentage(text):
    try:
        parts = text.split()

        if len(parts) != 2:
            return "Example: /percent 25 200"

        value = float(parts[0])
        total = float(parts[1])

        if total == 0:
            return "❌ Total cannot be zero."

        return f"📊 Percentage: {(value / total) * 100:.2f}%"

    except Exception:
        return "❌ Invalid numbers."


def average(text):
    try:
        numbers = [
            float(x)
            for x in text.split()
        ]

        if not numbers:
            return "Example: /average 10 20 30"

        return f"📊 Average: {sum(numbers) / len(numbers):.2f}"

    except Exception:
        return "❌ Enter numbers separated by spaces."


def min_max(text):
    try:
        numbers = [
            float(x)
            for x in text.split()
        ]

        if not numbers:
            return "Example: /minmax 5 10 2 8"

        return (
            f"⬇️ Minimum: {min(numbers)}\n"
            f"⬆️ Maximum: {max(numbers)}"
        )

    except Exception:
        return "❌ Enter numbers separated by spaces."


def even_odd(text):
    try:
        number = int(text.strip())

        return (
            f"🔢 {number} is "
            f"{'Even' if number % 2 == 0 else 'Odd'}."
        )

    except Exception:
        return "Example: /evenodd 25"


def prime_checker(text):
    try:
        number = int(text.strip())

        if number < 2:
            return f"❌ {number} is not prime."

        for divisor in range(
            2,
            math.isqrt(number) + 1
        ):
            if number % divisor == 0:
                return f"❌ {number} is not prime."

        return f"✅ {number} is prime."

    except Exception:
        return "Example: /prime 29"


def gcd_calculator(text):
    try:
        numbers = [
            int(x)
            for x in text.split()
        ]

        if len(numbers) < 2:
            return "Example: /gcd 24 36"

        result = numbers[0]

        for number in numbers[1:]:
            result = math.gcd(result, number)

        return f"🧮 GCD: {result}"

    except Exception:
        return "❌ Enter integers."


def lcm_calculator(text):
    try:
        numbers = [
            int(x)
            for x in text.split()
        ]

        if len(numbers) < 2:
            return "Example: /lcm 12 18"

        result = numbers[0]

        for number in numbers[1:]:
            result = math.lcm(result, number)

        return f"🧮 LCM: {result}"

    except Exception:
        return "❌ Enter integers."


def factorial(text):
    try:
        number = int(text.strip())

        if number < 0:
            return "❌ Number cannot be negative."

        if number > 1000:
            return "❌ Maximum value is 1000."

        return f"🧮 {number}! = {math.factorial(number)}"

    except Exception:
        return "Example: /factorial 5"


def fibonacci(text):
    try:
        count = int(text.strip()) if text.strip() else 10

        if count < 1:
            return "❌ Count must be at least 1."

        if count > 50:
            return "❌ Maximum 50 numbers."

        sequence = []

        a, b = 0, 1

        for _ in range(count):
            sequence.append(a)
            a, b = b, a + b

        return "🔢 Fibonacci:\n" + " ".join(
            str(number)
            for number in sequence
        )

    except Exception:
        return "Example: /fibonacci 10"


def number_to_binary(text):
    try:
        number = int(text.strip())

        return f"🔢 Binary: {bin(number)[2:]}"

    except Exception:
        return "Example: /tobinary 25"


def binary_to_number(text):
    try:
        number = int(text.strip(), 2)

        return f"🔢 Decimal: {number}"

    except Exception:
        return "Example: /frombinary 11001"


def number_to_hex(text):
    try:
        number = int(text.strip())

        return f"🔢 Hex: {hex(number)[2:].upper()}"

    except Exception:
        return "Example: /tohex 255"


def hex_to_number(text):
    try:
        number = int(text.strip(), 16)

        return f"🔢 Decimal: {number}"

    except Exception:
        return "Example: /fromhex FF"


# =========================
# EXTRA MATH TOOLS
# =========================

def square(text):
    try:
        number = float(text.strip())

        return f"🔢 Square: {number ** 2}"

    except Exception:
        return "Example: /square 12"


def cube(text):
    try:
        number = float(text.strip())

        return f"🔢 Cube: {number ** 3}"

    except Exception:
        return "Example: /cube 5"


def square_root(text):
    try:
        number = float(text.strip())

        if number < 0:
            return "❌ Cannot calculate square root of a negative number."

        return f"√ Square Root: {math.sqrt(number):.6f}"

    except Exception:
        return "Example: /sqrt 144"


def power(text):
    try:
        parts = text.split()

        if len(parts) != 2:
            return "Example: /power 2 8"

        base = float(parts[0])
        exponent = float(parts[1])

        return f"⚡ Result: {base ** exponent}"

    except Exception:
        return "❌ Invalid numbers."


def absolute(text):
    try:
        number = float(text.strip())

        return f"📏 Absolute Value: {abs(number)}"

    except Exception:
        return "Example: /abs -25"


def round_number(text):
    try:
        parts = text.split()

        if len(parts) == 1:
            number = float(parts[0])
            digits = 2

        elif len(parts) == 2:
            number = float(parts[0])
            digits = int(parts[1])

        else:
            return "Example: /round 12.3456 2"

        if digits < 0 or digits > 10:
            return "❌ Decimal places must be between 0 and 10."

        return f"🔢 Rounded: {round(number, digits)}"

    except Exception:
        return "Example: /round 12.3456 2"


def sum_numbers(text):
    try:
        numbers = [
            float(x)
            for x in text.split()
        ]

        if not numbers:
            return "Example: /sum 10 20 30"

        return f"➕ Sum: {sum(numbers)}"

    except Exception:
        return "❌ Enter numbers separated by spaces."


def product_numbers(text):
    try:
        numbers = [
            float(x)
            for x in text.split()
        ]

        if not numbers:
            return "Example: /product 2 3 4"

        result = 1

        for number in numbers:
            result *= number

        return f"✖️ Product: {result}"

    except Exception:
        return "❌ Enter numbers separated by spaces."


def median(text):
    try:
        numbers = sorted(
            float(x)
            for x in text.split()
        )

        if not numbers:
            return "Example: /median 10 20 30"

        middle = len(numbers) // 2

        if len(numbers) % 2 == 0:
            result = (
                numbers[middle - 1]
                + numbers[middle]
            ) / 2
        else:
            result = numbers[middle]

        return f"📊 Median: {result}"

    except Exception:
        return "❌ Enter numbers separated by spaces."


def range_numbers(text):
    try:
        numbers = [
            float(x)
            for x in text.split()
        ]

        if not numbers:
            return "Example: /range 5 10 2 20"

        return f"📊 Range: {max(numbers) - min(numbers)}"

    except Exception:
        return "❌ Enter numbers separated by spaces."


# =========================
# ENCODING / HASH
# =========================

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


def md5_hash(text):
    if not text:
        return "Give me some text."

    return hashlib.md5(
        text.encode("utf-8")
    ).hexdigest()


def sha1_hash(text):
    if not text:
        return "Give me some text."

    return hashlib.sha1(
        text.encode("utf-8")
    ).hexdigest()


def sha224_hash(text):
    if not text:
        return "Give me some text."

    return hashlib.sha224(
        text.encode("utf-8")
    ).hexdigest()


def sha256_hash(text):
    if not text:
        return "Give me some text."

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def sha384_hash(text):
    if not text:
        return "Give me some text."

    return hashlib.sha384(
        text.encode("utf-8")
    ).hexdigest()


def sha512_hash(text):
    if not text:
        return "Give me some text."

    return hashlib.sha512(
        text.encode("utf-8")
    ).hexdigest()


# =========================
# JSON
# =========================

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


# =========================
# EXTRA TEXT TOOLS
# =========================

def trim_text(text):
    if not text:
        return "Give me some text."

    return text.strip()


def remove_digits(text):
    if not text:
        return "Give me some text."

    return re.sub(r"\d", "", text)


def remove_punctuation(text):
    if not text:
        return "Give me some text."

    return text.translate(
        str.maketrans("", "", string.punctuation)
    )


def digits_only(text):
    if not text:
        return "Give me some text."

    return "".join(
        char
        for char in text
        if char.isdigit()
    )


def letters_only(text):
    if not text:
        return "Give me some text."

    return "".join(
        char
        for char in text
        if char.isalpha()
    )


def alternating_case(text):
    if not text:
        return "Give me some text."

    result = []
    index = 0

    for char in text:
        if char.isalpha():
            if index % 2 == 0:
                result.append(char.upper())
            else:
                result.append(char.lower())

            index += 1
        else:
            result.append(char)

    return "".join(result)


def repeat_text(text):
    parts = text.split()

    if len(parts) < 2:
        return "Example: /repeat hello 3"

    try:
        count = int(parts[-1])
        content = " ".join(parts[:-1])

        if count < 1:
            return "❌ Count must be at least 1."

        if count > 20:
            return "❌ Maximum repeat count is 20."

        return "\n".join(
            content
            for _ in range(count)
        )

    except Exception:
        return "Example: /repeat hello 3"


# =========================
# RANDOM / GENERATORS
# =========================

def random_number(text):
    try:
        parts = text.split()

        minimum = (
            int(parts[0])
            if len(parts) > 0
            else 1
        )

        maximum = (
            int(parts[1])
            if len(parts) > 1
            else 100
        )

        if minimum > maximum:
            minimum, maximum = maximum, minimum

        return (
            f"🎲 Random number: "
            f"{random.randint(minimum, maximum)}"
        )

    except Exception:
        return "Example: /random 1 100"


def random_choice(text):
    if not text:
        return "Example: /choose Apple Banana Orange"

    return f"🎲 Selected: {random.choice(text.split())}"


def uuid_generator(text):
    return f"🆔 UUID:\n{uuid.uuid4()}"


def uuid_multiple(text):
    try:
        count = (
            int(text.strip())
            if text.strip()
            else 5
        )

        if count < 1:
            return "❌ Count must be at least 1."

        if count > 20:
            return "❌ Maximum 20 UUIDs."

        return "\n".join(
            str(uuid.uuid4())
            for _ in range(count)
        )

    except Exception:
        return "Example: /uuids 5"


def random_password(text):
    try:
        length = (
            int(text.strip())
            if text.strip()
            else 12
        )

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


# =========================
# DATE TOOLS
# =========================

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

        return (
            f"📅 Difference: "
            f"{abs((date2 - date1).days)} days"
        )

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

        return (
            f"📅 Result: "
            f"{result.strftime('%Y-%m-%d')}"
        )

    except Exception:
        return "❌ Example: /adddays 2026-01-01 30"


# =========================
# TOOL REGISTRY
# =========================

TOOLS = {
    # Math
    "calc": ("Calculator", calculator),
    "percent": ("Percentage Calculator", percentage),
    "average": ("Average Calculator", average),
    "minmax": ("Min Max Finder", min_max),
    "evenodd": ("Even Odd Checker", even_odd),
    "prime": ("Prime Checker", prime_checker),
    "gcd": ("GCD Calculator", gcd_calculator),
    "lcm": ("LCM Calculator", lcm_calculator),
    "factorial": ("Factorial", factorial),
    "fibonacci": ("Fibonacci", fibonacci),
    "tobinary": ("Number To Binary", number_to_binary),
    "frombinary": ("Binary To Number", binary_to_number),
    "tohex": ("Number To Hex", number_to_hex),
    "fromhex": ("Hex To Number", hex_to_number),
    "square": ("Square", square),
    "cube": ("Cube", cube),
    "sqrt": ("Square Root", square_root),
    "power": ("Power Calculator", power),
    "abs": ("Absolute Value", absolute),
    "round": ("Round Number", round_number),
    "sum": ("Sum Calculator", sum_numbers),
    "product": ("Product Calculator", product_numbers),
    "median": ("Median Calculator", median),
    "range": ("Range Calculator", range_numbers),

    # Text
    "upper": ("Uppercase", uppercase),
    "lower": ("Lowercase", lowercase),
    "title": ("Title Case", title_case),
    "sentence": ("Sentence Case", sentence_case),
    "reverse": ("Reverse Text", reverse_text),
    "spaces": ("Remove Extra Spaces", remove_extra_spaces),
    "emptylines": ("Remove Empty Lines", remove_empty_lines),
    "numberlines": ("Line Numbering", number_lines),
    "count": ("Word Counter", word_count),
    "chars": ("Character Counter", char_count),
    "lines": ("Line Counter", line_count),
    "stats": ("Text Statistics", text_statistics),
    "dedupe": ("Duplicate Line Remover", duplicate_lines),
    "sortlines": ("Text Sorter", sort_lines),
    "trim": ("Trim Text", trim_text),
    "nodigits": ("Remove Digits", remove_digits),
    "nopunctuation": ("Remove Punctuation", remove_punctuation),
    "digits": ("Digits Only", digits_only),
    "letters": ("Letters Only", letters_only),
    "altcase": ("Alternating Case", alternating_case),
    "repeat": ("Repeat Text", repeat_text),

    # Encoding
    "ascii": ("ASCII Encoder", ascii_encode),
    "asciidecode": ("ASCII Decoder", ascii_decode),
    "binary": ("Binary Encoder", binary_encode),
    "binarydecode": ("Binary Decoder", binary_decode),
    "hex": ("Hex Encoder", hex_encode),
    "hexdecode": ("Hex Decoder", hex_decode),
    "rot13": ("ROT13", rot13),
    "base64": ("Base64 Encoder", base64_encode),
    "base64decode": ("Base64 Decoder", base64_decode),
    "urlencode": ("URL Encoder", url_encode),
    "urldecode": ("URL Decoder", url_decode),

    # Hash
    "md5": ("MD5 Hash", md5_hash),
    "sha1": ("SHA-1 Hash", sha1_hash),
    "sha224": ("SHA-224 Hash", sha224_hash),
    "sha256": ("SHA-256 Hash", sha256_hash),
    "sha384": ("SHA-384 Hash", sha384_hash),
    "sha512": ("SHA-512 Hash", sha512_hash),

    # JSON
    "json": ("JSON Formatter", json_format),
    "jsonmin": ("JSON Minifier", json_minify),
    "jsoncheck": ("JSON Validator", json_validate),

    # Random
    "random": ("Random Number", random_number),
    "choose": ("Random Choice", random_choice),

    # Generators
    "uuid": ("UUID Generator", uuid_generator),
    "uuids": ("Multiple UUID Generator", uuid_multiple),
    "password": ("Random Password Generator", random_password),

    # Date
    "datediff": ("Date Difference", date_difference),
    "adddays": ("Add Days To Date", add_days),
}
