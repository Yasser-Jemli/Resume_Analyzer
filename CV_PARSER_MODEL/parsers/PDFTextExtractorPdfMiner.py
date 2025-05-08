#!/usr/bin/python3

# -*- coding: utf-8 -*-
# @Time    : 2025/05/08
# @Author  : Yasser JEMLI
# @File    : PDFTextExtractorPdfMiner.py
# @Software: Vscode
# @Description: This module extracts text from each text box using pdfminer3.


import io
from pdfminer3.layout import LAParams, LTTextBox, LTTextContainer
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.pdfparser import PDFSyntaxError
from pdfminer3.pdfdocument import PDFTextExtractionNotAllowed
from pdfminer3.pdfparser import PDFParser
from pdfminer3.pdfdocument import PDFDocument

class PDFTextExtractorPdfMiner:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.paragraphs = []

    def load_pdf(self):
        try:
            with open(self.pdf_path, 'rb') as f:
                parser = PDFParser(f)
                document = PDFDocument(parser)
                if not document.is_extractable:
                    raise PDFTextExtractionNotAllowed("Text extraction not allowed")

                rsrcmgr = PDFResourceManager()
                laparams = LAParams()
                device = PDFPageAggregator(rsrcmgr, laparams=laparams)
                interpreter = PDFPageInterpreter(rsrcmgr, device)

                for page in PDFPage.create_pages(document):
                    interpreter.process_page(page)
                    layout = device.get_result()
                    for element in layout:
                        if isinstance(element, (LTTextBox, LTTextContainer)):
                            text = element.get_text().strip()
                            if text:
                                self.paragraphs.append(text)
            print(f"Successfully extracted text boxes from: {self.pdf_path}")
        except (FileNotFoundError, PDFSyntaxError, PDFTextExtractionNotAllowed) as e:
            print(f"Error processing PDF: {e}")
            self.paragraphs = []

    def save_extracted_paragraphs(self, output_path):
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for para in self.paragraphs:
                    f.write(para + "\n\n")
            print(f"Extracted paragraphs saved to: {output_path}")
        except Exception as e:
            print(f"Failed to save extracted paragraphs: {e}")

    def extract_paragraphs(self, output_path=None):
        self.load_pdf()
        if output_path:
            self.save_extracted_paragraphs(output_path)
        return self.paragraphs

    def close(self):
        # No persistent resource to close in this implementation
        pass


# Example usage
# if __name__ == "__main__":
#     extractor = PDFTextExtractorPdfMiner("example.pdf")
#     paragraphs = extractor.extract_paragraphs()
#     for i, para in enumerate(paragraphs, 1):
#         print(f"\n--- Paragraph {i} ---\n{para}")
