import math
import os

import pyttsx3
from pydub import AudioSegment


SUPPORTED_AUDIO_FORMATS = {
    "mp3",
    "wav",
    "ogg",
    "m4a",
    "flac",
}


def text_to_voice(
    text,
    output_path,
    rate=150,
    volume=1.0,
):
    if not text or not text.strip():
        raise ValueError(
            "Text cannot be empty."
        )

    output_dir = os.path.dirname(
        output_path
    )

    if output_dir:
        os.makedirs(
            output_dir,
            exist_ok=True,
        )

    engine = pyttsx3.init()

    try:
        engine.setProperty(
            "rate",
            int(rate),
        )

        engine.setProperty(
            "volume",
            max(
                0.0,
                min(1.0, float(volume)),
            ),
        )

        # pyttsx3 uses the system speech engine.
        # The Dockerfile installs espeak on Linux.
        engine.save_to_file(
            text,
            output_path,
        )

        engine.runAndWait()

    finally:
        try:
            engine.stop()
        except Exception:
            pass

    if not os.path.isfile(
        output_path
    ):
        raise RuntimeError(
            "Voice engine did not create "
            "the output file."
        )

    return output_path


def load_audio(input_path):
    if not os.path.isfile(input_path):
        raise FileNotFoundError(
            "Audio file not found."
        )

    return AudioSegment.from_file(
        input_path
    )


def _export_format(output_path):
    extension = os.path.splitext(
        output_path
    )[1].lower().lstrip(".")

    if extension == "m4a":
        # FFmpeg normally handles AAC inside M4A.
        return "ipod"

    if extension in SUPPORTED_AUDIO_FORMATS:
        return extension

    raise ValueError(
        f"Unsupported audio format: "
        f"{extension}"
    )


def save_audio(
    audio,
    output_path,
    output_format=None,
):
    output_dir = os.path.dirname(
        output_path
    )

    if output_dir:
        os.makedirs(
            output_dir,
            exist_ok=True,
        )

    if output_format:
        output_format = (
            output_format
            .lower()
            .replace(".", "")
        )

        if output_format == "m4a":
            export_format = "ipod"
        else:
            export_format = output_format

    else:
        export_format = _export_format(
            output_path
        )

    if output_format:
        if output_format not in (
            SUPPORTED_AUDIO_FORMATS
        ):
            raise ValueError(
                f"Unsupported audio format: "
                f"{output_format}"
            )

    audio.export(
        output_path,
        format=export_format,
    )

    return output_path


def convert_audio(
    input_path,
    output_path,
    output_format,
):
    output_format = (
        output_format
        .lower()
        .replace(".", "")
    )

    if output_format not in (
        SUPPORTED_AUDIO_FORMATS
    ):
        raise ValueError(
            f"Unsupported audio format: "
            f"{output_format}"
        )

    audio = load_audio(
        input_path
    )

    return save_audio(
        audio,
        output_path,
        output_format,
    )


def change_volume(
    input_path,
    output_path,
    volume_percent,
):
    volume_percent = float(
        volume_percent
    )

    if volume_percent <= 0:
        raise ValueError(
            "Volume must be greater than 0."
        )

    audio = load_audio(
        input_path
    )

    multiplier = (
        volume_percent / 100.0
    )

    # Convert linear volume multiplier
    # to decibels.
    db_change = (
        20 * math.log10(multiplier)
    )

    changed = audio + db_change

    return save_audio(
        changed,
        output_path,
    )


def cut_audio(
    input_path,
    output_path,
    start_time,
    end_time,
):
    start_time = float(
        start_time
    )
    end_time = float(
        end_time
    )

    if start_time < 0:
        raise ValueError(
            "Start time cannot be negative."
        )

    if end_time <= start_time:
        raise ValueError(
            "End time must be greater than "
            "start time."
        )

    audio = load_audio(
        input_path
    )

    duration_ms = len(audio)

    start_ms = int(
        start_time * 1000
    )

    end_ms = int(
        end_time * 1000
    )

    if start_ms >= duration_ms:
        raise ValueError(
            "Start time is outside the audio."
        )

    end_ms = min(
        end_ms,
        duration_ms,
    )

    if end_ms <= start_ms:
        raise ValueError(
            "Invalid cut range."
        )

    clipped = audio[
        start_ms:end_ms
    ]

    return save_audio(
        clipped,
        output_path,
    )


def get_audio_info(
    input_path
):
    if not os.path.isfile(input_path):
        raise FileNotFoundError(
            "Audio file not found."
        )

    audio = load_audio(
        input_path
    )

    size_bytes = os.path.getsize(
        input_path
    )

    duration_seconds = (
        len(audio) / 1000.0
    )

    size_kb = (
        size_bytes / 1024.0
    )

    extension = os.path.splitext(
        input_path
    )[1].lower().lstrip(".")

    info = {
        "filename": os.path.basename(
            input_path
        ),
        "format": extension or "unknown",
        "duration_seconds": duration_seconds,
        "duration": duration_seconds,
        "channels": audio.channels,
        "sample_rate": audio.frame_rate,
        "sample_width": audio.sample_width,
        "frame_count": (
            len(audio.get_array_of_samples())
        ),
        "size_bytes": size_bytes,
        "size_kb": size_kb,
        "file_size_kb": size_kb,
        "size_mb": (
            size_bytes / (1024 * 1024)
        ),
    }

    return info


def get_audio_duration(
    input_path
):
    info = get_audio_info(
        input_path
    )

    return info[
        "duration_seconds"
    ]
