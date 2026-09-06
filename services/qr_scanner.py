import cv2


def scan_qr(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(
            "Image could not be opened."
        )

    detector = cv2.QRCodeDetector()
    results = []

    # Try detecting multiple QR codes first.
    try:
        (
            success,
            decoded_info,
            points,
            _,
        ) = detector.detectAndDecodeMulti(image)

        if success and decoded_info:
            for data in decoded_info:
                if data and data.strip():
                    value = data.strip()

                    if value not in results:
                        results.append(value)

    except Exception:
        pass

    # Fallback: detect a single QR code.
    if not results:
        try:
            data, points, _ = (
                detector.detectAndDecode(image)
            )

            if data and data.strip():
                results.append(
                    data.strip()
                )

        except Exception:
            pass

    return results
