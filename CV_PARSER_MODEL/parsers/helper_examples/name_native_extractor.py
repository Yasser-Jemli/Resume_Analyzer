#!/usr/bin/python3

# -*- coding: utf-8 -*-
# @Author  : Yasser JEMLI
# @File    : name_native_extractor.py
# @Description: Extracts the name from resume paragraphs.

# @Requirements pip install PyPDF2

import re
from PyPDF2 import PdfReader

def extract_names_from_pdf(pdf_path):
    """
    Extracts potential names from a PDF file using basic heuristics.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        list: A list of potential full names found in the PDF.
    """
    names = set()
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

            # Basic splitting into words
            words = re.findall(r'\b[A-Za-z]+\b', text)

            potential_names = []
            for i in range(len(words)):
                if words[i][0].isupper():  # Check if the word starts with a capital letter
                    potential_names.append(words[i])

            # Look for sequences of capitalized words (potential full names)
            name_candidates = []
            i = 0
            while i < len(potential_names):
                current_name = [potential_names[i]]
                j = i + 1
                while j < len(potential_names) and potential_names[j][0].isupper():
                    current_name.append(potential_names[j])
                    j += 1
                if len(current_name) >= 2:  # Consider at least two capitalized words as a potential name
                    name_candidates.append(" ".join(current_name))
                i = j

            # Further refinement (very basic - can be improved significantly)
            common_titles = ["Mr", "Ms", "Dr", "Prof"]
            refined_names = set()
            for candidate in name_candidates:
                parts = candidate.split()
                # Remove common titles if present at the beginning
                if parts[0] in common_titles and len(parts) > 1:
                    refined_names.add(" ".join(parts[1:]))
                else:
                    refined_names.add(candidate)

            return list(refined_names)

    except FileNotFoundError:
        print(f"Error: PDF file not found at {pdf_path}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage:
if __name__ == "__main__":
    pdf_file = "name_native_extractor_example.pdf"  # Replace with the actual path to your PDF file

    # Create a dummy PDF for testing
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(pdf_file)
    c.drawString(100, 750, "John Doe")
    c.drawString(100, 700, "Jane Smith")
    c.drawString(100, 650, "Meeting with Dr. Robert Jones")
    c.drawString(100, 600, "Agenda item: Discussion led by Ms. Alice Brown.")
    c.save()

    extracted_names = extract_names_from_pdf(pdf_file)
    print("Potential names extracted:", extracted_names)