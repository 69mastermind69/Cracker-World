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


# ============================================================
# KEYBOARDS
# ============================================================

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
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔙 Back",
                    callback_data="audio_menu",
                )
            ]
        ]
    )


# ============================================================
# START FUNCTIONS
# ============================================================

async def start_text_to_voice(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()
    context.user_data["audio_action"] = "text_to_voice"

    query = update.callback_query

    if query:
        await query.answer()

        await query.message.reply_text(
            "🗣️ <b>Text → Voice</b>\n\n"
            "যে text-টি voice-এ convert করতে চাও "
            "সেটি পাঠাও।",
            parse_mode="HTML",
        )


async def start_voice_changer(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()
    context.user_data["audio_action"] = "voice_changer"

    query = update.callback_query

    if query:
        await query.answer()

        await query.message.reply_text(
            "🎭 <b>Voice Changer</b>\n\n"
            "একটি audio বা voice message পাঠাও।\n\n"
            "বর্তমান local version basic audio processing করবে।",
            parse_mode="HTML",
        )


async def start_audio_cutter(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()
    context.user_data["audio_action"] = "audio_cutter"

    query = update.callback_query

    if query:
        await query.answer()

        await query.message.reply_text(
            "✂️ <b>Audio Cutter</b>\n\n"
            "একটি audio/voice file পাঠাও।",
            parse_mode="HTML",
        )


async def start_audio_converter(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()
    context.user_data["audio_action"] = "audio_converter"

    query = update.callback_query

    if query:
        await query.answer()

        await query.message.reply_text(
            "🔄 <b>Audio Converter</b>\n\n"
            "একটি audio/voice file পাঠাও।",
            parse_mode="HTML",
        )


async def start_volume_changer(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()
    context.user_data["audio_action"] = "volume_changer"

    query = update.callback_query

    if query:
        await query.answer()

        await query.message.reply_text(
            "🔊 <b>Volume Changer</b>\n\n"
            "একটি audio/voice file পাঠাও।",
            parse_mode="HTML",
        )


async def start_audio_info(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.clear()
    context.user_data["audio_action"] = "audio_info"

    query = update.callback_query

    if query:
        await query.answer()

        await query.message.reply_text(
            "ℹ️ <b>Audio Info</b>\n\n"
            "একটি audio/voice file পাঠাও।",
            parse_mode="HTML",
        )


# ============================================================
# TEXT → VOICE / CUT / VOLUME
# ============================================================

async def handle_audio_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message:
        return

    action = context.user_data.get("audio_action")

    # --------------------------------------------------------
    # TEXT → VOICE
    # --------------------------------------------------------

    if action == "text_to_voice":

        text = (update.message.text or "").strip()

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
                    caption="✅ Text → Voice complete!",
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

    # --------------------------------------------------------
    # AUDIO CUTTER
    # --------------------------------------------------------

    if action == "audio_cutter_waiting":

        folder = context.user_data.get(
            "audio_folder"
        )

        input_path = context.user_data.get(
            "audio_input"
        )

        if not folder or not input_path:
            await update.message.reply_text(
                "❌ Audio process পাওয়া যায়নি।"
            )
            context.user_data.clear()
            return

        parts = (
            (update.message.text or "")
            .strip()
            .replace(",", " ")
            .split()
        )

        if len(parts) != 2:
            await update.message.reply_text(
                "⚠️ Start এবং End time পাঠাও।\n\n"
                "উদাহরণ:\n"
                "<code>10 30</code>",
                parse_mode="HTML",
            )
            return

        try:
            start_seconds = float(parts[0])
            end_seconds = float(parts[1])

            if start_seconds < 0:
                raise ValueError

            if end_seconds <= start_seconds:
                raise ValueError

        except ValueError:
            await update.message.reply_text(
                "⚠️ সঠিক time দাও।\n\n"
                "উদাহরণ:\n"
                "<code>10 30</code>",
                parse_mode="HTML",
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
                    caption="✅ Audio cut complete!",
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

    # --------------------------------------------------------
    # VOLUME
    # --------------------------------------------------------

    if action == "volume_waiting":

        folder = context.user_data.get(
            "audio_folder"
        )

        input_path = context.user_data.get(
            "audio_input"
        )

        if not folder or not input_path:
            await update.message.reply_text(
                "❌ Audio process পাওয়া যায়নি।"
            )
            context.user_data.clear()
            return

        try:
            volume_db = float(
                (update.message.text or "").strip()
            )

        except ValueError:
            await update.message.reply_text(
                "⚠️ Volume number হতে হবে।\n\n"
                "বাড়াতে:\n"
                "<code>5</code>\n\n"
                "কমাতে:\n"
                "<code>-5</code>",
                parse_mode="HTML",
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
                    caption="✅ Volume change complete!",
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


# ============================================================
# DOWNLOAD TELEGRAM AUDIO
# ============================================================

async def _download_audio_message(
    update: Update,
    folder: str,
):
    """
    Supports:
    - Telegram Audio
    - Telegram Voice
    - Telegram Document
    """

    message = update.message

    if not message:
        raise ValueError("Message not found.")

    telegram_file = None
    filename = None
    extension = ".ogg"

    # Normal Telegram audio
    if message.audio:

        telegram_file = await message.audio.get_file()

        filename = (
            message.audio.file_name
            or "audio.mp3"
        )

        extension = (
            os.path.splitext(filename)[1]
            or ".mp3"
        )

    # Telegram voice message
    elif message.voice:

        telegram_file = await message.voice.get_file()

        filename = "voice.ogg"
        extension = ".ogg"

    # Telegram document containing audio
    elif message.document:

        telegram_file = await message.document.get_file()

        filename = (
            message.document.file_name
            or "audio"
        )

        extension = (
            os.path.splitext(filename)[1]
            or ".bin"
        )

    else:
        raise ValueError(
            "No audio file found."
        )

    input_path = os.path.join(
        folder,
        f"input{extension}",
    )

    await telegram_file.download_to_drive(
        input_path
    )

    return input_path, filename


# ============================================================
# AUDIO / VOICE / DOCUMENT HANDLER
# ============================================================

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

    # Only process actual audio/voice/document
    if not (
        update.message.audio
        or update.message.voice
        or update.message.document
    ):
        return

    folder = create_temp_dir()

    try:

        input_path, filename = (
            await _download_audio_message(
                update,
                folder,
            )
        )

        # ----------------------------------------------------
        # AUDIO INFO
        # ----------------------------------------------------

        if action == "audio_info":

            info = get_audio_info(
                input_path
            )

            text = (
                "ℹ️ <b>Audio Information</b>\n\n"
                f"📄 Filename: "
                f"<code>{filename}</code>\n"
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
                parse_mode="HTML",
                reply_markup=audio_back_keyboard(),
            )

            context.user_data.clear()
            return

        # ----------------------------------------------------
        # AUDIO CONVERTER
        # ----------------------------------------------------

        if action == "audio_converter":

            context.user_data[
                "audio_folder"
            ] = folder

            context.user_data[
                "audio_input"
            ] = input_path

            await update.message.reply_text(
                "🔄 <b>Audio received!</b>\n\n"
                "কোন format-এ convert করতে চাও?",
                parse_mode="HTML",
                reply_markup=audio_format_keyboard(),
            )

            return

        # ----------------------------------------------------
        # AUDIO CUTTER
        # ----------------------------------------------------

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
                "✂️ <b>Audio received!</b>\n\n"
                "Start এবং End time seconds-এ পাঠাও।\n\n"
                "উদাহরণ:\n"
                "<code>10 30</code>",
                parse_mode="HTML",
            )

            return

        # ----------------------------------------------------
        # VOLUME
        # ----------------------------------------------------

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
                "🔊 <b>Audio received!</b>\n\n"
                "কত dB change করতে চাও?\n\n"
                "বাড়াতে: <code>5</code>\n"
                "কমাতে: <code>-5</code>",
                parse_mode="HTML",
            )

            return

        # ----------------------------------------------------
        # VOICE CHANGER
        # ----------------------------------------------------

        if action == "voice_changer":

            # Local/free basic processing:
            # re-export audio as MP3.
            output_path = os.path.join(
                folder,
                "voice_changed.mp3",
            )

            convert_audio(
                input_path,
                output_path,
                "mp3",
            )

            with open(
                output_path,
                "rb",
            ) as audio_file:

                await update.message.reply_document(
                    document=audio_file,
                    filename="voice_changed.mp3",
                    caption=(
                        "🎭 Voice Changer complete!\n\n"
                        "ℹ️ Current free/local version "
                        "basic audio re-processing করেছে।"
                    ),
                )

            context.user_data.clear()
            return

        await update.message.reply_text(
            "⚠️ এই audio action বর্তমানে available নয়।"
        )

        context.user_data.clear()

    except Exception as error:

        await update.message.reply_text(
            "❌ Audio process করা যায়নি:\n"
            f"{error}"
        )

        context.user_data.clear()

    finally:

        # Do NOT delete folder when the next
        # step still needs it.
        if not context.user_data.get(
            "audio_folder"
        ):
            cleanup_temp_folder(folder)


# ============================================================
# AUDIO FORMAT CALLBACK
# ============================================================

async def handle_audio_format(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    output_format: str,
):
    query = update.callback_query

    if not query:
        return

    await query.answer()

    folder = context.user_data.get(
        "audio_folder"
    )

    input_path = context.user_data.get(
        "audio_input"
    )

    if not folder or not input_path:

        await query.message.reply_text(
            "⚠️ প্রথমে একটি audio file পাঠাও।"
        )

        return

    output_format = (
        output_format
        .lower()
        .replace(".", "")
    )

    allowed_formats = {
        "mp3",
        "wav",
        "ogg",
        "flac",
    }

    if output_format not in allowed_formats:

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

        with open(
            output_path,
            "rb",
        ) as audio_file:

            await query.message.reply_document(
                document=audio_file,
                filename=f"converted.{output_format}",
                caption=(
                    f"✅ Audio → "
                    f"{output_format.upper()} complete!"
                ),
            )

    except Exception as error:

        await query.message.reply_text(
            "❌ Audio convert করা যায়নি:\n"
            f"{error}"
        )

    finally:

        cleanup_temp_folder(
            folder
        )

        context.user_data.clear()


# ============================================================
# COMPATIBILITY ALIAS
# ============================================================

handle_text_to_voice = handle_audio_text
