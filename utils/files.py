import os
import shutil
import uuid


def create_temp_dir(base_dir="/tmp/telegram_bot"):
    """
    Create a unique temporary directory.
    """

    os.makedirs(base_dir, exist_ok=True)

    folder = os.path.join(
        base_dir,
        uuid.uuid4().hex,
    )

    os.makedirs(
        folder,
        exist_ok=True,
    )

    return folder


def cleanup_temp_folder(folder):
    """
    Safely remove a temporary folder.
    """

    if not folder:
        return

    folder = os.path.abspath(folder)

    # Only remove folders inside our temp directory.
    allowed_base = os.path.abspath(
        "/tmp/telegram_bot"
    )

    if not (
        folder == allowed_base
        or folder.startswith(
            allowed_base + os.sep
        )
    ):
        return

    if os.path.exists(folder):
        shutil.rmtree(
            folder,
            ignore_errors=True,
        )


def ensure_directory(path):
    """
    Create a directory if it does not exist.
    """

    os.makedirs(
        path,
        exist_ok=True,
    )

    return path


def get_extension(filename):
    """
    Return file extension without dot.
    """

    if not filename:
        return ""

    return os.path.splitext(
        filename
    )[1].lower().lstrip(".")


def get_filename_without_extension(filename):
    """
    Return filename without extension.
    """

    if not filename:
        return ""

    return os.path.splitext(
        os.path.basename(filename)
    )[0]


def safe_filename(filename, default="file"):
    """
    Create a filesystem-safe filename.
    """

    if not filename:
        return default

    filename = os.path.basename(
        str(filename)
    )

    allowed = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        "._-"
    )

    cleaned = "".join(
        char if char in allowed else "_"
        for char in filename
    )

    cleaned = cleaned.strip(".")

    return cleaned or default


def get_unique_filename(
    folder,
    filename,
):
    """
    Return a non-conflicting file path.
    """

    filename = safe_filename(filename)

    base, extension = os.path.splitext(
        filename
    )

    path = os.path.join(
        folder,
        filename,
    )

    counter = 1

    while os.path.exists(path):
        path = os.path.join(
            folder,
            f"{base}_{counter}{extension}",
        )
        counter += 1

    return path


def file_exists(path):
    return bool(
        path
        and os.path.isfile(path)
    )


def folder_exists(path):
    return bool(
        path
        and os.path.isdir(path)
    )


def get_file_size(path):
    """
    Return file size in bytes.
    """

    if not file_exists(path):
        return 0

    return os.path.getsize(path)


def get_file_size_mb(path):
    """
    Return file size in MB.
    """

    return round(
        get_file_size(path)
        / (1024 * 1024),
        2,
    )
