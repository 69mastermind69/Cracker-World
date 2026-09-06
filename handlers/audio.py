import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from services.audio_service import (
    text_to_voice,
    convert_audio,
    change_volume,
    cut_audio,
    get_audio_info,
)

from utils.files import create_temp_dir, cleanup_temp_folder


AUDIO_FORMATS = ["mp3", "wav", "ogg", "m4a", "flac"]


def audio_format_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("MP3", callback_data="audio_mp3"),
            InlineKeyboardButton("WAV", callback_data="audio_wav"),
        ],
        [
            InlineKeyboardButton("OGG", callback_data="audio_ogg"),
            InlineKeyboardButton("M4A", callback_data="audio_m4a"),
        ],
        [
            InlineKeyboardButton("FLAC", callback_data="audio_flac"),
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="audio_menu"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


async def start_text_to_voice(update, context):
    context.user_data.clear()
    context.user_data["audio_action"] = "text_to_voice"

    await update.callback_query.message.reply_text(
        "🗣️ Text → Voice\n\n"
        "যে text-টা voice করতে চাও সেটা পাঠাও।"
    )


async def start_voice_changer(update, context):
    context.user_data.clear()
    context.user_data["audio_action"] = "voice_changer"

    await update.callback_query.message.reply_text(
        "🎭 Voice Changer\n\n"
        "একটি audio/voice পাঠাও।\n\n"
        "Note: Free server version-এ audio re-export করা হবে।"
    )


async def start_audio_cutter(update, context):
    context.user_data.clear()
    context.user_data["audio_action"] = "cutter"

    await update.callback_query.message.reply_text(
        "✂️ Audio Cutter\n\n"
        "একটি audio/voice পাঠাও।"
    )


async def start_audio_converter(update, context):
    context.user_data.clear()
    context.user_data["audio_action"] = "converter"

    await update.callback_query.message.reply_text(
        "🔄 Audio Converter\n\n"
        "একটি audio/voice পাঠাও।"
    )


async def start_volume_changer(update, context):
    context.user_data.clear()
    context.user_data["audio_action"] = "volume"

    await update.callback_query.message.reply_text(
        "🔊 Volume Changer\n\n"
        "একটি audio/voice পাঠাও।"
    )


async def start_audio_info(update, context):
    context.user_data.clear()
    context.user_data["audio_action"] = "info"

    await update.callback_query.message.reply_text(
        "ℹ️ Audio Info\n\n"
        "একটি audio/voice পাঠাও।"
    )


async def handle_audio_text(update, context):
    if not update.message or not update.message.text:
        return

    if context.user_data.get("audio_action") != "text_to_voice":
        return

    text = update.message.text.strip()

    if not text:
        await update.message.reply_text(
            "⚠️ কিছু text পাঠাও।"
        )
        return

    folder = create_temp_dir()
    output_path = os.path.join(
        folder,
        "voice.wav",
    )

    try:
        await update.message.reply_text(
            "⏳ Voice তৈরি হচ্ছে..."
        )

        text_to_voice(
            text,
            output_path,
        )

        with open(output_path, "rb") as audio:
            await update.message.reply_document(
                document=audio,
                filename="voice.wav",
                caption="✅ Text → Voice complete!",
            )

    except Exception as error:
        await update.message.reply_text(
            "❌ Voice তৈরি করা যায়নি.\n\n"
            f"{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()


async def handle_audio_file(update, context):
    if not update.message:
        return

    action = context.user_data.get("audio_action")

    if action not in (
        "voice_changer",
        "cutter",
        "converter",
        "volume",
        "info",
    ):
        return

    message = update.message

    telegram_file = None
    original_name = "audio"

    if message.audio:
        telegram_file = await message.audio.get_file()
        original_name = (
            message.audio.file_name
            or "audio.mp3"
        )

    elif message.voice:
        telegram_file = await message.voice.get_file()
        original_name = "voice.ogg"

    elif message.document:
        telegram_file = await message.document.get_file()
        original_name = (
            message.document.file_name
            or "audio"
        )

    else:
        return

    folder = create_temp_dir()

    extension = os.path.splitext(
        original_name
    )[1].lower()

    if not extension:
        extension = ".ogg"

    input_path = os.path.join(
        folder,
        f"input{extension}",
    )

    try:
        await telegram_file.download_to_drive(
            input_path
        )

        if action == "info":
            info = get_audio_info(input_path)

            text = (
                "ℹ️ Audio Information\n\n"
                f"📄 Filename: {info['filename']}\n"
                f"🎵 Format: {info['format']}\n"
                f"⏱️ Duration: {info['duration_seconds']} sec\n"
                f"🔊 Channels: {info['channels']}\n"
                f"🎚️ Sample Rate: {info['sample_rate']} Hz\n"
                f"💾 Size: {info['size_kb']} KB"
            )

            await message.reply_text(text)
            return

        if action == "converter":
            context.user_data["audio_folder"] = folder
            context.user_data["audio_input"] = input_path

            await message.reply_text(
                "🔄 কোন format-এ convert করতে চাও?",
                reply_markup=audio_format_keyboard(),
            )
            return

        if action == "voice_changer":
            output_path = os.path.join(
                folder,
                "voice_changed.mp3",
            )

            convert_audio(
                input_path,
                output_path,
                "mp3",
            )

            with open(output_path, "rb") as audio:
                await message.reply_document(
                    document=audio,
                    filename="voice_changed.mp3",
                    caption="✅ Voice processed!",
                )

            return

        if action == "volume":
            context.user_data["audio_folder"] = folder
            context.user_data["audio_input"] = input_path
            context.user_data["audio_waiting_volume"] = True

            await message.reply_text(
                "🔊 Volume কত শতাংশ করতে চাও?\n\n"
                "উদাহরণ:\n"
                "150 = 1.5x volume\n"
                "50 = half volume"
            )
            return

        if action == "cutter":
            context.user_data["audio_folder"] = folder
            context.user_data["audio_input"] = input_path
            context.user_data["audio_waiting_cut"] = True

            await message.reply_text(
                "✂️ Start এবং End time পাঠাও।\n\n"
                "উদাহরণ:\n"
                "10 30\n\n"
                "মানে 10 second থেকে 30 second।"
            )
            return

    except Exception as error:
        await message.reply_text(
            "❌ Audio process করা যায়নি.\n\n"
            f"{error}"
        )

    finally:
        if not context.user_data.get(
            "audio_waiting_volume"
        ) and not context.user_data.get(
            "audio_waiting_cut"
        ) and not context.user_data.get(
            "audio_input"
        ):
            cleanup_temp_folder(folder)
            context.user_data.clear()


async def handle_audio_format(
    update,
    context,
    output_format,
):
    query = update.callback_query

    if query:
        await query.answer()

    folder = context.user_data.get(
        "audio_folder"
    )
    input_path = context.user_data.get(
        "audio_input"
    )

    if not folder or not input_path:
        target = query.message if query else update.message

        await target.reply_text(
            "⚠️ আগে একটি audio পাঠাও।"
        )
        return

    output_format = (
        str(output_format)
        .lower()
        .replace(".", "")
    )

    if output_format not in AUDIO_FORMATS:
        await query.message.reply_text(
            "❌ Unsupported audio format."
        )
        return

    output_path = os.path.join(
        folder,
        f"converted.{output_format}",
    )

    try:
        convert_audio(
            input_path,
            output_path,
            output_format,
        )

        with open(output_path, "rb") as audio:
            await query.message.reply_document(
                document=audio,
                filename=f"converted.{output_format}",
                caption=(
                    f"✅ Audio → "
                    f"{output_format.upper()} complete!"
                ),
            )

    except Exception as error:
        await query.message.reply_text(
            "❌ Audio convert করা যায়নি.\n\n"
            f"{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()


async def handle_volume_text(update, context):
    if not update.message:
        return

    if not context.user_data.get(
        "audio_waiting_volume"
    ):
        return

    folder = context.user_data.get(
        "audio_folder"
    )
    input_path = context.user_data.get(
        "audio_input"
    )

    if not folder or not input_path:
        return

    try:
        percentage = float(
            update.message.text.strip()
        )

        if percentage <= 0:
            raise ValueError

    except ValueError:
        await update.message.reply_text(
            "⚠️ একটি positive number পাঠাও।\n"
            "উদাহরণ: 150"
        )
        return

    output_path = os.path.join(
        folder,
        "volume_changed.mp3",
    )

    try:
        change_volume(
            input_path,
            output_path,
            percentage,
        )

        with open(output_path, "rb") as audio:
            await update.message.reply_document(
                document=audio,
                filename="volume_changed.mp3",
                caption="✅ Volume changed!",
            )

    except Exception as error:
        await update.message.reply_text(
            "❌ Volume change করা যায়নি.\n\n"
            f"{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()


async def handle_cut_text(update, context):
    if not update.message:
        return

    if not context.user_data.get(
        "audio_waiting_cut"
    ):
        return

    folder = context.user_data.get(
        "audio_folder"
    )
    input_path = context.user_data.get(
        "audio_input"
    )

    if not folder or not input_path:
        return

    parts = update.message.text.strip().split()

    if len(parts) != 2:
        await update.message.reply_text(
            "⚠️ Format হবে:\n"
            "start end\n\n"
            "উদাহরণ: 10 30"
        )
        return

    try:
        start = float(parts[0])
        end = float(parts[1])

        if start < 0 or end <= start:
            raise ValueError

    except ValueError:
        await update.message.reply_text(
            "⚠️ সঠিক start/end time দাও।"
        )
        return

    output_path = os.path.join(
        folder,
        "cut_audio.mp3",
    )

    try:
        cut_audio(
            input_path,
            output_path,
            start,
            end,
        )

        with open(output_path, "rb") as audio:
            await update.message.reply_document(
                document=audio,
                filename="cut_audio.mp3",
                caption="✅ Audio cut complete!",
            )

    except Exception as error:
        await update.message.reply_text(
            "❌ Audio cut করা যায়নি.\n\n"
            f"{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()


# Backward-compatible aliases
handle_text_to_voice = handle_audio_text
