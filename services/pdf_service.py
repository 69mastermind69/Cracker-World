import os

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter
from PIL import Image

import fitz


def text_to_pdf(
    text,
    output_path,
    title="Text Document",
):
    c = canvas.Canvas(
        output_path,
        pagesize=A4,
    )

    width, height = A4
    margin = 50
    line_height = 16
    y = height - margin

    c.setTitle(title)

    for paragraph in text.splitlines():

        if not paragraph.strip():
            y -= line_height

            if y < margin:
                c.showPage()
                y = height - margin

            continue

        words = paragraph.split()
        current_line = ""

        for word in words:

            test_line = (
                word
                if not current_line
                else current_line + " " + word
            )

            if c.stringWidth(
                test_line,
                "Helvetica",
                11,
            ) <= width - 2 * margin:

                current_line = test_line

            else:

                c.setFont(
                    "Helvetica",
                    11,
                )

                c.drawString(
                    margin,
                    y,
                    current_line,
                )

                y -= line_height

                if y < margin:
                    c.showPage()
                    y = height - margin

                current_line = word

        if current_line:

            c.setFont(
                "Helvetica",
                11,
            )

            c.drawString(
                margin,
                y,
                current_line,
            )

            y -= line_height

        if y < margin:
            c.showPage()
            y = height - margin

    c.save()

    return output_path


def images_to_pdf(
    image_paths,
    output_path,
):
    if not image_paths:
        raise ValueError(
            "No images provided."
        )

    processed_images = []

    try:

        for image_path in image_paths:

            img = Image.open(
                image_path
            )

            if img.mode != "RGB":
                img = img.convert("RGB")

            processed_images.append(img)

        first_image = processed_images[0]
        remaining_images = (
            processed_images[1:]
        )

        first_image.save(
            output_path,
            "PDF",
            resolution=100.0,
            save_all=True,
            append_images=remaining_images,
        )

    finally:

        for img in processed_images:
            try:
                img.close()
            except Exception:
                pass

    return output_path


def merge_pdfs(
    pdf_paths,
    output_path,
):
    if not pdf_paths:
        raise ValueError(
            "No PDF files provided."
        )

    writer = PdfWriter()

    for pdf_path in pdf_paths:

        reader = PdfReader(
            pdf_path
        )

        for page in reader.pages:
            writer.add_page(page)

    with open(
        output_path,
        "wb",
    ) as output_file:

        writer.write(
            output_file
        )

    return output_path


def split_pdf(
    pdf_path,
    output_dir,
):
    os.makedirs(
        output_dir,
        exist_ok=True,
    )

    reader = PdfReader(
        pdf_path
    )

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

            writer.write(
                output_file
            )

        output_files.append(
            output_path
        )

    return output_files


def pdf_to_text(
    pdf_path,
):
    reader = PdfReader(
        pdf_path
    )

    pages = []

    for page in reader.pages:

        text = (
            page.extract_text()
            or ""
        )

        pages.append(text)

    return "\n\n".join(pages)


def protect_pdf(
    pdf_path,
    output_path,
    password,
):
    if not password:
        raise ValueError(
            "Password cannot be empty."
        )

    reader = PdfReader(
        pdf_path
    )

    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(
        password
    )

    with open(
        output_path,
        "wb",
    ) as output_file:

        writer.write(
            output_file
        )

    return output_path


def pdf_to_images(
    pdf_path,
    output_dir,
    dpi=150,
):
    """
    Convert every PDF page into a PNG image.
    """

    if not os.path.isfile(
        pdf_path
    ):
        raise FileNotFoundError(
            "PDF file not found."
        )

    os.makedirs(
        output_dir,
        exist_ok=True,
    )

    pdf_document = fitz.open(
        pdf_path
    )

    output_files = []

    try:

        scale = dpi / 72.0

        matrix = fitz.Matrix(
            scale,
            scale,
        )

        for page_number in range(
            len(pdf_document)
        ):

            page = pdf_document[
                page_number
            ]

            pixmap = page.get_pixmap(
                matrix=matrix,
                alpha=False,
            )

            output_path = os.path.join(
                output_dir,
                f"page_{page_number + 1}.png",
            )

            pixmap.save(
                output_path
            )

            output_files.append(
                output_path
            )

    finally:

        pdf_document.close()

    return output_files


def get_pdf_info(
    pdf_path,
):
    reader = PdfReader(
        pdf_path
    )

    return {
        "pages": len(
            reader.pages
        ),
        "encrypted": (
            reader.is_encrypted
        ),
        "size_bytes": os.path.getsize(
            pdf_path
        ),
    }
