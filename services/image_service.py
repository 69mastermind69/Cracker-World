import os
from PIL import Image


SUPPORTED_FORMATS = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "webp": "WEBP",
    "bmp": "BMP",
    "gif": "GIF",
    "tiff": "TIFF",
}


def open_image(image_path):
    """Open an image safely."""
    return Image.open(image_path)


def resize_image(
    input_path,
    output_path,
    width,
    height,
    keep_aspect=True,
):
    """Resize an image."""

    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be greater than 0.")

    with Image.open(input_path) as image:

        if keep_aspect:
            image.thumbnail(
                (width, height),
                Image.Resampling.LANCZOS,
            )

            resized = image.copy()

        else:
            resized = image.resize(
                (width, height),
                Image.Resampling.LANCZOS,
            )

        if resized.mode in ("RGBA", "LA", "P"):
            if output_path.lower().endswith(
                (".jpg", ".jpeg")
            ):
                resized = resized.convert("RGB")

        resized.save(output_path)

        resized.close()

    return output_path


def compress_image(
    input_path,
    output_path,
    quality=70,
):
    """Compress an image."""

    quality = max(1, min(100, int(quality)))

    with Image.open(input_path) as image:

        if image.mode in ("RGBA", "LA", "P"):
            if output_path.lower().endswith(
                (".jpg", ".jpeg")
            ):
                image = image.convert("RGB")

        image.save(
            output_path,
            quality=quality,
            optimize=True,
        )

    return output_path


def convert_image(
    input_path,
    output_path,
    output_format,
):
    """Convert an image to another format."""

    output_format = output_format.lower().replace(
        ".",
        "",
    )

    if output_format not in SUPPORTED_FORMATS:
        raise ValueError(
            "Unsupported image format."
        )

    pil_format = SUPPORTED_FORMATS[
        output_format
    ]

    with Image.open(input_path) as image:

        if pil_format == "JPEG":
            if image.mode != "RGB":
                image = image.convert("RGB")

        image.save(
            output_path,
            format=pil_format,
        )

    return output_path


def get_image_info(image_path):
    """Get basic image information."""

    file_size = os.path.getsize(image_path)

    with Image.open(image_path) as image:

        return {
            "filename": os.path.basename(image_path),
            "format": image.format,
            "width": image.width,
            "height": image.height,
            "mode": image.mode,
            "size_bytes": file_size,
            "size_kb": round(
                file_size / 1024,
                2,
            ),
            "size_mb": round(
                file_size / (1024 * 1024),
                2,
            ),
        }


def image_to_rgb(input_path, output_path):
    """Convert image to RGB."""

    with Image.open(input_path) as image:
        rgb_image = image.convert("RGB")
        rgb_image.save(
            output_path,
            format="JPEG",
            quality=95,
        )
        rgb_image.close()

    return output_path
