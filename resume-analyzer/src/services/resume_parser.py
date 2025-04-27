import os
import spacy
import nltk
import pandas as pd
from pyresparser import ResumeParser
import io
from ..models.resume import Resume

class ResumeParserService:
    def __init__(self):
        pass

    def parse_resume(self, file_path):
        """
        Parse resume file and extract relevant information
        """
        try:
            # Load resume content
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Basic parsing for now - can be enhanced later
            parsed_data = {
                'filename': os.path.basename(file_path),
                'content': content,
                'analyzed_data': {}  # Placeholder for analyzed data
            }
            
            return parsed_data
            
        except Exception as e:
            print(f"Error parsing resume: {str(e)}")
            return None

    def read_pdf(self, file):
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        with open(file, 'rb') as fh:
            for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                page_interpreter.process_page(page)
            text = fake_file_handle.getvalue()

        converter.close()
        fake_file_handle.close()
        return text