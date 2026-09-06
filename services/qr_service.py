import os
import qrcode


# ============================================================
# BASIC QR GENERATOR
# ============================================================

def generate_qr(
    data,
    output_path,
    box_size=10,
    border=4,
):
    """
    Generate a standard QR code PNG.
    """

    if not data:
        raise ValueError("QR data is empty.")

    os.makedirs(
        os.path.dirname(output_path) or ".",
        exist_ok=True,
    )

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )

    qr.add_data(str(data))
    qr.make(fit=True)

    image = qr.make_image(
        fill_color="black",
        back_color="white",
    )

    image.save(output_path)

    return output_path


# ============================================================
# WIFI → QR
# ============================================================

def generate_qr_wifi(
    ssid,
    password,
    security="WPA",
    output_path="wifi_qr.png",
    hidden=False,
):
    """
    Generate Wi-Fi QR code.

    security:
        WPA
        WEP
        nopass
    """

    if not ssid:
        raise ValueError("SSID is required.")

    security = str(
        security or "WPA"
    ).strip()

    if security.lower() == "none":
        security = "nopass"

    if security.lower() == "open":
        security = "nopass"

    if security.upper() not in (
        "WPA",
        "WEP",
        "NOPASS",
    ):
        security = "WPA"

    # Escape special Wi-Fi QR characters
    def escape_wifi(value):
        return (
            str(value)
            .replace("\\", "\\\\")
            .replace(";", "\\;")
            .replace(",", "\\,")
            .replace(":", "\\:")
            .replace('"', '\\"')
        )

    wifi_data = (
        f'WIFI:T:{security};'
        f'S:{escape_wifi(ssid)};'
        f'P:{escape_wifi(password or "")};'
        f'H:{"true" if hidden else "false"};;'
    )

    return generate_qr(
        wifi_data,
        output_path,
    )


# ============================================================
# CONTACT / VCARD → QR
# ============================================================

def generate_qr_contact(
    name,
    phone,
    email="",
    output_path="contact_qr.png",
):
    """
    Generate a vCard QR code.
    """

    if not name:
        raise ValueError(
            "Contact name is required."
        )

    if not phone:
        raise ValueError(
            "Phone number is required."
        )

    vcard = (
        "BEGIN:VCARD\n"
        "VERSION:3.0\n"
        f"FN:{name}\n"
        f"TEL:{phone}\n"
    )

    if email:
        vcard += f"EMAIL:{email}\n"

    vcard += "END:VCARD"

    return generate_qr(
        vcard,
        output_path,
    )


# ============================================================
# EMAIL → QR
# ============================================================

def generate_qr_email(
    email,
    subject="",
    message="",
    output_path="email_qr.png",
):
    """
    Generate a mailto QR code.
    """

    if not email:
        raise ValueError(
            "Email address is required."
        )

    from urllib.parse import quote

    query = []

    if subject:
        query.append(
            "subject=" + quote(str(subject))
        )

    if message:
        query.append(
            "body=" + quote(str(message))
        )

    data = f"mailto:{email}"

    if query:
        data += "?" + "&".join(query)

    return generate_qr(
        data,
        output_path,
    )


# ============================================================
# PHONE → QR
# ============================================================

def generate_qr_phone(
    phone,
    output_path="phone_qr.png",
):
    """
    Generate a telephone QR code.
    """

    if not phone:
        raise ValueError(
            "Phone number is required."
        )

    data = f"tel:{phone}"

    return generate_qr(
        data,
        output_path,
    )


# ============================================================
# URL → QR
# ============================================================

def generate_qr_url(
    url,
    output_path="url_qr.png",
):
    """
    Generate a URL QR code.
    """

    if not url:
        raise ValueError(
            "URL is required."
        )

    return generate_qr(
        url,
        output_path,
    )


# ============================================================
# TEXT → QR
# ============================================================

def generate_qr_text(
    text,
    output_path="text_qr.png",
):
    """
    Generate a text QR code.
    """

    if not text:
        raise ValueError(
            "Text is required."
        )

    return generate_qr(
        text,
        output_path,
    )
