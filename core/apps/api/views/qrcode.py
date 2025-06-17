import qrcode
import base64
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
from config.env import env
import hashlib



BASE_URL = env("BASE_URL") 


def encode_id_base64(item_id):
    item_str = str(item_id)
    hash_part = hashlib.sha256(item_str.encode()).hexdigest()[:6]  
    full_str = f"{hash_part}-{item_str}"  
    encoded = base64.urlsafe_b64encode(full_str.encode()).decode()
    return encoded.rstrip("=")  



def add_qr_to_each_page(original_pdf_path, item_id, base_url=BASE_URL):

    encoded_id = encode_id_base64(item_id)
    qr_url = f"{base_url}/{encoded_id}"
    print(qr_url)

    qr_img = qrcode.make(qr_url).convert("RGB")
    img_buffer = BytesIO()
    qr_img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    qr_image_reader = ImageReader(Image.open(img_buffer))

    original_reader = PdfReader(original_pdf_path)
    writer = PdfWriter()

    for page in original_reader.pages:
        overlay_buffer = BytesIO()
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)

        c = canvas.Canvas(overlay_buffer, pagesize=(page_width, page_height))
        qr_size = 100
        x = page_width - qr_size - 20
        y = 20
        c.drawImage(qr_image_reader, x, y, width=qr_size, height=qr_size)
        c.showPage()
        c.save()
        overlay_buffer.seek(0)

        overlay_pdf = PdfReader(overlay_buffer)
        overlay_page = overlay_pdf.pages[0]

        page.merge_page(overlay_page)
        writer.add_page(page)

    output = BytesIO()
    writer.write(output)
    output.seek(0)
    return output
