import io
import base64
import os
from werkzeug.utils import secure_filename
from pdfminer.high_level import extract_text
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from ..config.settings import Settings

def read_pdf(file_path):
    resource_manager = PDFResourceManager()
    output = io.StringIO()
    laparams = LAParams()
    device = TextConverter(resource_manager, output, laparams=laparams)

    with open(file_path, 'rb') as file:
        interpreter = PDFPageInterpreter(resource_manager, device)
        for page in PDFPage.get_pages(file):
            interpreter.process_page(page)

    text = output.getvalue()
    device.close()
    output.close()
    return text

def pdf_to_base64(file_path):
    with open(file_path, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode('utf-8')
    return encoded_string

def save_uploaded_file(file):
    """
    Save uploaded file to the configured upload folder
    """
    filename = secure_filename(file.filename)
    file_path = os.path.join(Settings.UPLOAD_FOLDER, filename)
    file.save(file_path)
    return file_path