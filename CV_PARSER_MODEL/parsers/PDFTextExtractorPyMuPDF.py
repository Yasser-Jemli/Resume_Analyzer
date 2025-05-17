#!/usr/bin/python3

# -*- coding: utf-8 -*-
# @Time    : 2023/10/12 16:00
# @Author  : Yasser JEMLI
# @File    : PDFTextExtractorPyMuPDF.py
# @Software: Vscode
# @Description: This module provides a class to extract text from PDF files.

import fitz  # PyMuPDF

class PDFTextExtractorPyMuPDF:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.doc = None

    def load_pdf(self):
        try:
            self.doc = fitz.open(self.pdf_path)
            print(f"PDF loaded successfully: {self.pdf_path}")
        except Exception as e:
            print(f"Failed to load PDF: {e}")
            self.doc = None

    def save_extracted_paragraphs(self, paragraphs, output_path):
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for para in paragraphs:
                    f.write(para + "\n\n")
            print(f"Extracted paragraphs saved to: {output_path}")
        except Exception as e:
            print(f"Failed to save extracted paragraphs: {e}")

    def extract_paragraphs(self, output_path=None):
        if not self.doc:
            self.load_pdf()
        if not self.doc:
            return []

        paragraphs = []
        for page_num in range(len(self.doc)):
            page = self.doc.load_page(page_num)
            text = page.get_text("text")
            page_paragraphs = self._split_into_paragraphs(text)
            paragraphs.extend(page_paragraphs)
        return self.save_extracted_paragraphs(paragraphs, output_path) if output_path else paragraphs


    def _split_into_paragraphs(self, text):
        # Split by two or more newlines as paragraph separator
        return [para.strip() for para in text.split('\n\n') if para.strip()]

    def close(self):
        if self.doc:
            self.doc.close()


# Example usage
# if __name__ == "__main__":
#     extractor = PDFTextExtractor("example.pdf")
#     paragraphs = extractor.extract_paragraphs()

#     for i, para in enumerate(paragraphs, 1):
#         print(f"\n--- Paragraph {i} ---\n{para}")

#     extractor.close()