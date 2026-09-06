import cv2


def scan_qr(image_path):
    """Decode QR code(s) from an image."""

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Image could not be opened.")

    detector = cv2.QRCodeDetector()

    results = []

    # Try multi-QR detection first
    try:
        success, decoded_info, points, _ = (
            detector.detectAndDecodeMulti(image)
        )

        if success and decoded_info:
            for data in decoded_info:
                if data and data.strip():
                    results.append(data.strip())

    except Exception:
        pass

    # Fallback to single QR detection
    if not results:
        try:
            data, points, _ = detector.detectAndDecode(image)

            if data and data.strip():
                results.append(data.strip())

        except Exception:
            pass

    return results
