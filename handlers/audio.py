import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from services.audio_service import (
    text_to_voice,
    convert_audio,
    change_volume,
    cut_audio,
    get_audio_info,
)
from utils.files import create_temp_dir, cleanup_temp_folder


def audio_format_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("MP3", callback_data="audio_mp3"),
            InlineKeyboardButton("WAV", callback_data="audio_wav"),
        ],
        [
            InlineKeyboardButton("OGG", callback_data="audio_ogg"),
            InlineKeyboardButton("FLAC", callback_data="audio_flac"),
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data="audio_menu"),
        ],
    ])


def audio_back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="audio_menu")]
    ])


async def start_text_to_voice(update, context):
    context.user_data.clear()
    context.user_data["audio_action"] = "text_to_voice"

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "🗣️ <b>Text → Voice</b>\n\n"
        "যে text voice-এ convert করতে চাও সেটি পাঠাও।",
        parse_mode="HTML",
    )


async def start_voice_changer(update, context):
    context.user_data.clear()
    context.user_data["audio_action"] = "voice_changer"

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "🎭 <b>Voice Changer</b>\n\n"
        "একটি audio/voice file পাঠাও।\n\n"
        "বর্তমানে basic processing করা হবে।",
        parse_mode="HTML",
    )


async def start_audio_cutter(update, context):
    context.user_data.clear()
    context.user_data["audio_action"] = "audio_cutter"

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "✂️ <b>Audio Cutter</b>\n\n"
        "একটি audio/voice file পাঠাও।",
        parse_mode="HTML",
    )


async def start_audio_converter(update, context):
    context.user_data.clear()
    context.user_data["audio_action"] = "audio_converter"

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "🔄 <b>Audio Converter</b>\n\n"
        "একটি audio/voice file পাঠাও।",
        parse_mode="HTML",
    )


async def start_volume_changer(update, context):
    context.user_data.clear()
    context.user_data["audio_action"] = "volume_changer"

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "🔊 <b>Volume Changer</b>\n\n"
        "একটি audio/voice file পাঠাও।",
        parse_mode="HTML",
    )


async def start_audio_info(update, context):
    context.user_data.clear()
    context.user_data["audio_action"] = "audio_info"

    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "ℹ️ <b>Audio Info</b>\n\n"
        "একটি audio/voice file পাঠাও।",
        parse_mode="HTML",
    )


async def handle_audio_text(update, context):
    if not update.message:
        return

    action = context.user_data.get("audio_action")

    if action == "text_to_voice":
        text = (update.message.text or "").strip()

        if not text:
            await update.message.reply_text("⚠️ Text খালি হতে পারবে না।")
            return

        folder = create_temp_dir()
        output = os.path.join(folder, "voice.wav")

        try:
            text_to_voice(text, output)

            with open(output, "rb") as file:
                await update.message.reply_document(
                    document=file,
                    filename="voice.wav",
                    caption="✅ Text → Voice complete!",
                )

        except Exception as error:
            await update.message.reply_text(
                f"❌ Voice তৈরি করা যায়নি:\n{error}"
            )

        finally:
            cleanup_temp_folder(folder)
            context.user_data.clear()

        return

    if action == "audio_cutter_waiting":
        folder = context.user_data.get("audio_folder")
        input_path = context.user_data.get("audio_input")

        if not folder or not input_path:
            return

        parts = (update.message.text or "").split()

        if len(parts) != 2:
            await update.message.reply_text(
                "⚠️ Format:\n10 30"
            )
            return

        try:
            start = float(parts[0])
            end = float(parts[1])

            output = os.path.join(folder, "cut_audio.mp3")

            cut_audio(
                input_path,
                output,
                start,
                end,
            )

            with open(output, "rb") as file:
                await update.message.reply_document(
                    document=file,
                    filename="cut_audio.mp3",
                    caption="✅ Audio cut হয়েছে!",
                )

        except Exception as error:
            await update.message.reply_text(
                f"❌ Audio cut করা যায়নি:\n{error}"
            )

        finally:
            cleanup_temp_folder(folder)
            context.user_data.clear()

        return

    if action == "volume_waiting":
        folder = context.user_data.get("audio_folder")
        input_path = context.user_data.get("audio_input")

        if not folder or not input_path:
            return

        try:
            db = float((update.message.text or "").strip())
        except ValueError:
            await update.message.reply_text(
                "⚠️ Volume number হতে হবে।\nউদাহরণ: 5 অথবা -5"
            )
            return

        output = os.path.join(folder, "volume_changed.mp3")

        try:
            change_volume(
                input_path,
                output,
                db,
            )

            with open(output, "rb") as file:
                await update.message.reply_document(
                    document=file,
                    filename="volume_changed.mp3",
                    caption="✅ Volume change হয়েছে!",
                )

        except Exception as error:
            await update.message.reply_text(
                f"❌ Volume change করা যায়নি:\n{error}"
            )

        finally:
            cleanup_temp_folder(folder)
            context.user_data.clear()


async def handle_audio_file(update, context):
    if not update.message:
        return

    action = context.user_data.get("audio_action")

    if not action:
        return

    message = update.message

    telegram_file = None
    filename = "input_audio"

    if message.audio:
        telegram_file = await message.audio.get_file()
        filename = message.audio.file_name or "input.mp3"

    elif message.voice:
        telegram_file = await message.voice.get_file()
        filename = "input.ogg"

    elif message.document:
        telegram_file = await message.document.get_file()
        filename = message.document.file_name or "input_audio"

    if not telegram_file:
        await message.reply_text(
            "⚠️ একটি audio/voice file পাঠাও।"
        )
        return

    folder = create_temp_dir()

    extension = os.path.splitext(filename)[1].lower()

    if not extension:
        extension = ".ogg"

    input_path = os.path.join(
        folder,
        f"input{extension}",
    )

    try:
        await telegram_file.download_to_drive(input_path)

        if action == "audio_info":
            info = get_audio_info(input_path)

            await message.reply_text(
                "ℹ️ <b>Audio Information</b>\n\n"
                f"📄 Filename: {info['filename']}\n"
                f"🎵 Format: {info['format']}\n"
                f"⏱️ Duration: {info['duration']} sec\n"
                f"🔊 Channels: {info['channels']}\n"
                f"🎚️ Sample Rate: {info['sample_rate']} Hz\n"
                f"💾 Size: {info['file_size_mb']} MB",
                parse_mode="HTML",
            )

            cleanup_temp_folder(folder)
            context.user_data.clear()
            return

        if action == "audio_converter":
            context.user_data["audio_folder"] = folder
            context.user_data["audio_input"] = input_path

            await message.reply_text(
                "🔄 কোন format-এ convert করতে চাও?",
                reply_markup=audio_format_keyboard(),
            )
            return

        if action == "audio_cutter":
            context.user_data["audio_folder"] = folder
            context.user_data["audio_input"] = input_path
            context.user_data["audio_action"] = "audio_cutter_waiting"

            await message.reply_text(
                "✂️ Start time এবং End time seconds-এ পাঠাও।\n\n"
                "উদাহরণ: 10 30"
            )
            return

        if action == "volume_changer":
            context.user_data["audio_folder"] = folder
            context.user_data["audio_input"] = input_path
            context.user_data["audio_action"] = "volume_waiting"

            await message.reply_text(
                "🔊 কত dB change করতে চাও?\n\n"
                "বাড়াতে: 5\n"
                "কমাতে: -5"
            )
            return

        if action == "voice_changer":
            # Basic safe/local effect: convert to WAV/MP3-compatible output.
            output = os.path.join(folder, "voice_changed.mp3")

            convert_audio(
                input_path,
                output,
                "mp3",
            )

            with open(output, "rb") as file:
                await message.reply_document(
                    document=file,
                    filename="voice_changed.mp3",
                    caption="✅ Voice processing complete!",
                )

            cleanup_temp_folder(folder)
            context.user_data.clear()
            return

    except Exception as error:
        cleanup_temp_folder(folder)
        context.user_data.clear()

        await message.reply_text(
            f"❌ Audio process করা যায়নি:\n{error}"
        )


async def handle_audio_format(update, context, output_format):
    if not update.callback_query:
        return

    folder = context.user_data.get("audio_folder")
    input_path = context.user_data.get("audio_input")

    await update.callback_query.answer()

    if not folder or not input_path:
        await update.callback_query.message.reply_text(
            "⚠️ প্রথমে একটি audio file পাঠাও।"
        )
        return

    output = os.path.join(
        folder,
        f"converted.{output_format}",
    )

    try:
        convert_audio(
            input_path,
            output,
            output_format,
        )

        with open(output, "rb") as file:
            await update.callback_query.message.reply_document(
                document=file,
                filename=f"converted.{output_format}",
                caption=f"✅ Audio → {output_format.upper()} complete!",
            )

    except Exception as error:
        await update.callback_query.message.reply_text(
            f"❌ Audio conversion failed:\n{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()


# Compatibility name
handle_text_to_voice = handle_audio_text
