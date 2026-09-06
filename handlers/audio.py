import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from config import MAX_FILE_SIZE_MB
from services.audio_service import (
    text_to_voice,
    convert_audio,
    change_volume,
    cut_audio,
    get_audio_info,
)
from utils.files import (
    create_temp_dir,
    cleanup_temp_folder,
)


def audio_format_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🎵 MP3",
                callback_data="audio_mp3",
            ),
            InlineKeyboardButton(
                "🔊 WAV",
                callback_data="audio_wav",
            ),
        ],
        [
            InlineKeyboardButton(
                "🎧 OGG",
                callback_data="audio_ogg",
            ),
            InlineKeyboardButton(
                "📱 M4A",
                callback_data="audio_m4a",
            ),
        ],
        [
            InlineKeyboardButton(
                "🎼 FLAC",
                callback_data="audio_flac",
            ),
        ],
    ])


def _too_large(size_bytes):
    return (
        size_bytes
        and size_bytes
        > MAX_FILE_SIZE_MB * 1024 * 1024
    )


async def start_text_to_voice(
    update,
    context,
):
    context.user_data.clear()
    context.user_data["audio_action"] = (
        "text_to_voice"
    )

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🗣️ <b>Text → Voice</b>\n\n"
        "যে text voice করতে চাও সেটা পাঠাও।",
        parse_mode="HTML",
    )


async def start_voice_changer(
    update,
    context,
):
    context.user_data.clear()
    context.user_data["audio_action"] = (
        "voice_changer"
    )

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🎭 <b>Voice Changer</b>\n\n"
        "একটি audio বা voice message পাঠাও।",
        parse_mode="HTML",
    )


async def start_audio_cutter(
    update,
    context,
):
    context.user_data.clear()
    context.user_data["audio_action"] = (
        "cutter"
    )

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "✂️ <b>Audio Cutter</b>\n\n"
        "একটি audio/voice পাঠাও।",
        parse_mode="HTML",
    )


async def start_audio_converter(
    update,
    context,
):
    context.user_data.clear()
    context.user_data["audio_action"] = (
        "converter"
    )

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🔄 <b>Audio Converter</b>\n\n"
        "একটি audio/voice পাঠাও।",
        parse_mode="HTML",
    )


async def start_volume_changer(
    update,
    context,
):
    context.user_data.clear()
    context.user_data["audio_action"] = (
        "volume"
    )

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🔊 <b>Volume Changer</b>\n\n"
        "একটি audio/voice পাঠাও।",
        parse_mode="HTML",
    )


async def start_audio_info(
    update,
    context,
):
    context.user_data.clear()
    context.user_data["audio_action"] = (
        "info"
    )

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "ℹ️ <b>Audio Info</b>\n\n"
        "একটি audio/voice পাঠাও।",
        parse_mode="HTML",
    )


async def handle_audio_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    if (
        context.user_data.get("audio_action")
        != "text_to_voice"
    ):
        return

    text = (
        update.message.text or ""
    ).strip()

    if not text:
        await update.message.reply_text(
            "⚠️ Empty text পাঠানো যাবে না।"
        )
        return

    folder = create_temp_dir()

    output_path = os.path.join(
        folder,
        "voice.mp3",
    )

    try:
        text_to_voice(
            text,
            output_path,
        )

        with open(
            output_path,
            "rb",
        ) as file:
            await update.message.reply_audio(
                audio=file,
                filename="voice.mp3",
                caption="🗣️ Text → Voice complete!",
            )

    except Exception as error:
        await update.message.reply_text(
            f"❌ Voice তৈরি করা যায়নি:\n{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()


async def handle_audio_file(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    data = context.user_data
    action = data.get("audio_action")

    if action not in {
        "voice_changer",
        "cutter",
        "converter",
        "volume",
        "info",
    }:
        return

    source = (
        update.message.audio
        or update.message.voice
        or update.message.document
    )

    if not source:
        await update.message.reply_text(
            "⚠️ একটি audio/voice file পাঠাও।"
        )
        return

    size = getattr(
        source,
        "file_size",
        0,
    )

    if _too_large(size):
        await update.message.reply_text(
            f"⚠️ File size {MAX_FILE_SIZE_MB}MB-এর বেশি।"
        )
        return

    folder = create_temp_dir()

    try:
        original_name = getattr(
            source,
            "file_name",
            None,
        ) or "audio"

        extension = os.path.splitext(
            original_name
        )[1].lower()

        if not extension:
            extension = ".ogg"

        input_path = os.path.join(
            folder,
            f"input{extension}",
        )

        telegram_file = await source.get_file()

        await telegram_file.download_to_drive(
            input_path
        )

        if action == "info":
            info = get_audio_info(
                input_path
            )

            await update.message.reply_text(
                "ℹ️ <b>Audio Info</b>\n\n"
                f"📄 Name: <code>{info['filename']}</code>\n"
                f"🎵 Format: {info['format']}\n"
                f"⏱️ Duration: {info['duration_seconds']:.2f}s\n"
                f"🔊 Channels: {info['channels']}\n"
                f"🎚️ Sample Rate: {info['sample_rate']} Hz\n"
                f"💾 Size: {info['size_kb']:.2f} KB",
                parse_mode="HTML",
            )

            cleanup_temp_folder(folder)
            context.user_data.clear()
            return

        if action == "voice_changer":
            output_path = os.path.join(
                folder,
                "voice_changed.mp3",
            )

            # Basic free processing:
            # convert the voice to MP3.
            convert_audio(
                input_path,
                output_path,
                "mp3",
            )

            with open(
                output_path,
                "rb",
            ) as file:
                await update.message.reply_audio(
                    audio=file,
                    filename="voice_changed.mp3",
                    caption=(
                        "🎭 Voice processing complete!"
                    ),
                )

            cleanup_temp_folder(folder)
            context.user_data.clear()
            return

        if action == "converter":
            data["audio_folder"] = folder
            data["audio_input"] = input_path

            await update.message.reply_text(
                "🔄 কোন format-এ convert করতে চাও?",
                reply_markup=audio_format_keyboard(),
            )
            return

        if action == "volume":
            data["audio_folder"] = folder
            data["audio_input"] = input_path
            data["audio_waiting_volume"] = True

            await update.message.reply_text(
                "🔊 Volume percentage পাঠাও।\n\n"
                "Example:\n"
                "<code>150</code> = louder\n"
                "<code>100</code> = original\n"
                "<code>50</code> = quieter",
                parse_mode="HTML",
            )
            return

        if action == "cutter":
            data["audio_folder"] = folder
            data["audio_input"] = input_path
            data["audio_waiting_cut"] = True

            await update.message.reply_text(
                "✂️ Start ও end time পাঠাও।\n\n"
                "Format:\n"
                "<code>10 30</code>\n\n"
                "মানে 10s থেকে 30s পর্যন্ত।",
                parse_mode="HTML",
            )
            return

    except Exception as error:
        await update.message.reply_text(
            f"❌ Audio process করা যায়নি:\n{error}"
        )

        cleanup_temp_folder(folder)
        context.user_data.clear()


async def handle_audio_format(
    update,
    context,
    output_format,
):
    query = update.callback_query
    data = context.user_data

    if data.get("audio_action") != "converter":
        await query.answer(
            "No active audio conversion.",
            show_alert=True,
        )
        return

    folder = data.get(
        "audio_folder"
    )

    input_path = data.get(
        "audio_input"
    )

    if not folder or not input_path:
        await query.answer(
            "Audio data পাওয়া যায়নি।",
            show_alert=True,
        )
        data.clear()
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

        await query.answer(
            "Conversion complete!"
        )

        with open(
            output_path,
            "rb",
        ) as file:
            await query.message.reply_audio(
                audio=file,
                filename=(
                    f"converted.{output_format}"
                ),
                caption=(
                    f"🔄 Converted to "
                    f"{output_format.upper()}"
                ),
            )

    except Exception as error:
        await query.answer(
            "Conversion failed.",
            show_alert=True,
        )

        await query.message.reply_text(
            f"❌ Audio convert করা যায়নি:\n{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        data.clear()


async def handle_volume_text(
    update,
    context,
):
    if not update.message:
        return

    data = context.user_data

    if not data.get(
        "audio_waiting_volume"
    ):
        return

    try:
        volume = float(
            update.message.text.strip()
        )

        if volume <= 0 or volume > 300:
            raise ValueError

    except ValueError:
        await update.message.reply_text(
            "⚠️ 1 থেকে 300-এর মধ্যে percentage দাও।"
        )
        return

    folder = data.get(
        "audio_folder"
    )

    input_path = data.get(
        "audio_input"
    )

    if not folder or not input_path:
        await update.message.reply_text(
            "❌ Audio data পাওয়া যায়নি।"
        )
        data.clear()
        return

    output_path = os.path.join(
        folder,
        "volume_changed.mp3",
    )

    try:
        change_volume(
            input_path,
            output_path,
            volume,
        )

        with open(
            output_path,
            "rb",
        ) as file:
            await update.message.reply_audio(
                audio=file,
                filename="volume_changed.mp3",
                caption=(
                    f"🔊 Volume set to {volume:g}%"
                ),
            )

    except Exception as error:
        await update.message.reply_text(
            f"❌ Volume change করা যায়নি:\n{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        data.clear()


async def handle_cut_text(
    update,
    context,
):
    if not update.message:
        return

    data = context.user_data

    if not data.get(
        "audio_waiting_cut"
    ):
        return

    parts = (
        update.message.text or ""
    ).split()

    if len(parts) != 2:
        await update.message.reply_text(
            "⚠️ এভাবে পাঠাও: <code>10 30</code>",
            parse_mode="HTML",
        )
        return

    try:
        start_time = float(parts[0])
        end_time = float(parts[1])

        if (
            start_time < 0
            or end_time <= start_time
        ):
            raise ValueError

    except ValueError:
        await update.message.reply_text(
            "⚠️ Valid start/end time দাও।"
        )
        return

    folder = data.get(
        "audio_folder"
    )

    input_path = data.get(
        "audio_input"
    )

    if not folder or not input_path:
        await update.message.reply_text(
            "❌ Audio data পাওয়া যায়নি।"
        )
        data.clear()
        return

    output_path = os.path.join(
        folder,
        "cut_audio.mp3",
    )

    try:
        cut_audio(
            input_path,
            output_path,
            start_time,
            end_time,
        )

        with open(
            output_path,
            "rb",
        ) as file:
            await update.message.reply_audio(
                audio=file,
                filename="cut_audio.mp3",
                caption=(
                    f"✂️ Cut: "
                    f"{start_time:g}s → "
                    f"{end_time:g}s"
                ),
            )

    except Exception as error:
        await update.message.reply_text(
            f"❌ Audio কাটতে সমস্যা হয়েছে:\n{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        data.clear()


# Compatibility alias
handle_text_to_voice = handle_audio_text
