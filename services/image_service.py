import os

from PIL import Image


SUPPORTED_FORMATS = {
    "jpg",
    "jpeg",
    "png",
    "webp",
    "bmp",
    "gif",
    "tiff",
}


def open_image(input_path):
    if not os.path.isfile(input_path):
        raise FileNotFoundError(
            "Image file not found."
        )

    return Image.open(input_path)


def resize_image(
    input_path,
    output_path,
    width,
    height,
    keep_aspect=True,
):
    if width <= 0 or height <= 0:
        raise ValueError(
            "Width and height must be positive."
        )

    image = open_image(input_path)

    if keep_aspect:
        image.thumbnail(
            (width, height),
            Image.Resampling.LANCZOS,
        )
        resized = image
    else:
        resized = image.resize(
            (width, height),
            Image.Resampling.LANCZOS,
        )

    output_dir = os.path.dirname(output_path)

    if output_dir:
        os.makedirs(
            output_dir,
            exist_ok=True,
        )

    resized.save(
        output_path,
        quality=95,
    )

    return output_path


def compress_image(
    input_path,
    output_path,
    quality=70,
):
    quality = max(
        1,
        min(95, int(quality)),
    )

    image = open_image(input_path)

    output_dir = os.path.dirname(output_path)

    if output_dir:
        os.makedirs(
            output_dir,
            exist_ok=True,
        )

    extension = os.path.splitext(
        output_path
    )[1].lower()

    if extension in {
        ".jpg",
        ".jpeg",
    }:
        image = image.convert("RGB")

        image.save(
            output_path,
            format="JPEG",
            quality=quality,
            optimize=True,
        )

    elif extension == ".webp":
        if image.mode not in {
            "RGB",
            "RGBA",
        }:
            image = image.convert("RGB")

        image.save(
            output_path,
            format="WEBP",
            quality=quality,
            optimize=True,
        )

    elif extension == ".png":
        image.save(
            output_path,
            format="PNG",
            optimize=True,
        )

    else:
        image.save(output_path)

    return output_path


def convert_image(
    input_path,
    output_path,
    output_format,
):
    output_format = (
        output_format
        .lower()
        .replace(".", "")
    )

    if output_format not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported image format: "
            f"{output_format}"
        )

    image = open_image(input_path)

    output_dir = os.path.dirname(output_path)

    if output_dir:
        os.makedirs(
            output_dir,
            exist_ok=True,
        )

    format_map = {
        "jpg": "JPEG",
        "jpeg": "JPEG",
        "png": "PNG",
        "webp": "WEBP",
        "bmp": "BMP",
        "gif": "GIF",
        "tiff": "TIFF",
    }

    save_format = format_map[
        output_format
    ]

    if save_format == "JPEG":
        image = image.convert("RGB")

    elif save_format in {
        "BMP",
        "WEBP",
    }:
        if image.mode not in {
            "RGB",
            "RGBA",
        }:
            image = image.convert("RGB")

    image.save(
        output_path,
        format=save_format,
    )

    return output_path


def get_image_info(input_path):
    image = open_image(input_path)

    width, height = image.size

    size_bytes = os.path.getsize(
        input_path
    )

    return {
        "filename": os.path.basename(
            input_path
        ),
        "format": image.format or "Unknown",
        "mode": image.mode,
        "width": width,
        "height": height,
        "size_bytes": size_bytes,
        "size_kb": round(
            size_bytes / 1024,
            2,
        ),
        "size_mb": round(
            size_bytes / (1024 * 1024),
            2,
        ),
    }


def image_to_rgb(input_path):
    image = open_image(input_path)

    if image.mode != "RGB":
        image = image.convert("RGB")

    return image
