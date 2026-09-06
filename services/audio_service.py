import os

import pyttsx3
from pydub import AudioSegment


SUPPORTED_AUDIO_FORMATS = {
    "mp3": "mp3",
    "wav": "wav",
    "ogg": "ogg",
    "m4a": "ipod",
    "flac": "flac",
}


def text_to_voice(
    text,
    output_path,
    rate=150,
    volume=1.0,
):
    """Convert text to speech locally using pyttsx3."""

    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    engine = pyttsx3.init()

    try:
        engine.setProperty(
            "rate",
            int(rate),
        )

        engine.setProperty(
            "volume",
            max(0.0, min(1.0, float(volume))),
        )

        engine.save_to_file(
            text,
            output_path,
        )

        engine.runAndWait()

    finally:
        engine.stop()

    if not os.path.exists(output_path):
        raise RuntimeError(
            "Voice file could not be created."
        )

    if os.path.getsize(output_path) == 0:
        raise RuntimeError(
            "Generated voice file is empty."
        )

    return output_path


def load_audio(input_path):
    """Load an audio file."""

    if not os.path.exists(input_path):
        raise FileNotFoundError(
            "Audio file not found."
        )

    return AudioSegment.from_file(
        input_path
    )


def save_audio(
    audio,
    output_path,
    output_format="mp3",
):
    """Save audio to a supported format."""

    output_format = (
        str(output_format)
        .lower()
        .replace(".", "")
    )

    if output_format not in SUPPORTED_AUDIO_FORMATS:
        raise ValueError(
            f"Unsupported audio format: {output_format}"
        )

    audio.export(
        output_path,
        format=SUPPORTED_AUDIO_FORMATS[
            output_format
        ],
    )

    return output_path


def convert_audio(
    input_path,
    output_path,
    output_format,
):
    """Convert audio between formats."""

    audio = load_audio(input_path)

    try:
        return save_audio(
            audio,
            output_path,
            output_format,
        )
    finally:
        del audio


def change_volume(
    input_path,
    output_path,
    volume_percent,
):
    """
    Change volume using percentage.

    100 = original
    150 = louder
    50  = quieter
    """

    volume_percent = float(volume_percent)

    if volume_percent <= 0:
        raise ValueError(
            "Volume percentage must be greater than 0."
        )

    audio = load_audio(input_path)

    try:
        multiplier = volume_percent / 100.0

        if multiplier <= 0:
            raise ValueError(
                "Invalid volume percentage."
            )

        # Convert multiplier to decibels.
        import math

        db_change = 20 * math.log10(multiplier)

        changed_audio = audio + db_change

        output_format = (
            os.path.splitext(output_path)[1]
            .lower()
            .replace(".", "")
        )

        return save_audio(
            changed_audio,
            output_path,
            output_format,
        )

    finally:
        del audio


def cut_audio(
    input_path,
    output_path,
    start_seconds,
    end_seconds,
):
    """Cut a section from an audio file."""

    start_seconds = float(start_seconds)
    end_seconds = float(end_seconds)

    if start_seconds < 0:
        raise ValueError(
            "Start time cannot be negative."
        )

    if end_seconds <= start_seconds:
        raise ValueError(
            "End time must be greater than start time."
        )

    audio = load_audio(input_path)

    try:
        start_ms = int(
            start_seconds * 1000
        )
        end_ms = int(
            end_seconds * 1000
        )

        if start_ms >= len(audio):
            raise ValueError(
                "Start time is beyond the audio length."
            )

        end_ms = min(
            end_ms,
            len(audio),
        )

        if end_ms <= start_ms:
            raise ValueError(
                "Selected audio section is empty."
            )

        clipped_audio = audio[
            start_ms:end_ms
        ]

        output_format = (
            os.path.splitext(output_path)[1]
            .lower()
            .replace(".", "")
        )

        return save_audio(
            clipped_audio,
            output_path,
            output_format,
        )

    finally:
        del audio


def get_audio_info(input_path):
    """Get basic audio information."""

    audio = load_audio(input_path)

    try:
        file_size = os.path.getsize(
            input_path
        )

        duration_seconds = (
            len(audio) / 1000
        )

        return {
            "filename": os.path.basename(
                input_path
            ),
            "format": (
                os.path.splitext(
                    input_path
                )[1]
                .replace(".", "")
                .upper()
            ),
            "duration_seconds": round(
                duration_seconds,
                2,
            ),
            "duration": round(
                duration_seconds,
                2,
            ),
            "channels": audio.channels,
            "sample_rate": audio.frame_rate,
            "sample_width": audio.sample_width,
            "size_kb": round(
                file_size / 1024,
                2,
            ),
            "size_mb": round(
                file_size / (1024 * 1024),
                2,
            ),
            "file_size_kb": round(
                file_size / 1024,
                2,
            ),
            "file_size_mb": round(
                file_size / (1024 * 1024),
                2,
            ),
        }

    finally:
        del audio


def get_audio_duration(input_path):
    """Return audio duration in seconds."""

    audio = load_audio(input_path)

    try:
        return len(audio) / 1000
    finally:
        del audio
