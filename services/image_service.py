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
    """Open an image."""
    return Image.open(image_path)


def _prepare_for_jpeg(image):
    """Convert an image to RGB when saving as JPEG."""
    if image.mode != "RGB":
        return image.convert("RGB")

    return image.copy()


def resize_image(
    input_path,
    output_path,
    width,
    height,
    keep_aspect=True,
):
    """Resize an image."""

    width = int(width)
    height = int(height)

    if width <= 0 or height <= 0:
        raise ValueError(
            "Width and height must be greater than 0."
        )

    with Image.open(input_path) as image:
        if keep_aspect:
            resized = image.copy()
            resized.thumbnail(
                (width, height),
                Image.Resampling.LANCZOS,
            )
        else:
            resized = image.resize(
                (width, height),
                Image.Resampling.LANCZOS,
            )

        try:
            if output_path.lower().endswith(
                (".jpg", ".jpeg")
            ):
                prepared = _prepare_for_jpeg(resized)
                prepared.save(
                    output_path,
                    format="JPEG",
                    quality=95,
                    optimize=True,
                )
                prepared.close()
            else:
                resized.save(output_path)
        finally:
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
        if output_path.lower().endswith(
            (".jpg", ".jpeg")
        ):
            prepared = _prepare_for_jpeg(image)

            try:
                prepared.save(
                    output_path,
                    format="JPEG",
                    quality=quality,
                    optimize=True,
                )
            finally:
                prepared.close()

        elif output_path.lower().endswith(".webp"):
            image.save(
                output_path,
                format="WEBP",
                quality=quality,
                method=6,
            )

        elif output_path.lower().endswith(".png"):
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
    """Convert an image to another supported format."""

    output_format = (
        str(output_format)
        .lower()
        .replace(".", "")
    )

    if output_format not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported image format: {output_format}"
        )

    pil_format = SUPPORTED_FORMATS[
        output_format
    ]

    with Image.open(input_path) as image:
        if pil_format == "JPEG":
            prepared = _prepare_for_jpeg(image)

            try:
                prepared.save(
                    output_path,
                    format="JPEG",
                    quality=95,
                    optimize=True,
                )
            finally:
                prepared.close()

        elif pil_format == "GIF":
            image.save(
                output_path,
                format="GIF",
            )

        else:
            image.save(
                output_path,
                format=pil_format,
            )

    return output_path


def get_image_info(image_path):
    """Return basic image information."""

    if not os.path.exists(image_path):
        raise FileNotFoundError(
            "Image file does not exist."
        )

    file_size = os.path.getsize(image_path)

    with Image.open(image_path) as image:
        return {
            "filename": os.path.basename(image_path),
            "format": image.format or "Unknown",
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


def image_to_rgb(
    input_path,
    output_path,
):
    """Convert an image to RGB JPEG."""

    with Image.open(input_path) as image:
        rgb_image = image.convert("RGB")

        try:
            rgb_image.save(
                output_path,
                format="JPEG",
                quality=95,
                optimize=True,
            )
        finally:
            rgb_image.close()

    return output_path
