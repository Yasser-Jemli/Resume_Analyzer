#!/usr/bin/python3

# -*- coding: utf-8 -*-
# @Time    : 2023/10/12 16:00
# @Author  : Yasser JEMLI
# @File    : PDFTextExtractorPyMuPDF.py
# @Software: Vscode
# @Description: This module provides a class to extract text from PDF files.

import fitz  # PyMuPDF
import logging

class PDFTextExtractorPyMuPDF:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.logger = logging.getLogger(__name__)

    def extract_text(self) -> str:
        """Extract text using PyMuPDF with better formatting"""
        try:
            doc = fitz.open(self.pdf_path)
            text_blocks = []
            
            for page in doc:
                blocks = page.get_text("blocks")
                for b in blocks:
                    if b[4].strip():  # Get clean text content
                        text_blocks.append(b[4].strip())
            
            doc.close()
            return "\n\n".join(text_blocks)
            
        except Exception as e:
            self.logger.error(f"PyMuPDF extraction failed: {e}")
            return ""

    def save_extracted_paragraphs(self, paragraphs, output_path):
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for para in paragraphs:
                    f.write(para + "\n\n")
            print(f"Extracted paragraphs saved to: {output_path}")
        except Exception as e:
            print(f"Failed to save extracted paragraphs: {e}")

    def extract_paragraphs(self, output_path=None):
        paragraphs = self.extract_text().split("\n\n")
        return self.save_extracted_paragraphs(paragraphs, output_path) if output_path else paragraphs

    def close(self):
        pass


# Example usage
# if __name__ == "__main__":
#     extractor = PDFTextExtractor("example.pdf")
#     paragraphs = extractor.extract_paragraphs()

#     for i, para in enumerate(paragraphs, 1):
#         print(f"\n--- Paragraph {i} ---\n{para}")

#     extractor.close()