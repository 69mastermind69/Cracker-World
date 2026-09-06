import os
import zipfile


def get_file_info(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError("File not found.")

    size_bytes = os.path.getsize(file_path)

    return {
        "filename": os.path.basename(file_path),
        "extension": os.path.splitext(file_path)[1].lower(),
        "size_bytes": size_bytes,
        "size_kb": round(size_bytes / 1024, 2),
        "size_mb": round(size_bytes / (1024 * 1024), 2),
    }


def create_zip(input_files, output_path):
    if not input_files:
        raise ValueError("No files to compress.")

    output_dir = os.path.dirname(output_path)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(
        output_path,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as archive:

        for file_path in input_files:
            if not os.path.isfile(file_path):
                continue

            archive.write(
                file_path,
                arcname=os.path.basename(file_path),
            )

    return output_path


def _safe_extract_path(output_dir, member_name):
    output_dir = os.path.abspath(output_dir)
    target_path = os.path.abspath(
        os.path.join(output_dir, member_name)
    )

    if os.path.commonpath(
        [output_dir, target_path]
    ) != output_dir:
        raise ValueError(
            "Unsafe ZIP path detected."
        )

    return target_path


def extract_zip(zip_path, output_dir):
    if not os.path.isfile(zip_path):
        raise FileNotFoundError("ZIP file not found.")

    if not zipfile.is_zipfile(zip_path):
        raise ValueError("Invalid ZIP file.")

    os.makedirs(output_dir, exist_ok=True)

    extracted_files = []

    with zipfile.ZipFile(zip_path, "r") as archive:
        for member in archive.infolist():
            if member.is_dir():
                _safe_extract_path(
                    output_dir,
                    member.filename,
                )
                continue

            target_path = _safe_extract_path(
                output_dir,
                member.filename,
            )

            os.makedirs(
                os.path.dirname(target_path),
                exist_ok=True,
            )

            with archive.open(member, "r") as source:
                with open(target_path, "wb") as target:
                    target.write(source.read())

            extracted_files.append(target_path)

    return extracted_files


def is_zip_file(file_path):
    if not os.path.isfile(file_path):
        return False

    return zipfile.is_zipfile(file_path)
