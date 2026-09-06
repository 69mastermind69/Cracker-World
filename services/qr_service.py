import os

import qrcode
from PIL import Image


def create_qr(
    data,
    output_path,
    box_size=10,
    border=4,
):
    """Create a QR code from any text/data."""

    if not data or not data.strip():
        raise ValueError("QR data cannot be empty.")

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )

    qr.add_data(data)
    qr.make(fit=True)

    image = qr.make_image(
        fill_color="black",
        back_color="white",
    )

    image.save(output_path)

    return output_path


def text_to_qr(text, output_path):
    """Create QR from normal text."""
    return create_qr(text, output_path)


def url_to_qr(url, output_path):
    """Create QR from URL."""

    url = url.strip()

    if not (
        url.startswith("http://")
        or url.startswith("https://")
    ):
        raise ValueError(
            "URL must start with http:// or https://"
        )

    return create_qr(url, output_path)


def phone_to_qr(phone, output_path):
    """Create QR for phone number."""

    phone = phone.strip()

    if not phone:
        raise ValueError("Phone number cannot be empty.")

    data = f"tel:{phone}"

    return create_qr(data, output_path)


def email_to_qr(
    email,
    output_path,
    subject="",
    message="",
):
    """Create QR for email."""

    email = email.strip()

    if not email:
        raise ValueError("Email cannot be empty.")

    data = f"mailto:{email}"

    if subject:
        data += f"?subject={subject}"

    if message:
        separator = "&" if "?" in data else "?"
        data += f"{separator}body={message}"

    return create_qr(data, output_path)


def wifi_to_qr(
    ssid,
    password,
    security="WPA",
    hidden=False,
    output_path=None,
):
    """Create QR for Wi-Fi connection."""

    if not ssid:
        raise ValueError("Wi-Fi SSID cannot be empty.")

    if output_path is None:
        raise ValueError("Output path is required.")

    security = security.upper()

    if security not in ("WPA", "WEP", "nopass"):
        security = "WPA"

    hidden_value = "true" if hidden else "false"

    data = (
        f"WIFI:"
        f"T:{security};"
        f"S:{ssid};"
        f"P:{password};"
        f"H:{hidden_value};;"
    )

    return create_qr(
        data,
        output_path,
    )


def contact_to_qr(
    name,
    phone="",
    email="",
    organization="",
    output_path=None,
):
    """Create a vCard QR code."""

    if not name:
        raise ValueError("Contact name cannot be empty.")

    if output_path is None:
        raise ValueError("Output path is required.")

    data = (
        "BEGIN:VCARD\n"
        "VERSION:3.0\n"
        f"FN:{name}\n"
    )

    if phone:
        data += f"TEL:{phone}\n"

    if email:
        data += f"EMAIL:{email}\n"

    if organization:
        data += f"ORG:{organization}\n"

    data += "END:VCARD"

    return create_qr(
        data,
        output_path,
    )


def qr_to_pdf(
    qr_image_path,
    output_path,
):
    """Convert generated QR image to PDF."""

    with Image.open(qr_image_path) as image:

        if image.mode != "RGB":
            image = image.convert("RGB")

        image.save(
            output_path,
            "PDF",
            resolution=100.0,
        )

    return output_path


def get_qr_info(image_path):
    """Return basic QR image information."""

    with Image.open(image_path) as image:
        return {
            "format": image.format,
            "width": image.width,
            "height": image.height,
            "mode": image.mode,
            "size_bytes": os.path.getsize(
                image_path
            ),
        }
