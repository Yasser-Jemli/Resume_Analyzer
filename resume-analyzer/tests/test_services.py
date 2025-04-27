import unittest
from src.services.pdf_service import read_pdf, process_pdf

class TestPDFService(unittest.TestCase):

    def test_read_pdf(self):
        # Test reading a PDF file
        pdf_path = 'path/to/sample.pdf'
        content = read_pdf(pdf_path)
        self.assertIsInstance(content, str)  # Ensure the content is a string

    def test_process_pdf(self):
        # Test processing a PDF file
        pdf_content = "Sample PDF content"
        processed_data = process_pdf(pdf_content)
        self.assertIsInstance(processed_data, dict)  # Ensure the processed data is a dictionary

if __name__ == '__main__':
    unittest.main()