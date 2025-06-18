import qrcode
import base64
import time
import hashlib
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
from config.env import env

BASE_URL = env("BASE_URL")


def encode_id_base64(item_id):
    item_str = str(item_id)
    hash_part = hashlib.sha256(item_str.encode()).hexdigest()[:6]
    full_str = f"{hash_part}-{item_str}"
    encoded = base64.urlsafe_b64encode(full_str.encode()).decode()
    return encoded.rstrip("=")


def create_qr_overlay(page_width, page_height, qr_image_reader):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(page_width, page_height))
    qr_size = 100
    x = page_width - qr_size - 20
    y = 20
    c.drawImage(qr_image_reader, x, y, width=qr_size, height=qr_size)
    c.showPage()
    c.save()
    buffer.seek(0)
    return PdfReader(buffer).pages[0]


def add_qr_to_each_page(original_pdf_path, item_id, base_url=BASE_URL):
    start_time = time.perf_counter()

    encoded_id = encode_id_base64(item_id)
    qr_url = f"{base_url}/qr/show/{encoded_id}"
    print(f"[QR URL]: {qr_url}")

    qr_img = qrcode.make(qr_url).convert("RGB").resize((100, 100))
    img_buffer = BytesIO()
    qr_img.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    qr_image_reader = ImageReader(Image.open(img_buffer))

    original_reader = PdfReader(original_pdf_path)
    writer = PdfWriter()

    if not original_reader.pages:
        raise ValueError("PDF faylda sahifa yo‘q!")

    first_page = original_reader.pages[0]
    page_width = float(first_page.mediabox.width)
    page_height = float(first_page.mediabox.height)
    overlay_page = create_qr_overlay(page_width, page_height, qr_image_reader)

    for page in original_reader.pages:
        page.merge_page(overlay_page)
        writer.add_page(page)

    output = BytesIO()
    writer.write(output)
    output.seek(0)

    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"[INFO]: {len(original_reader.pages)} sahifaga QR qo‘shildi.")
    print(f"[INFO]: Jarayon {duration:.2f} soniya davom etdi.")

    return output
