import os
import shutil
import uuid


def create_temp_dir(base_dir="/tmp/telegram_bot"):
    os.makedirs(base_dir, exist_ok=True)

    folder = os.path.join(
        base_dir,
        uuid.uuid4().hex,
    )

    os.makedirs(folder, exist_ok=True)

    return folder


def cleanup_temp_folder(folder):
    if not folder:
        return

    base_dir = os.path.abspath(
        "/tmp/telegram_bot"
    )

    folder = os.path.abspath(folder)

    try:
        if os.path.commonpath(
            [base_dir, folder]
        ) != base_dir:
            return
    except ValueError:
        return

    if os.path.isdir(folder):
        shutil.rmtree(
            folder,
            ignore_errors=True,
        )


def ensure_directory(folder):
    os.makedirs(
        folder,
        exist_ok=True,
    )

    return folder


def get_extension(filename):
    return os.path.splitext(
        filename
    )[1].lower().lstrip(".")


def get_filename_without_extension(filename):
    return os.path.splitext(
        os.path.basename(filename)
    )[0]


def safe_filename(filename, default="file"):
    filename = os.path.basename(
        filename or ""
    )

    filename = filename.replace(
        "\x00",
        "",
    )

    if not filename:
        return default

    return filename


def get_unique_filename(folder, filename):
    filename = safe_filename(filename)

    name, extension = os.path.splitext(
        filename
    )

    candidate = os.path.join(
        folder,
        filename,
    )

    counter = 1

    while os.path.exists(candidate):
        candidate = os.path.join(
            folder,
            f"{name}_{counter}{extension}",
        )
        counter += 1

    return candidate


def file_exists(path):
    return os.path.isfile(path)


def folder_exists(path):
    return os.path.isdir(path)


def get_file_size(path):
    if not os.path.isfile(path):
        return 0

    return os.path.getsize(path)


def get_file_size_mb(path):
    return get_file_size(path) / (
        1024 * 1024
    )
