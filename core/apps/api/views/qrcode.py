import qrcode
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

from reportlab.lib.utils import ImageReader

def add_qr_to_pdf(original_pdf_path, output_pdf_path, car_instance):
    qr_text = f"https://yourdomain.com{car_instance.get_absolute_url()}"
    qr_img = qrcode.make(qr_text)
    img_buffer = BytesIO()
    qr_img.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    qr_img_reader = ImageReader(img_buffer)  

    qr_pdf_buffer = BytesIO()
    c = canvas.Canvas(qr_pdf_buffer, pagesize=(595, 842))  
    c.drawInlineImage(qr_img_reader, 450, 50, 100, 100) 
    c.showPage()
    c.save()
    qr_pdf_buffer.seek(0)

    original_reader = PdfReader(original_pdf_path)
    qr_reader = PdfReader(qr_pdf_buffer)
    writer = PdfWriter()

    for page in original_reader.pages:
        writer.add_page(page)

    writer.add_page(qr_reader.pages[0])

    with open(output_pdf_path, 'wb') as out_file:
        writer.write(out_file)
