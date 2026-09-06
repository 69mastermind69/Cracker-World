import os
import qrcode


def generate_qr(data, output_path, box_size=10, border=4):
    if not data:
        raise ValueError("QR data cannot be empty.")

    output_dir = os.path.dirname(output_path)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

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


def generate_qr_wifi(
    ssid,
    password,
    security="WPA",
    output_path="wifi_qr.png",
    hidden=False,
):
    if not ssid:
        raise ValueError("Wi-Fi SSID cannot be empty.")

    security = (security or "WPA").upper()

    if security not in {"WPA", "WEP", "nopass"}:
        security = "WPA"

    def escape(value):
        return (
            str(value)
            .replace("\\", "\\\\")
            .replace(";", "\\;")
            .replace(",", "\\,")
            .replace(":", "\\:")
            .replace('"', '\\"')
        )

    data = (
        f'WIFI:T:{security};'
        f'S:{escape(ssid)};'
        f'P:{escape(password or "")};'
        f'H:{"true" if hidden else "false"};;'
    )

    return generate_qr(
        data,
        output_path,
    )


def generate_qr_contact(
    name,
    phone,
    email="",
    output_path="contact_qr.png",
):
    if not name:
        raise ValueError("Contact name cannot be empty.")

    data = (
        "BEGIN:VCARD\n"
        "VERSION:3.0\n"
        f"FN:{name}\n"
        f"TEL:{phone}\n"
    )

    if email:
        data += f"EMAIL:{email}\n"

    data += "END:VCARD"

    return generate_qr(
        data,
        output_path,
    )


def generate_qr_email(
    email,
    subject="",
    message="",
    output_path="email_qr.png",
):
    if not email:
        raise ValueError("Email address cannot be empty.")

    data = f"mailto:{email}"

    params = []

    if subject:
        params.append(
            f"subject={subject}"
        )

    if message:
        params.append(
            f"body={message}"
        )

    if params:
        data += "?" + "&".join(params)

    return generate_qr(
        data,
        output_path,
    )


def generate_qr_phone(
    phone,
    output_path="phone_qr.png",
):
    if not phone:
        raise ValueError("Phone number cannot be empty.")

    return generate_qr(
        f"tel:{phone}",
        output_path,
    )


def generate_qr_url(
    url,
    output_path="url_qr.png",
):
    if not url:
        raise ValueError("URL cannot be empty.")

    return generate_qr(
        url,
        output_path,
    )


def generate_qr_text(
    text,
    output_path="text_qr.png",
):
    if not text:
        raise ValueError("Text cannot be empty.")

    return generate_qr(
        text,
        output_path,
    )
