
Free offline utility tools for Cracker World.

No paid APIs.
No API keys.
No external services.
All operations are local.


import base64
import binascii
import calendar
import csv
import hashlib
import html
import math
import random
import re
import statistics
import string
import textwrap
import uuid
import zlib

from collections import Counter
from datetime import datetime, timedelta
from urllib.parse import quote, unquote


# =========================================================
# HELPERS
# =========================================================

def need_text(text):
    return bool(text and text.strip())


def words(text):
    return re.findall(r"\S+", text)


def parse_numbers(text):
    return [float(x) for x in text.split()]


def clean_float(value):
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


# =========================================================
# TEXT TOOLS
# =========================================================

def text_len(text):
    return f"Characters: {len(text)}"


def word_count2(text):
    return f"Words: {len(words(text))}"


def vowel_count(text):
    return f"Vowels: {sum(c.lower() in 'aeiou' for c in text)}"


def consonant_count(text):
    return f"Consonants: {sum(c.isalpha() and c.lower() not in 'aeiou' for c in text)}"


def digit_count(text):
    return f"Digits: {sum(c.isdigit() for c in text)}"


def space_count(text):
    return f"Spaces: {sum(c.isspace() for c in text)}"


def punctuation_count(text):
    return f"Punctuation: {sum(c in string.punctuation for c in text)}"


def uppercase_count(text):
    return f"Uppercase: {sum(c.isupper() for c in text)}"


def lowercase_count(text):
    return f"Lowercase: {sum(c.islower() for c in text)}"


def capitalize_words(text):
    return " ".join(x.capitalize() for x in text.split())


def swapcase(text):
    return text.swapcase()


def center_text(text):
    parts = text.split("|", 1)

    if len(parts) != 2:
        return "Example: /center 30|hello"

    try:
        width = int(parts[0])
        return parts[1].center(width)
    except ValueError:
        return "Example: /center 30|hello"


def wrap_text(text):
    parts = text.split("|", 1)

    if len(parts) != 2:
        return "Example: /wrap 30|hello world"

    try:
        width = max(1, int(parts[0]))
        return textwrap.fill(parts[1], width=width)
    except ValueError:
        return "Example: /wrap 30|hello world"


def duplicate_words(text):
    ws = words(text)
    counts = Counter(w.lower() for w in ws)
    duplicates = [w for w, n in counts.items() if n > 1]

    return "\n".join(duplicates) if duplicates else "No duplicate words."


def unique_words(text):
    seen = set()
    result = []

    for word in words(text):
        key = word.lower()

        if key not in seen:
            seen.add(key)
            result.append(word)

    return " ".join(result)


def reverse_words(text):
    return " ".join(text.split()[::-1])


def sort_words(text):
    return " ".join(sorted(words(text), key=str.lower))


def alphabetical_words(text):
    return "\n".join(
        f"{i}. {word}"
        for i, word in enumerate(
            sorted(words(text), key=str.lower),
            1
        )
    )


def word_frequency(text):
    counts = Counter(w.lower() for w in words(text))

    return "\n".join(
        f"{word}: {count}"
        for word, count in counts.most_common()
    )


def longest_word(text):
    ws = words(text)
    return max(ws, key=len) if ws else "No words."


def shortest_word(text):
    ws = words(text)
    return min(ws, key=len) if ws else "No words."


def palindrome(text):
    value = re.sub(r"[^a-zA-Z0-9]", "", text).lower()

    return (
        "✅ Palindrome"
        if value == value[::-1]
        else "❌ Not a palindrome"
    )


def isogram(text):
    value = re.sub(r"[^a-zA-Z]", "", text).lower()

    return (
        "✅ Isogram"
        if len(value) == len(set(value))
        else "❌ Not an isogram"
    )


def anagram(text):
    parts = text.split("|", 1)

    if len(parts) != 2:
        return "Example: /anagram listen|silent"

    a = sorted(re.sub(r"\W", "", parts[0].lower()))
    b = sorted(re.sub(r"\W", "", parts[1].lower()))

    return "✅ Anagrams" if a == b else "❌ Not anagrams"


def remove_vowels(text):
    return re.sub(r"[aeiouAEIOU]", "", text)


def remove_consonants(text):
    return "".join(
        c
        for c in text
        if not (
            c.isalpha()
            and c.lower() not in "aeiou"
        )
    )


def keep_alphanumeric(text):
    return "".join(c for c in text if c.isalnum())


def keep_ascii(text):
    return "".join(c for c in text if ord(c) < 128)


def remove_non_ascii(text):
    return "".join(c for c in text if ord(c) >= 128)


def normalize_newlines(text):
    return text.replace("\r\n", "\n").replace("\r", "\n")


def tabs_to_spaces(text):
    return text.replace("\t", "    ")


def spaces_to_tabs(text):
    return re.sub(r" {4}", "\t", text)


def collapse_lines(text):
    return " ".join(
        line.strip()
        for line in text.splitlines()
    )


def reverse_lines(text):
    return "\n".join(text.splitlines()[::-1])


def sort_unique_lines(text):
    return "\n".join(
        sorted(
            set(text.splitlines()),
            key=str.lower
        )
    )


def line_lengths(text):
    return "\n".join(
        f"{i}: {len(line)}"
        for i, line in enumerate(
            text.splitlines(),
            1
        )
    )


# =========================================================
# EXTRA TEXT TOOLS
# =========================================================

def unique_character_count(text):
    return f"Unique characters: {len(set(text))}"


def unique_word_count(text):
    return f"Unique words: {len(set(w.lower() for w in words(text)))}"


def first_character(text):
    return text[0] if text else "No text."


def last_character(text):
    return text[-1] if text else "No text."


def first_word(text):
    ws = words(text)
    return ws[0] if ws else "No words."


def last_word(text):
    ws = words(text)
    return ws[-1] if ws else "No words."


def reverse_each_word(text):
    return " ".join(
        word[::-1]
        for word in text.split()
    )


def lowercase_words(text):
    return " ".join(
        word.lower()
        for word in text.split()
    )


def uppercase_words(text):
    return " ".join(
        word.upper()
        for word in text.split()
    )


def remove_double_spaces(text):
    return re.sub(r" {2,}", " ", text)


def remove_all_spaces(text):
    return re.sub(r"\s+", "", text)


def spaces_only(text):
    return "".join(
        c for c in text
        if c.isspace()
    )


def letters_digits_only(text):
    return "".join(
        c for c in text
        if c.isalnum()
    )


def remove_digits_extra(text):
    return "".join(
        c for c in text
        if not c.isdigit()
    )


def remove_letters_extra(text):
    return "".join(
        c for c in text
        if not c.isalpha()
    )


def nonempty_line_count(text):
    return f"Non-empty lines: {sum(bool(x.strip()) for x in text.splitlines())}"


def empty_line_count(text):
    return f"Empty lines: {sum(not x.strip() for x in text.splitlines())}"


def first_line(text):
    lines = text.splitlines()
    return lines[0] if lines else "No lines."


def last_line(text):
    lines = text.splitlines()
    return lines[-1] if lines else "No lines."


def longest_line(text):
    lines = text.splitlines()
    return max(lines, key=len) if lines else "No lines."


def shortest_line(text):
    lines = text.splitlines()
    return min(lines, key=len) if lines else "No lines."


def sort_lines_by_length(text):
    return "\n".join(
        sorted(
            text.splitlines(),
            key=len
        )
    )


def unique_sorted_words(text):
    return "\n".join(
        sorted(
            set(words(text)),
            key=str.lower
        )
    )


def character_frequency(text):
    counts = Counter(text)

    return "\n".join(
        f"{repr(char)}: {count}"
        for char, count in counts.most_common()
    )


def letter_frequency(text):
    counts = Counter(
        c.lower()
        for c in text
        if c.isalpha()
    )

    return "\n".join(
        f"{char}: {count}"
        for char, count in counts.most_common()
    )


def digit_frequency(text):
    counts = Counter(
        c for c in text
        if c.isdigit()
    )

    return "\n".join(
        f"{digit}: {count}"
        for digit, count in sorted(counts.items())
    ) or "No digits."


def word_lengths(text):
    return "\n".join(
        f"{word}: {len(word)}"
        for word in words(text)
    ) or "No words."


def average_word_length(text):
    ws = words(text)

    if not ws:
        return "No words."

    return f"{sum(len(w) for w in ws) / len(ws):.2f}"


def average_line_length(text):
    lines = text.splitlines()

    if not lines:
        return "No lines."

    return f"{sum(len(x) for x in lines) / len(lines):.2f}"


def text_density(text):
    if not text:
        return "0%"

    useful = sum(c.isalnum() for c in text)

    return f"{useful / len(text) * 100:.2f}%"


def has_numbers(text):
    return (
        "✅ Contains numbers"
        if any(c.isdigit() for c in text)
        else "❌ No numbers"
    )


def has_letters(text):
    return (
        "✅ Contains letters"
        if any(c.isalpha() for c in text)
        else "❌ No letters"
    )


def has_spaces(text):
    return (
        "✅ Contains spaces"
        if any(c.isspace() for c in text)
        else "❌ No spaces"
    )


def has_punctuation(text):
    return (
        "✅ Contains punctuation"
        if any(c in string.punctuation for c in text)
        else "❌ No punctuation"
    )


def is_numeric(text):
    try:
        float(text.strip())
        return "✅ Numeric"
    except ValueError:
        return "❌ Not numeric"


def is_empty(text):
    return (
        "✅ Empty"
        if not text.strip()
        else "❌ Not empty"
    )


def repeat_each_word(text):
    return " ".join(
        f"{word} {word}"
        for word in text.split()
    )


def number_each_word(text):
    return "\n".join(
        f"{i}. {word}"
        for i, word in enumerate(
            text.split(),
            1
        )
    )


def comma_separated_words(text):
    return ", ".join(words(text))


def words_to_lines(text):
    return "\n".join(words(text))


def remove_first_character(text):
    return text[1:] if text else ""


def remove_last_character(text):
    return text[:-1] if text else ""


def duplicate_text(text):
    return text + text


def reverse_characters(text):
    return text[::-1]


def sort_characters(text):
    return "".join(
        sorted(
            text,
            key=str.lower
        )
    )


def unique_characters(text):
    seen = set()
    result = []

    for char in text:
        if char not in seen:
            seen.add(char)
            result.append(char)

    return "".join(result)


def remove_vowels_extra(text):
    return re.sub(
        r"[aeiouAEIOU]",
        "",
        text
    )


def word_initial_frequency(text):
    counts = Counter(
        word[0].lower()
        for word in words(text)
        if word
    )

    return "\n".join(
        f"{letter}: {count}"
        for letter, count in sorted(counts.items())
    )


def text_summary(text):
    return (
        f"Characters: {len(text)}\n"
        f"Words: {len(words(text))}\n"
        f"Lines: {len(text.splitlines())}\n"
        f"Letters: {sum(c.isalpha() for c in text)}\n"
        f"Digits: {sum(c.isdigit() for c in text)}\n"
        f"Spaces: {sum(c.isspace() for c in text)}\n"
        f"Punctuation: {sum(c in string.punctuation for c in text)}"
    )


# =========================================================
# NUMBER TOOLS
# =========================================================

def decimal_to_binary(text):
    try:
        return bin(int(text.strip()))
    except ValueError:
        return "Example: /decbinary 42"


def decimal_to_octal(text):
    try:
        return oct(int(text.strip()))
    except ValueError:
        return "Example: /decoctal 42"


def decimal_to_hex(text):
    try:
        return hex(int(text.strip()))
    except ValueError:
        return "Example: /dechex 42"


def binary_to_decimal(text):
    try:
        return str(int(text.strip(), 2))
    except ValueError:
        return "Invalid binary."


def octal_to_decimal(text):
    try:
        return str(int(text.strip(), 8))
    except ValueError:
        return "Invalid octal."


def hex_to_decimal(text):
    try:
        return str(int(text.strip(), 16))
    except ValueError:
        return "Invalid hexadecimal."


def binary_to_hex(text):
    try:
        return hex(int(text.strip(), 2))
    except ValueError:
        return "Invalid binary."


def hex_to_binary(text):
    try:
        return bin(int(text.strip(), 16))
    except ValueError:
        return "Invalid hexadecimal."


def digit_sum(text):
    value = re.sub(r"\D", "", text)

    return (
        str(sum(int(x) for x in value))
        if value
        else "0"
    )


def digital_root(text):
    try:
        n = abs(int(text.strip()))

        while n >= 10:
            n = sum(
                int(x)
                for x in str(n)
            )

        return str(n)

    except ValueError:
        return "Example: /root 9875"


def factors(text):
    try:
        n = abs(int(text.strip()))

        if n == 0:
            return "0 has infinitely many divisors."

        result = []

        for i in range(
            1,
            math.isqrt(n) + 1
        ):
            if n % i == 0:
                result.append(i)

                if i != n // i:
                    result.append(n // i)

        return " ".join(
            map(str, sorted(result))
        )

    except ValueError:
        return "Example: /factors 60"


def prime_factors(text):
    try:
        n = abs(int(text.strip()))
        result = []
        d = 2

        while d * d <= n:
            while n % d == 0:
                result.append(d)
                n //= d

            d += 1

        if n > 1:
            result.append(n)

        return (
            " × ".join(map(str, result))
            if result
            else "No factors."
        )

    except ValueError:
        return "Example: /primefactors 84"


def lcm_two(text):
    try:
        a, b = map(int, text.split())
        return str(math.lcm(a, b))
    except ValueError:
        return "Example: /lcm2 12 18"


def gcd_two(text):
    try:
        a, b = map(int, text.split())
        return str(math.gcd(a, b))
    except ValueError:
        return "Example: /gcd2 12 18"


def distance_numbers(text):
    try:
        a, b = map(float, text.split())
        return str(abs(a - b))
    except ValueError:
        return "Example: /distance 10 25"


def percent_change(text):
    try:
        old, new = map(float, text.split())

        if old == 0:
            return "Old value cannot be zero."

        return f"{((new - old) / old) * 100:.2f}%"

    except ValueError:
        return "Example: /percentchange 100 125"


def proportion(text):
    try:
        a, b, c = map(float, text.split())

        if a == 0:
            return "A cannot be zero."

        return str((b * c) / a)

    except ValueError:
        return "Example: /proportion 2 3 10"


def mean2(text):
    try:
        nums = parse_numbers(text)
        return str(
            clean_float(
                statistics.mean(nums)
            )
        )
    except ValueError:
        return "Enter numbers separated by spaces."


def median2(text):
    try:
        nums = parse_numbers(text)
        return str(
            clean_float(
                statistics.median(nums)
            )
        )
    except ValueError:
        return "Enter numbers separated by spaces."


def mode2(text):
    try:
        nums = parse_numbers(text)
        modes = statistics.multimode(nums)

        return " ".join(
            map(str, modes)
        )

    except ValueError:
        return "Enter numbers separated by spaces."


def variance(text):
    try:
        nums = parse_numbers(text)

        if len(nums) < 2:
            return "Need at least 2 numbers."

        return str(
            clean_float(
                statistics.variance(nums)
            )
        )

    except ValueError:
        return "Enter numbers separated by spaces."


def stdev(text):
    try:
        nums = parse_numbers(text)

        if len(nums) < 2:
            return "Need at least 2 numbers."

        return str(
            clean_float(
                statistics.stdev(nums)
            )
        )

    except ValueError:
        return "Enter numbers separated by spaces."


def percentage_of(text):
    try:
        percent, value = map(
            float,
            text.split()
        )

        return str(
            (percent / 100) * value
        )

    except ValueError:
        return "Example: /percentageof 15 200"


def add_numbers(text):
    try:
        return str(
            clean_float(
                sum(parse_numbers(text))
            )
        )
    except ValueError:
        return "Enter numbers separated by spaces."


def multiply_numbers(text):
    try:
        result = 1

        for n in parse_numbers(text):
            result *= n

        return str(clean_float(result))

    except ValueError:
        return "Enter numbers separated by spaces."


# =========================================================
# RANDOM / GENERATORS
# =========================================================

def coin(text):
    return random.choice([
        "🪙 Heads",
        "🪙 Tails"
    ])


def dice(text):
    try:
        sides = int(
            text.strip() or "6"
        )

        if sides < 2 or sides > 1000:
            return "Sides must be between 2 and 1000."

        return f"🎲 {random.randint(1, sides)}"

    except ValueError:
        return "Example: /dice 6"


def dice_many(text):
    try:
        count, sides = map(
            int,
            text.split()
        )

        if not 1 <= count <= 20:
            return "Count must be 1-20."

        if not 2 <= sides <= 1000:
            return "Sides must be 2-1000."

        return " ".join(
            str(random.randint(1, sides))
            for _ in range(count)
        )

    except ValueError:
        return "Example: /dices 5 6"


def random_letter(text):
    return random.choice(
        string.ascii_letters
    )


def random_lowercase(text):
    return random.choice(
        string.ascii_lowercase
    )


def random_uppercase(text):
    return random.choice(
        string.ascii_uppercase
    )


def random_digit(text):
    return random.choice(
        string.digits
    )


def random_hex_color(text):
    return "#" + "".join(
        random.choice(
            "0123456789ABCDEF"
        )
        for _ in range(6)
    )


def random_hex(text):
    try:
        length = int(
            text.strip() or "16"
        )

        if not 1 <= length <= 128:
            return "Length must be 1-128."

        return "".join(
            random.choice(
                "0123456789abcdef"
            )
            for _ in range(length)
        )

    except ValueError:
        return "Example: /randomhex 32"


def uuid_short(text):
    return uuid.uuid4().hex


def random_bool(text):
    return random.choice([
        "True",
        "False"
    ])


# =========================================================
# ENCODING
# =========================================================

def base32_encode2(text):
    return base64.b32encode(
        text.encode()
    ).decode()


def base32_decode2(text):
    try:
        return base64.b32decode(
            text.strip()
        ).decode()
    except Exception:
        return "Invalid Base32."


def base16_encode2(text):
    return base64.b16encode(
        text.encode()
    ).decode()


def base16_decode2(text):
    try:
        return base64.b16decode(
            text.strip()
        ).decode()
    except Exception:
        return "Invalid Base16."


def url_component_encode(text):
    return quote(
        text,
        safe=""
    )


def url_component_decode(text):
    return unquote(text)


def html_escape2(text):
    return html.escape(text)


def html_unescape2(text):
    return html.unescape(text)


def unicode_codepoints(text):
    return " ".join(
        f"U+{ord(c):04X}"
        for c in text
    )


def unicode_chars(text):
    return "\n".join(
        f"{i}. {c} → U+{ord(c):04X}"
        for i, c in enumerate(
            text,
            1
        )
    )


# =========================================================
# HASH / CHECKSUM
# =========================================================

def sha3_224(text):
    return hashlib.sha3_224(
        text.encode()
    ).hexdigest()


def sha3_256(text):
    return hashlib.sha3_256(
        text.encode()
    ).hexdigest()


def sha3_384(text):
    return hashlib.sha3_384(
        text.encode()
    ).hexdigest()


def sha3_512(text):
    return hashlib.sha3_512(
        text.encode()
    ).hexdigest()


def blake2b_hash(text):
    return hashlib.blake2b(
        text.encode()
    ).hexdigest()


def blake2s_hash(text):
    return hashlib.blake2s(
        text.encode()
    ).hexdigest()


def crc32_hash(text):
    return f"{zlib.crc32(text.encode()) & 0xffffffff:08x}"


# =========================================================
# JSON / DATA
# =========================================================

def json_sort_keys(text):
    try:
        data = json.loads(text)

        return json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
            sort_keys=True
        )

    except Exception:
        return "Invalid JSON."


def json_compact(text):
    try:
        data = json.loads(text)

        return json.dumps(
            data,
            ensure_ascii=False,
            separators=(",", ":")
        )

    except Exception:
        return "Invalid JSON."


def json_type(text):
    try:
        data = json.loads(text)

        if data is None:
            return "null"

        if isinstance(data, bool):
            return "boolean"

        if isinstance(data, dict):
            return "object"

        if isinstance(data, list):
            return "array"

        if isinstance(
            data,
            (int, float)
        ):
            return "number"

        return "string"

    except Exception:
        return "Invalid JSON."


def json_keys(text):
    try:
        data = json.loads(text)

        if not isinstance(data, dict):
            return "JSON object required."

        return "\n".join(
            data.keys()
        ) or "No keys."

    except Exception:
        return "Invalid JSON."


def json_array_length(text):
    try:
        data = json.loads(text)

        if not isinstance(data, list):
            return "JSON array required."

        return str(len(data))

    except Exception:
        return "Invalid JSON."


def csv_to_json(text):
    try:
        rows = list(
            csv.DictReader(
                text.splitlines()
            )
        )

        return json.dumps(
            rows,
            indent=2,
            ensure_ascii=False
        )

    except Exception:
        return "Invalid CSV."


def csv_columns(text):
    try:
        reader = csv.reader(
            text.splitlines()
        )

        first = next(reader, [])

        return (
            "\n".join(first)
            if first
            else "No columns."
        )

    except Exception:
        return "Invalid CSV."


# =========================================================
# DATE / TIME
# =========================================================

def today(text):
    return datetime.now().strftime(
        "%Y-%m-%d"
    )


def current_datetime(text):
    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def current_year(text):
    return str(datetime.now().year)


def current_month(text):
    return str(datetime.now().month)


def current_day(text):
    return str(datetime.now().day)


def weekday(text):
    try:
        d = datetime.strptime(
            text.strip(),
            "%Y-%m-%d"
        )

        return d.strftime("%A")

    except ValueError:
        return "Example: /weekday 2026-09-04"


def leap_year(text):
    try:
        year = int(text.strip())

        return (
            "✅ Leap year"
            if calendar.isleap(year)
            else "❌ Not a leap year"
        )

    except ValueError:
        return "Example: /leap 2028"


def days_in_month(text):
    try:
        year, month = map(
            int,
            text.split()
        )

        return str(
            calendar.monthrange(
                year,
                month
            )[1]
        )

    except ValueError:
        return "Example: /monthdays 2026 2"


def add_hours(text):
    try:
        date_text, hours = text.rsplit(
            " ",
            1
        )

        dt = datetime.strptime(
            date_text,
            "%Y-%m-%d %H:%M:%S"
        )

        return (
            dt + timedelta(
                hours=float(hours)
            )
        ).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    except ValueError:
        return "Example: /addhours 2026-01-01 12:00:00 5"


def add_minutes(text):
    try:
        date_text, minutes = text.rsplit(
            " ",
            1
        )

        dt = datetime.strptime(
            date_text,
            "%Y-%m-%d %H:%M:%S"
        )

        return (
            dt + timedelta(
                minutes=float(minutes)
            )
        ).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    except ValueError:
        return "Example: /addminutes 2026-01-01 12:00:00 30"


# =========================================================
# COLOR
# =========================================================

def rgb_to_hsl(text):
    try:
        r, g, b = [
            int(x) / 255
            for x in text.split()
        ]

        import colorsys

        h, l, s = colorsys.rgb_to_hls(
            r,
            g,
            b
        )

        return (
            f"H: {h * 360:.2f}\n"
            f"S: {s * 100:.2f}%\n"
            f"L: {l * 100:.2f}%"
        )

    except Exception:
        return "Example: /rgbtohsl 255 128 0"


def hsl_to_rgb(text):
    try:
        h, s, l = map(
            float,
            text.split()
        )

        import colorsys

        r, g, b = colorsys.hls_to_rgb(
            h / 360,
            l / 100,
            s / 100
        )

        return (
            f"RGB: {round(r * 255)} "
            f"{round(g * 255)} "
            f"{round(b * 255)}"
        )

    except Exception:
        return "Example: /hsltorgb 30 100 50"


# =========================================================
# REGISTRY
# =========================================================

FREE_TOOLS = {

    # -------------------------
    # Original Text
    # -------------------------

    "textlen": ("Text Length", text_len),
    "wordcount2": ("Word Count", word_count2),
    "vowels": ("Vowel Count", vowel_count),
    "consonants": ("Consonant Count", consonant_count),
    "digitcount": ("Digit Count", digit_count),
    "spacecount": ("Space Count", space_count),
    "punctcount": ("Punctuation Count", punctuation_count),
    "uppercount": ("Uppercase Count", uppercase_count),
    "lowercount": ("Lowercase Count", lowercase_count),
    "capitalize": ("Capitalize Words", capitalize_words),
    "swapcase": ("Swap Case", swapcase),
    "center": ("Center Text", center_text),
    "wrap": ("Wrap Text", wrap_text),
    "duplicatewords": ("Duplicate Words", duplicate_words),
    "uniquewords": ("Unique Words", unique_words),
    "reversewords": ("Reverse Words", reverse_words),
    "sortwords": ("Sort Words", sort_words),
    "alphabetical": ("Alphabetical Words", alphabetical_words),
    "wordfreq": ("Word Frequency", word_frequency),
    "longestword": ("Longest Word", longest_word),
    "shortestword": ("Shortest Word", shortest_word),
    "palindrome": ("Palindrome Checker", palindrome),
    "isogram": ("Isogram Checker", isogram),
    "anagram": ("Anagram Checker", anagram),
    "removevowels": ("Remove Vowels", remove_vowels),
    "removeconsonants": ("Remove Consonants", remove_consonants),
    "alphanumeric": ("Keep Alphanumeric", keep_alphanumeric),
    "keepascii": ("Keep ASCII", keep_ascii),
    "nonascii": ("Find Non ASCII", remove_non_ascii),
    "normalizenewline": ("Normalize Newlines", normalize_newlines),
    "tabspace": ("Tabs To Spaces", tabs_to_spaces),
    "spacetab": ("Spaces To Tabs", spaces_to_tabs),
    "collapselines": ("Collapse Lines", collapse_lines),
    "reverselines": ("Reverse Lines", reverse_lines),
    "sortuniquelines": ("Sort Unique Lines", sort_unique_lines),
    "linelengths": ("Line Lengths", line_lengths),

    # -------------------------
    # Extra Text
    # -------------------------

    "uniquechars": ("Unique Character Count", unique_character_count),
    "uniquewordcount": ("Unique Word Count", unique_word_count),
    "firstchar": ("First Character", first_character),
    "lastchar": ("Last Character", last_character),
    "firstword": ("First Word", first_word),
    "lastword": ("Last Word", last_word),
    "reverseeachword": ("Reverse Each Word", reverse_each_word),
    "lowerwords": ("Lowercase Words", lowercase_words),
    "upperwords": ("Uppercase Words", uppercase_words),
    "nodoublespaces": ("Remove Double Spaces", remove_double_spaces),
    "nospace": ("Remove All Spaces", remove_all_spaces),
    "spacesonly": ("Spaces Only", spaces_only),
    "alnumonly": ("Letters And Digits", letters_digits_only),
    "removedigits": ("Remove Digits", remove_digits_extra),
    "removeletters": ("Remove Letters", remove_letters_extra),
    "nonemptylines": ("Non Empty Lines", nonempty_line_count),
    "emptylinecount": ("Empty Line Count", empty_line_count),
    "firstline": ("First Line", first_line),
    "lastline": ("Last Line", last_line),
    "longestline": ("Longest Line", longest_line),
    "shortestline": ("Shortest Line", shortest_line),
    "sortbylength": ("Sort Lines By Length", sort_lines_by_length),
    "uniquewordssorted": ("Unique Sorted Words", unique_sorted_words),
    "charfreq": ("Character Frequency", character_frequency),
    "letterfreq": ("Letter Frequency", letter_frequency),
    "digitfreq": ("Digit Frequency", digit_frequency),
    "wordlengths": ("Word Lengths", word_lengths),
    "avgwordlength": ("Average Word Length", average_word_length),
    "avglinelength": ("Average Line Length", average_line_length),
    "textdensity": ("Text Density", text_density),
    "hasnumbers": ("Has Numbers", has_numbers),
    "hasletters": ("Has Letters", has_letters),
    "hasspaces": ("Has Spaces", has_spaces),
    "haspunctuation": ("Has Punctuation", has_punctuation),
    "isnumeric": ("Is Numeric", is_numeric),
    "isempty": ("Is Empty", is_empty),
    "repeatwords": ("Repeat Each Word", repeat_each_word),
    "numberwords": ("Number Words", number_each_word),
    "commaseparated": ("Comma Separated Words", comma_separated_words),
    "wordsnewline": ("Words To New Lines", words_to_lines),
    "removefirstchar": ("Remove First Character", remove_first_character),
    "removelastchar": ("Remove Last Character", remove_last_character),
    "duplicatetext": ("Duplicate Text", duplicate_text),
    "reversechars": ("Reverse Characters", reverse_characters),
    "sortchars": ("Sort Characters", sort_characters),
    "uniquecharslist": ("Remove Duplicate Characters", unique_characters),
    "removevowels2": ("Remove Vowels 2", remove_vowels_extra),
    "initialfreq": ("Word Initial Frequency", word_initial_frequency),
    "textsummary": ("Text Summary", text_summary),

    # -------------------------
    # Numbers
    # -------------------------

    "decbinary": ("Decimal To Binary", decimal_to_binary),
    "decoctal": ("Decimal To Octal", decimal_to_octal),
    "dechex": ("Decimal To Hex", decimal_to_hex),
    "bindec": ("Binary To Decimal", binary_to_decimal),
    "octdec": ("Octal To Decimal", octal_to_decimal),
    "hexdec": ("Hex To Decimal", hex_to_decimal),
    "binhex": ("Binary To Hex", binary_to_hex),
    "hexbin": ("Hex To Binary", hex_to_binary),
    "digitsum": ("Digit Sum", digit_sum),
    "root": ("Digital Root", digital_root),
    "factors": ("Factors", factors),
    "primefactors": ("Prime Factors", prime_factors),
    "lcm2": ("LCM Two Numbers", lcm_two),
    "gcd2": ("GCD Two Numbers", gcd_two),
    "distance": ("Number Distance", distance_numbers),
    "percentchange": ("Percentage Change", percent_change),
    "proportion": ("Proportion Calculator", proportion),
    "mean2": ("Mean", mean2),
    "median2": ("Median", median2),
    "mode2": ("Mode", mode2),
    "variance": ("Variance", variance),
    "stdev": ("Standard Deviation", stdev),
    "percentageof": ("Percentage Of", percentage_of),
    "addnums": ("Add Numbers", add_numbers),
    "mulnums": ("Multiply Numbers", multiply_numbers),

    # -------------------------
    # Random
    # -------------------------

    "coin": ("Coin Flip", coin),
    "dice": ("Dice", dice),
    "dices": ("Multiple Dice", dice_many),
    "randomletter": ("Random Letter", random_letter),
    "randomlower": ("Random Lowercase", random_lowercase),
    "randomupper": ("Random Uppercase", random_uppercase),
    "randomdigit": ("Random Digit", random_digit),
    "randomcolor": ("Random HEX Color", random_hex_color),
    "randomhex": ("Random Hex", random_hex),
    "uuidshort": ("UUID Hex", uuid_short),
    "randombool": ("Random Boolean", random_bool),

    # -------------------------
    # Encoding
    # -------------------------

    "base32": ("Base32 Encode", base32_encode2),
    "base32decode": ("Base32 Decode", base32_decode2),
    "base16": ("Base16 Encode", base16_encode2),
    "base16decode": ("Base16 Decode", base16_decode2),
    "urlcomponent": ("URL Component Encode", url_component_encode),
    "urlcomponentdecode": ("URL Component Decode", url_component_decode),
    "htmlescape2": ("HTML Escape", html_escape2),
    "htmlunescape2": ("HTML Unescape", html_unescape2),
    "codepoints": ("Unicode Codepoints", unicode_codepoints),
    "unicodechars": ("Unicode Character Info", unicode_chars),

    # -------------------------
    # Hash
    # -------------------------

    "sha3_224": ("SHA3-224", sha3_224),
    "sha3_256": ("SHA3-256", sha3_256),
    "sha3_384": ("SHA3-384", sha3_384),
    "sha3_512": ("SHA3-512", sha3_512),
    "blake2b": ("BLAKE2b", blake2b_hash),
    "blake2s": ("BLAKE2s", blake2s_hash),
    "crc32": ("CRC32", crc32_hash),

    # -------------------------
    # JSON / Data
    # -------------------------

    "jsonsort": ("JSON Sort Keys", json_sort_keys),
    "jsoncompact": ("JSON Compact", json_compact),
    "jsontype": ("JSON Type", json_type),
    "jsonkeys": ("JSON Keys", json_keys),
    "jsonlength": ("JSON Array Length", json_array_length),
    "csvjson": ("CSV To JSON", csv_to_json),
    "csvcolumns": ("CSV Columns", csv_columns),

    # -------------------------
    # Date / Time
    # -------------------------

    "today": ("Today", today),
    "datetime": ("Current Date Time", current_datetime),
    "year": ("Current Year", current_year),
    "month": ("Current Month", current_month),
    "day": ("Current Day", current_day),
    "weekday": ("Weekday", weekday),
    "leap": ("Leap Year", leap_year),
    "monthdays": ("Days In Month", days_in_month),
    "addhours": ("Add Hours", add_hours),
    "addminutes": ("Add Minutes", add_minutes),

    # -------------------------
    # Color
    # -------------------------

    "rgbtohsl": ("RGB To HSL", rgb_to_hsl),
    "hsltorgb": ("HSL To RGB", hsl_to_rgb),
}
