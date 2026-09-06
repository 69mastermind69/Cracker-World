import os

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import ContextTypes

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
    keyboard = [
        [
            InlineKeyboardButton(
                "MP3",
                callback_data="audio_mp3",
            ),
            InlineKeyboardButton(
                "WAV",
                callback_data="audio_wav",
            ),
        ],
        [
            InlineKeyboardButton(
                "OGG",
                callback_data="audio_ogg",
            ),
            InlineKeyboardButton(
                "FLAC",
                callback_data="audio_flac",
            ),
        ],
        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="audio_menu",
            ),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def audio_back_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="audio_menu",
            )
        ]
    ])


async def start_text_to_voice(
    update,
    context,
):
    context.user_data.clear()

    context.user_data["audio_action"] = (
        "text_to_voice"
    )

    await update.callback_query.message.reply_text(
        "🗣️ Text → Voice\n\n"
        "যে text-টি voice-এ convert করতে চাও "
        "সেটি পাঠাও।"
    )


async def start_voice_changer(
    update,
    context,
):
    context.user_data.clear()

    context.user_data["audio_action"] = (
        "voice_changer"
    )

    await update.callback_query.message.reply_text(
        "🎭 Voice Changer\n\n"
        "একটি audio file পাঠাও।\n\n"
        "⚠️ Advanced voice effects পরের ধাপে "
        "আরও উন্নত করা হবে।"
    )


async def start_audio_cutter(
    update,
    context,
):
    context.user_data.clear()

    context.user_data["audio_action"] = (
        "audio_cutter"
    )

    await update.callback_query.message.reply_text(
        "✂️ Audio Cutter\n\n"
        "একটি audio file পাঠাও।"
    )


async def start_audio_converter(
    update,
    context,
):
    context.user_data.clear()

    context.user_data["audio_action"] = (
        "audio_converter"
    )

    await update.callback_query.message.reply_text(
        "🔄 Audio Converter\n\n"
        "প্রথমে একটি audio file পাঠাও।"
    )


async def start_volume_changer(
    update,
    context,
):
    context.user_data.clear()

    context.user_data["audio_action"] = (
        "volume_changer"
    )

    await update.callback_query.message.reply_text(
        "🔊 Volume Changer\n\n"
        "একটি audio file পাঠাও।"
    )


async def start_audio_info(
    update,
    context,
):
    context.user_data.clear()

    context.user_data["audio_action"] = (
        "audio_info"
    )

    await update.callback_query.message.reply_text(
        "ℹ️ Audio Info\n\n"
        "একটি audio file পাঠাও।"
    )


async def handle_audio_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    action = context.user_data.get(
        "audio_action"
    )

    if action == "text_to_voice":
        text = update.message.text.strip()

        if not text:
            await update.message.reply_text(
                "⚠️ Text খালি হতে পারবে না।"
            )
            return

        folder = create_temp_dir()

        output_path = os.path.join(
            folder,
            "voice.wav",
        )

        try:
            text_to_voice(
                text,
                output_path,
            )

            with open(
                output_path,
                "rb",
            ) as voice_file:
                await update.message.reply_document(
                    document=voice_file,
                    filename="voice.wav",
                    caption=(
                        "✅ Text → Voice complete!"
                    ),
                )

        except Exception as error:
            await update.message.reply_text(
                "❌ Text → Voice করা যায়নি:\n"
                f"{error}"
            )

        finally:
            cleanup_temp_folder(folder)
            context.user_data.clear()

        return

    if action == "audio_cutter_waiting":
        folder = context.user_data.get(
            "audio_folder"
        )

        input_path = context.user_data.get(
            "audio_input"
        )

        if not folder or not input_path:
            return

        parts = (
            update.message.text
            .strip()
            .replace(",", " ")
            .split()
        )

        if len(parts) != 2:
            await update.message.reply_text(
                "⚠️ Start এবং End time পাঠাও।\n\n"
                "উদাহরণ:\n"
                "10 30"
            )
            return

        try:
            start_seconds = float(parts[0])
            end_seconds = float(parts[1])

        except ValueError:
            await update.message.reply_text(
                "⚠️ Time অবশ্যই number হতে হবে।\n\n"
                "উদাহরণ:\n"
                "10 30"
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
                start_seconds,
                end_seconds,
            )

            with open(
                output_path,
                "rb",
            ) as audio_file:
                await update.message.reply_document(
                    document=audio_file,
                    filename="cut_audio.mp3",
                    caption=(
                        "✅ Audio কাট করা হয়েছে!"
                    ),
                )

        except Exception as error:
            await update.message.reply_text(
                "❌ Audio কাট করা যায়নি:\n"
                f"{error}"
            )

        finally:
            cleanup_temp_folder(folder)
            context.user_data.clear()

        return

    if action == "volume_waiting":
        folder = context.user_data.get(
            "audio_folder"
        )

        input_path = context.user_data.get(
            "audio_input"
        )

        if not folder or not input_path:
            return

        try:
            volume_db = float(
                update.message.text.strip()
            )

        except ValueError:
            await update.message.reply_text(
                "⚠️ Volume একটি number হতে হবে।\n\n"
                "উদাহরণ:\n"
                "5\n\n"
                "অথবা কমাতে:\n"
                "-5"
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
                volume_db,
            )

            with open(
                output_path,
                "rb",
            ) as audio_file:
                await update.message.reply_document(
                    document=audio_file,
                    filename="volume_changed.mp3",
                    caption=(
                        "✅ Volume change হয়েছে!"
                    ),
                )

        except Exception as error:
            await update.message.reply_text(
                "❌ Volume change করা যায়নি:\n"
                f"{error}"
            )

        finally:
            cleanup_temp_folder(folder)
            context.user_data.clear()

        return


async def handle_audio_file(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    action = context.user_data.get(
        "audio_action"
    )

    if not action:
        return

    document = update.message.document

    if not document:
        return

    folder = create_temp_dir()

    filename = (
        document.file_name
        or "input_audio"
    )

    extension = os.path.splitext(
        filename
    )[1].lower()

    input_path = os.path.join(
        folder,
        f"input{extension}",
    )

    try:
        telegram_file = (
            await document.get_file()
        )

        await telegram_file.download_to_drive(
            input_path
        )

        if action == "audio_info":
            info = get_audio_info(
                input_path
            )

            text = (
                "ℹ️ Audio Information\n\n"
                f"📄 Filename: "
                f"{info['filename']}\n"
                f"🎵 Format: "
                f"{info['format']}\n"
                f"⏱️ Duration: "
                f"{info['duration']} sec\n"
                f"🔊 Channels: "
                f"{info['channels']}\n"
                f"🎚️ Sample Rate: "
                f"{info['sample_rate']} Hz\n"
                f"💾 Size: "
                f"{info['file_size_mb']} MB"
            )

            await update.message.reply_text(
                text,
                reply_markup=audio_back_keyboard(),
            )

            return

        if action == "audio_converter":
            context.user_data[
                "audio_folder"
            ] = folder

            context.user_data[
                "audio_input"
            ] = input_path

            await update.message.reply_text(
                "🔄 Audio পাওয়া গেছে!\n\n"
                "কোন format-এ convert করতে চাও?",
                reply_markup=audio_format_keyboard(),
            )

            return

        if action == "audio_cutter":
            context.user_data[
                "audio_folder"
            ] = folder

            context.user_data[
                "audio_input"
            ] = input_path

            context.user_data[
                "audio_action"
            ] = "audio_cutter_waiting"

            await update.message.reply_text(
                "✂️ Audio পাওয়া গেছে!\n\n"
                "Start time এবং End time seconds-এ পাঠাও।\n\n"
                "উদাহরণ:\n"
                "10 30"
            )

            return

        if action == "volume_changer":
            context.user_data[
                "audio_folder"
            ] = folder

            context.user_data[
                "audio_input"
            ] = input_path

            context.user_data[
                "audio_action"
            ] = "volume_waiting"

            await update.message.reply_text(
                "🔊 Audio পাওয়া গেছে!\n\n"
                "কত dB change করতে চাও?\n\n"
                "Volume বাড়াতে:\n"
                "5\n\n"
                "Volume কমাতে:\n"
                "-5"
            )

            return

        if action == "voice_changer":
            await update.message.reply_text(
                "🎭 Voice Changer\n\n"
                "Audio পাওয়া গেছে।\n"
                "Advanced voice effects module "
                "পরের ধাপে connect করা হবে।",
                reply_markup=audio_back_keyboard(),
            )

            return

    except Exception as error:
        await update.message.reply_text(
            "❌ Audio process করা যায়নি:\n"
            f"{error}"
        )

    finally:
        if not context.user_data.get(
            "audio_folder"
        ):
            cleanup_temp_folder(folder)


async def handle_audio_format(
    update,
    context,
    output_format,
):
    folder = context.user_data.get(
        "audio_folder"
    )

    input_path = context.user_data.get(
        "audio_input"
    )

    if not folder or not input_path:
        await update.callback_query.message.reply_text(
            "⚠️ প্রথমে একটি audio file পাঠাও।"
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

        with open(
            output_path,
            "rb",
        ) as audio_file:
            await update.callback_query.message.reply_document(
                document=audio_file,
                filename=f"converted.{output_format}",
                caption=(
                    f"✅ Audio → "
                    f"{output_format.upper()} complete!"
                ),
            )

    except Exception as error:
        await update.callback_query.message.reply_text(
            "❌ Audio convert করা যায়নি:\n"
            f"{error}"
        )

    finally:
        cleanup_temp_folder(folder)
        context.user_data.clear()
