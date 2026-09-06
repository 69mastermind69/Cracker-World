import os
import uuid
import shutil
from pathlib import Path

from config import TEMP_DIR


def ensure_temp_dir():
    """Create the temporary directory if it does not exist."""
    Path(TEMP_DIR).mkdir(parents=True, exist_ok=True)
    return TEMP_DIR


def create_temp_dir():
    """Create a unique temporary folder for one user's task."""
    ensure_temp_dir()

    folder = os.path.join(
        TEMP_DIR,
        str(uuid.uuid4())
    )

    os.makedirs(folder, exist_ok=True)
    return folder


def get_file_path(folder, filename):
    """Create a safe path inside the given folder."""
    filename = os.path.basename(filename)
    return os.path.join(folder, filename)


def delete_file(path):
    """Delete a single file safely."""
    try:
        if os.path.isfile(path):
            os.remove(path)
            return True
    except Exception:
        pass

    return False


def delete_folder(folder):
    """Delete a folder and everything inside it."""
    try:
        if os.path.isdir(folder):
            shutil.rmtree(folder, ignore_errors=True)
            return True
    except Exception:
        pass

    return False


def cleanup_temp_folder(folder):
    """Clean up a user's temporary processing folder."""
    return delete_folder(folder)


def get_file_size_mb(path):
    """Return file size in MB."""
    try:
        size_bytes = os.path.getsize(path)
        return round(size_bytes / (1024 * 1024), 2)
    except Exception:
        return 0.0


def is_allowed_size(path, max_size_mb=20):
    """Check whether a file is within the allowed size."""
    return get_file_size_mb(path) <= max_size_mb
