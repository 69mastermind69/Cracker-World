import os

import fitz
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def text_to_pdf(
    text,
    output_path,
    title="Document",
):
    output_dir = os.path.dirname(output_path)

    if output_dir:
        os.makedirs(
            output_dir,
            exist_ok=True,
        )

    pdf = canvas.Canvas(
        output_path,
        pagesize=A4,
    )

    width, height = A4

    pdf.setTitle(title)

    x = 50
    y = height - 60
    line_height = 18

    for paragraph in str(text).splitlines():
        if not paragraph:
            y -= line_height

            if y < 50:
                pdf.showPage()
                y = height - 60

            continue

        words = paragraph.split()
        current_line = ""

        for word in words:
            test_line = (
                f"{current_line} {word}"
                if current_line
                else word
            )

            if (
                pdf.stringWidth(
                    test_line,
                    "Helvetica",
                    11,
                )
                > width - 100
            ):
                pdf.setFont(
                    "Helvetica",
                    11,
                )
                pdf.drawString(
                    x,
                    y,
                    current_line,
                )

                y -= line_height
                current_line = word

                if y < 50:
                    pdf.showPage()
                    y = height - 60

            else:
                current_line = test_line

        if current_line:
            pdf.setFont(
                "Helvetica",
                11,
            )
            pdf.drawString(
                x,
                y,
                current_line,
            )

            y -= line_height

        if y < 50:
            pdf.showPage()
            y = height - 60

    pdf.save()

    return output_path


def images_to_pdf(
    image_paths,
    output_path,
):
    if not image_paths:
        raise ValueError(
            "No images provided."
        )

    output_dir = os.path.dirname(output_path)

    if output_dir:
        os.makedirs(
            output_dir,
            exist_ok=True,
        )

    document = fitz.open()

    try:
        for image_path in image_paths:
            if not os.path.isfile(image_path):
                continue

            image = fitz.Pixmap(image_path)

            page = document.new_page(
                width=image.width,
                height=image.height,
            )

            page.insert_image(
                page.rect,
                filename=image_path,
            )

        if document.page_count == 0:
            raise ValueError(
                "No valid images found."
            )

        document.save(output_path)

    finally:
        document.close()

    return output_path


def merge_pdfs(
    pdf_paths,
    output_path,
):
    if not pdf_paths:
        raise ValueError(
            "No PDF files provided."
        )

    output_dir = os.path.dirname(output_path)

    if output_dir:
        os.makedirs(
            output_dir,
            exist_ok=True,
        )

    writer = PdfWriter()

    for pdf_path in pdf_paths:
        if not os.path.isfile(pdf_path):
            continue

        reader = PdfReader(pdf_path)

        for page in reader.pages:
            writer.add_page(page)

    if len(writer.pages) == 0:
        raise ValueError(
            "No valid PDF pages found."
        )

    with open(
        output_path,
        "wb",
    ) as file:
        writer.write(file)

    return output_path


def split_pdf(
    input_path,
    output_dir,
):
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
        ) as file:
            writer.write(file)

        output_files.append(
            output_path
        )

    return output_files


def pdf_to_text(
    input_path,
    output_path=None,
):
    if not os.path.isfile(input_path):
        raise FileNotFoundError(
            "PDF file not found."
        )

    reader = PdfReader(input_path)

    text_parts = []

    for page in reader.pages:
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""

        text_parts.append(text)

    text = "\n\n".join(
        text_parts
    )

    if output_path:
        output_dir = os.path.dirname(
            output_path
        )

        if output_dir:
            os.makedirs(
                output_dir,
                exist_ok=True,
            )

        with open(
            output_path,
            "w",
            encoding="utf-8",
        ) as file:
            file.write(text)

        return output_path

    return text


def protect_pdf(
    input_path,
    output_path,
    password,
):
    if not os.path.isfile(input_path):
        raise FileNotFoundError(
            "PDF file not found."
        )

    if not password:
        raise ValueError(
            "Password cannot be empty."
        )

    output_dir = os.path.dirname(output_path)

    if output_dir:
        os.makedirs(
            output_dir,
            exist_ok=True,
        )

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)

    with open(
        output_path,
        "wb",
    ) as file:
        writer.write(file)

    return output_path


def pdf_to_images(
    input_path,
    output_dir,
    image_format="png",
):
    if not os.path.isfile(input_path):
        raise FileNotFoundError(
            "PDF file not found."
        )

    os.makedirs(
        output_dir,
        exist_ok=True,
    )

    image_format = (
        image_format.lower()
    )

    if image_format not in {
        "png",
        "jpg",
        "jpeg",
    }:
        image_format = "png"

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
                )
            )

            extension = (
                "jpg"
                if image_format
                in {"jpg", "jpeg"}
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
