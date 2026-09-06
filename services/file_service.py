import os
import zipfile
from pathlib import Path


def get_file_info(file_path):
    """Return basic information about a file."""

    if not os.path.isfile(file_path):
        raise FileNotFoundError("File not found.")

    size_bytes = os.path.getsize(file_path)

    return {
        "filename": os.path.basename(file_path),
        "extension": Path(file_path).suffix or "None",
        "size_bytes": size_bytes,
        "size_kb": round(size_bytes / 1024, 2),
        "size_mb": round(size_bytes / (1024 * 1024), 2),
    }


def create_zip(input_files, output_path):
    """Create a ZIP archive from multiple files."""

    if not input_files:
        raise ValueError("No files provided.")

    valid_files = [
        file_path
        for file_path in input_files
        if os.path.isfile(file_path)
    ]

    if not valid_files:
        raise ValueError("No valid files found.")

    os.makedirs(
        os.path.dirname(output_path) or ".",
        exist_ok=True,
    )

    with zipfile.ZipFile(
        output_path,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as archive:

        for file_path in valid_files:
            archive.write(
                file_path,
                arcname=os.path.basename(file_path),
            )

    return output_path


def extract_zip(zip_path, output_dir):
    """Extract a ZIP archive safely."""

    if not os.path.isfile(zip_path):
        raise FileNotFoundError("ZIP file not found.")

    if not zipfile.is_zipfile(zip_path):
        raise ValueError("Invalid ZIP file.")

    os.makedirs(
        output_dir,
        exist_ok=True,
    )

    output_dir = os.path.abspath(output_dir)

    extracted_files = []

    with zipfile.ZipFile(zip_path, "r") as archive:

        # Security check against ZIP path traversal.
        for member in archive.infolist():

            member_path = os.path.abspath(
                os.path.join(
                    output_dir,
                    member.filename,
                )
            )

            if not (
                member_path == output_dir
                or member_path.startswith(
                    output_dir + os.sep
                )
            ):
                raise ValueError(
                    "Unsafe ZIP file detected."
                )

        archive.extractall(output_dir)

        for root, _, files in os.walk(output_dir):

            for filename in files:
                extracted_files.append(
                    os.path.join(
                        root,
                        filename,
                    )
                )

    return extracted_files


def is_zip_file(file_path):
    """Check whether a file is a valid ZIP archive."""

    if not os.path.isfile(file_path):
        return False

    try:
        return zipfile.is_zipfile(file_path)
    except Exception:
        return False
