import os

import fitz
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def _ensure_output_dir(output_path):
    folder = os.path.dirname(output_path)

    if folder:
        os.makedirs(folder, exist_ok=True)


def text_to_pdf(
    text,
    output_path,
    title="Document",
):
    """Convert plain text to PDF."""

    if not text or not text.strip():
        raise ValueError("Text is empty.")

    _ensure_output_dir(output_path)

    page_width, page_height = A4

    pdf = canvas.Canvas(
        output_path,
        pagesize=A4,
    )

    pdf.setTitle(title)

    left = 50
    right = 50
    top = page_height - 55
    bottom = 50

    font_name = "Helvetica"
    font_size = 11
    line_height = 16

    max_width = (
        page_width - left - right
    )

    x = left
    y = top

    pdf.setFont(
        font_name,
        font_size,
    )

    for paragraph in text.splitlines():

        if not paragraph.strip():
            y -= line_height

            if y <= bottom:
                pdf.showPage()
                pdf.setFont(
                    font_name,
                    font_size,
                )
                y = top

            continue

        words = paragraph.split()
        current_line = ""

        for word in words:
            test_line = (
                word
                if not current_line
                else current_line + " " + word
            )

            if (
                pdf.stringWidth(
                    test_line,
                    font_name,
                    font_size,
                )
                <= max_width
            ):
                current_line = test_line
            else:
                if current_line:
                    pdf.drawString(
                        x,
                        y,
                        current_line,
                    )

                    y -= line_height

                    if y <= bottom:
                        pdf.showPage()
                        pdf.setFont(
                            font_name,
                            font_size,
                        )
                        y = top

                current_line = word

        if current_line:
            pdf.drawString(
                x,
                y,
                current_line,
            )

            y -= line_height

            if y <= bottom:
                pdf.showPage()
                pdf.setFont(
                    font_name,
                    font_size,
                )
                y = top

    pdf.save()

    return output_path


def images_to_pdf(
    image_paths,
    output_path,
):
    """Convert one or multiple images to a PDF."""

    if not image_paths:
        raise ValueError(
            "No images were provided."
        )

    _ensure_output_dir(output_path)

    document = fitz.open()

    try:
        for image_path in image_paths:

            if not os.path.exists(image_path):
                raise FileNotFoundError(
                    image_path
                )

            image_document = fitz.open(
                image_path
            )

            try:
                page = document.new_page()

                rect = fitz.Rect(
                    0,
                    0,
                    page.rect.width,
                    page.rect.height,
                )

                page.insert_image(
                    rect,
                    filename=image_path,
                    keep_proportion=True,
                )

            finally:
                image_document.close()

        document.save(output_path)

    finally:
        document.close()

    return output_path


def merge_pdfs(
    pdf_paths,
    output_path,
):
    """Merge multiple PDF files."""

    if not pdf_paths:
        raise ValueError(
            "No PDF files were provided."
        )

    _ensure_output_dir(output_path)

    writer = PdfWriter()

    try:
        for pdf_path in pdf_paths:

            if not os.path.exists(pdf_path):
                raise FileNotFoundError(
                    pdf_path
                )

            reader = PdfReader(pdf_path)

            for page in reader.pages:
                writer.add_page(page)

        with open(
            output_path,
            "wb",
        ) as output:
            writer.write(output)

    finally:
        writer.close()

    return output_path


def split_pdf(
    input_path,
    output_dir,
):
    """Split a PDF into individual page PDFs."""

    if not os.path.exists(input_path):
        raise FileNotFoundError(
            input_path
        )

    os.makedirs(
        output_dir,
        exist_ok=True,
    )

    reader = PdfReader(input_path)
    output_files = []

    for index, page in enumerate(
        reader.pages,
        start=1,
    ):
        writer = PdfWriter()
        writer.add_page(page)

        output_path = os.path.join(
            output_dir,
            f"page_{index}.pdf",
        )

        with open(
            output_path,
            "wb",
        ) as output:
            writer.write(output)

        output_files.append(output_path)

        writer.close()

    return output_files


def pdf_to_text(
    input_path,
    output_path=None,
):
    """Extract text from a PDF."""

    if not os.path.exists(input_path):
        raise FileNotFoundError(
            input_path
        )

    document = fitz.open(input_path)

    try:
        text = "\n".join(
            page.get_text()
            for page in document
        )
    finally:
        document.close()

    if output_path:
        _ensure_output_dir(output_path)

        with open(
            output_path,
            "w",
            encoding="utf-8",
        ) as output:
            output.write(text)

    return text


def protect_pdf(
    input_path,
    output_path,
    password,
):
    """Password-protect a PDF."""

    if not password:
        raise ValueError(
            "Password cannot be empty."
        )

    if not os.path.exists(input_path):
        raise FileNotFoundError(
            input_path
        )

    _ensure_output_dir(output_path)

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)

    with open(
        output_path,
        "wb",
    ) as output:
        writer.write(output)

    writer.close()

    return output_path


def pdf_to_images(
    input_path,
    output_dir,
    image_format="png",
):
    """Convert every PDF page to an image."""

    if not os.path.exists(input_path):
        raise FileNotFoundError(
            input_path
        )

    os.makedirs(
        output_dir,
        exist_ok=True,
    )

    image_format = (
        str(image_format)
        .lower()
        .replace(".", "")
    )

    if image_format not in (
        "png",
        "jpg",
        "jpeg",
    ):
        raise ValueError(
            "Supported formats: PNG, JPG, JPEG."
        )

    document = fitz.open(input_path)
    output_files = []

    try:
        for index, page in enumerate(
            document,
            start=1,
        ):
            pixmap = page.get_pixmap(
                matrix=fitz.Matrix(
                    2,
                    2,
                ),
                alpha=False,
            )

            extension = (
                "jpg"
                if image_format in (
                    "jpg",
                    "jpeg",
                )
                else "png"
            )

            output_path = os.path.join(
                output_dir,
                f"page_{index}.{extension}",
            )

            pixmap.save(output_path)

            output_files.append(
                output_path
            )

    finally:
        document.close()

    return output_files
