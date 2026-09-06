import os

from pypdf import (
    PdfReader,
    PdfWriter,
)

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

import fitz  # PyMuPDF


# ============================================================
# TEXT → PDF
# ============================================================

def text_to_pdf(
    text,
    output_path,
    title="Document",
):
    """
    Convert plain text into a PDF.
    """

    if not text or not text.strip():
        raise ValueError("Text is empty.")

    os.makedirs(
        os.path.dirname(output_path) or ".",
        exist_ok=True,
    )

    page_width, page_height = A4

    pdf = canvas.Canvas(
        output_path,
        pagesize=A4,
    )

    pdf.setTitle(title)

    left_margin = 50
    right_margin = 50
    top_margin = page_height - 55
    bottom_margin = 50

    font_name = "Helvetica"
    font_size = 11
    line_height = 16

    pdf.setFont(
        font_name,
        font_size,
    )

    x = left_margin
    y = top_margin

    max_width = (
        page_width
        - left_margin
        - right_margin
    )

    for paragraph in text.splitlines():

        # Empty line
        if not paragraph.strip():
            y -= line_height

            if y <= bottom_margin:
                pdf.showPage()

                pdf.setFont(
                    font_name,
                    font_size,
                )

                y = top_margin

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
                pdf.drawString(
                    x,
                    y,
                    current_line,
                )

                y -= line_height
                current_line = word

                if y <= bottom_margin:
                    pdf.showPage()

                    pdf.setFont(
                        font_name,
                        font_size,
                    )

                    y = top_margin

        if current_line:
            pdf.drawString(
                x,
                y,
                current_line,
            )

            y -= line_height

        if y <= bottom_margin:
            pdf.showPage()

            pdf.setFont(
                font_name,
                font_size,
            )

            y = top_margin

    pdf.save()

    return output_path


# ============================================================
# IMAGES → PDF
# ============================================================

def images_to_pdf(
    image_paths,
    output_path,
):
    """
    Convert one or more images into a single PDF.
    """

    if not image_paths:
        raise ValueError(
            "No images provided."
        )

    valid_images = [
        path
        for path in image_paths
        if os.path.isfile(path)
    ]

    if not valid_images:
        raise ValueError(
            "No valid image files found."
        )

    os.makedirs(
        os.path.dirname(output_path) or ".",
        exist_ok=True,
    )

    pdf = canvas.Canvas(
        output_path,
        pagesize=A4,
    )

    page_width, page_height = A4

    margin = 30

    for image_path in valid_images:

        try:
            image = fitz.Pixmap(image_path)

            width = image.width
            height = image.height

            if width <= 0 or height <= 0:
                continue

            available_width = (
                page_width - 2 * margin
            )

            available_height = (
                page_height - 2 * margin
            )

            scale = min(
                available_width / width,
                available_height / height,
            )

            draw_width = width * scale
            draw_height = height * scale

            x = (
                page_width - draw_width
            ) / 2

            y = (
                page_height - draw_height
            ) / 2

            pdf.drawImage(
                image_path,
                x,
                y,
                width=draw_width,
                height=draw_height,
                preserveAspectRatio=True,
                anchor="c",
            )

            pdf.showPage()

        except Exception:
            continue

    pdf.save()

    return output_path


# ============================================================
# MERGE PDF
# ============================================================

def merge_pdfs(
    pdf_paths,
    output_path,
):
    """
    Merge multiple PDF files.
    """

    if not pdf_paths:
        raise ValueError(
            "No PDF files provided."
        )

    writer = PdfWriter()

    valid_count = 0

    for pdf_path in pdf_paths:

        if not os.path.isfile(pdf_path):
            continue

        reader = PdfReader(pdf_path)

        for page in reader.pages:
            writer.add_page(page)

        valid_count += 1

    if valid_count == 0:
        raise ValueError(
            "No valid PDF files found."
        )

    os.makedirs(
        os.path.dirname(output_path) or ".",
        exist_ok=True,
    )

    with open(
        output_path,
        "wb",
    ) as output_file:
        writer.write(output_file)

    return output_path


# ============================================================
# SPLIT PDF
# ============================================================

def split_pdf(
    input_path,
    output_dir,
):
    """
    Split PDF into individual page PDFs.
    """

    if not os.path.isfile(input_path):
        raise FileNotFoundError(
            "PDF file not found."
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
        ) as output_file:
            writer.write(output_file)

        output_files.append(
            output_path
        )

    return output_files


# ============================================================
# PDF → TEXT
# ============================================================

def pdf_to_text(
    input_path,
):
    """
    Extract text from PDF.
    """

    if not os.path.isfile(input_path):
        raise FileNotFoundError(
            "PDF file not found."
        )

    document = fitz.open(input_path)

    try:
        pages = []

        for page in document:
            text = page.get_text()

            if text:
                pages.append(text)

        return "\n\n".join(pages)

    finally:
        document.close()


# ============================================================
# PROTECT PDF
# ============================================================

def protect_pdf(
    input_path,
    output_path,
    password,
):
    """
    Password-protect a PDF.
    """

    if not os.path.isfile(input_path):
        raise FileNotFoundError(
            "PDF file not found."
        )

    if not password:
        raise ValueError(
            "Password cannot be empty."
        )

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(
        password,
        use_128bit=True,
    )

    os.makedirs(
        os.path.dirname(output_path) or ".",
        exist_ok=True,
    )

    with open(
        output_path,
        "wb",
    ) as output_file:
        writer.write(output_file)

    return output_path


# ============================================================
# PDF → IMAGES
# ============================================================

def pdf_to_images(
    input_path,
    output_dir,
    dpi=150,
):
    """
    Convert every PDF page into PNG.
    """

    if not os.path.isfile(input_path):
        raise FileNotFoundError(
            "PDF file not found."
        )

    os.makedirs(
        output_dir,
        exist_ok=True,
    )

    document = fitz.open(input_path)

    output_files = []

    try:
        scale = dpi / 72

        matrix = fitz.Matrix(
            scale,
            scale,
        )

        for index, page in enumerate(
            document,
            start=1,
        ):
            pixmap = page.get_pixmap(
                matrix=matrix,
                alpha=False,
            )

            output_path = os.path.join(
                output_dir,
                f"page_{index}.png",
            )

            pixmap.save(output_path)

            output_files.append(
                output_path
            )

    finally:
        document.close()

    return output_files
