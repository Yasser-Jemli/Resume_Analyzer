#!/usr/bin/python3

# -*- coding: utf-8 -*-
# @Author  : Yasser JEMLI
# @File    : ResumeInfoExtractor.py
# @Description: Extracts structured information from resume paragraphs.

import re
import json
import os
from pathlib import Path

class ResumeInfoExtractor:
    def __init__(self, paragraphs):
        if not paragraphs:
            raise ValueError("No paragraphs provided")
            
        # Convert to list if string is passed
        if isinstance(paragraphs, str):
            self.paragraphs = [p for p in paragraphs.split('\n\n') if p.strip()]
        else:
            self.paragraphs = [p for p in paragraphs if p.strip()]
            
        if not self.paragraphs:
            raise ValueError("No valid paragraphs after processing")
            
        self.text = "\n".join(self.paragraphs)
        print(f"Debug: Loaded {len(self.paragraphs)} paragraphs")
        
        self.skills_file = Path(__file__).parent.parent / 'assets' / 'skills_keywords.json'
        self.experience_file = Path(__file__).parent.parent / 'assets' / 'experience_keywords.json'
        self.education_file = Path(__file__).parent.parent / 'assets' / 'education_keywords.json'
        self.skill_keywords = self._load_skills()
        self.experience_keywords = self._load_experience_keywords()
        self.education_keywords = self._load_education_keywords()
        print(f"Debug: Loaded {len(self.skill_keywords)} skills")

    def _load_skills(self):
        """Load skills from JSON file"""
        try:
            with open(self.skills_file, 'r') as f:
                skills_data = json.load(f)
                # Flatten the dictionary of skill categories into a single list
                return [skill.lower() for category in skills_data.values() for skill in category]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading skills file: {e}")
            return []

    def _load_experience_keywords(self):
        """Load experience keywords from JSON file"""
        try:
            with open(self.experience_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading experience keywords: {str(e)}")
            return {
                "section_headers": [],
                "date_patterns": [],
                "position_indicators": [],
                "company_indicators": [],
                "action_verbs": []
            }

    def _load_education_keywords(self):
        """Load education keywords from JSON file"""
        try:
            with open(self.education_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading education keywords: {str(e)}")
            return {
                "section_headers": [],
                "degree_types": {},
                "fields": [],
                "institutions": []
            }

    def extract_name(self):
        # Naive assumption: first non-empty line is the name
        for line in self.text.splitlines():
            if line.strip() and not any(char.isdigit() for char in line):
                return line.strip()
        return "Name not found"

    def extract_emails(self):
        return re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", self.text)

    def extract_phone_numbers(self):
        """Extract phone numbers with improved validation"""
        phone_patterns = [
            # International format with country code
            r'(?:\+\d{1,3}[-\s]?)?\d{8,12}',
            # Format: +XXX XXXXXXXX
            r'\+\d{1,3}\s\d{8}',
            # Common Tunisian format
            r'\+216\s\d{8}'
        ]
        
        found_numbers = []
        
        for para in self.paragraphs:
            for pattern in phone_patterns:
                matches = re.finditer(pattern, para)
                for match in matches:
                    number = match.group().strip()
                    # Additional validation
                    if self._is_valid_phone(number):
                        found_numbers.append(number)
        
        # Remove duplicates while maintaining order
        unique_numbers = list(dict.fromkeys(found_numbers))
        
        return unique_numbers if unique_numbers else ["No phone number found"]

    def _is_valid_phone(self, number):
        """Validate phone number"""
        # Remove all non-digit characters except '+'
        cleaned = ''.join(c for c in number if c.isdigit() or c == '+')
        
        # Basic validation rules
        if not cleaned:
            return False
            
        # Must start with + or digit
        if not (cleaned.startswith('+') or cleaned[0].isdigit()):
            return False
            
        # Check length (including country code)
        if len(cleaned) < 8 or len(cleaned) > 15:
            return False
            
        # If starts with +, must have proper country code
        if cleaned.startswith('+'):
            # For Tunisia (+216)
            if cleaned.startswith('+216'):
                return len(cleaned) == 12  # +216 + 8 digits
                
        # Must contain only digits after potential '+'
        if not cleaned[1:].isdigit():
            return False
            
        # Reject if contains year-like numbers
        if re.search(r'[12]\d{3}', cleaned):
            return False
            
        return True

    def extract_skills(self):
        """Extract skills from resume text using loaded keywords"""
        found_skills = []
        for skill in self.skill_keywords:
            if re.search(r'\b' + re.escape(skill) + r'\b', self.text.lower()):
                found_skills.append(skill)
        return found_skills

    def extract_experience(self):
        """Extract work experience using keywords from JSON file"""
        experience_sections = []
        current_section = []
        in_experience_section = False
        
        lines = self.text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check section headers
            if any(header.lower() in line.lower() 
                   for header in self.experience_keywords['section_headers']):
                in_experience_section = True
                if current_section:
                    experience_sections.append(' '.join(current_section))
                    current_section = []
                continue
                
            # Identify experience entries using position and company indicators
            has_position = any(indicator.lower() in line.lower() 
                             for indicator in self.experience_keywords['position_indicators'])
            has_company = any(indicator.lower() in line.lower() 
                             for indicator in self.experience_keywords['company_indicators'])
            
            if in_experience_section and (has_position or has_company):
                if current_section:
                    experience_sections.append(' '.join(current_section))
                current_section = [line]
                continue
                
            if in_experience_section:
                current_section.append(line)
        
        # Add final section
        if current_section:
            experience_sections.append(' '.join(current_section))
        
        # Clean and format sections
        cleaned_sections = []
        for section in experience_sections:
            cleaned = ' '.join(section.split())
            cleaned = re.sub(r'---\s*Paragraph\s*\d+\s*---', '', cleaned)
            if cleaned:
                cleaned_sections.append(cleaned)
        
        return cleaned_sections if cleaned_sections else ["No experience found"]

    def extract_education(self):
        """Extract education information using keywords from JSON file"""
        education_sections = []
        current_section = []
        in_education_section = False
        
        lines = self.text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check section headers
            if any(header.lower() in line.lower() 
                   for header in self.education_keywords['section_headers']):
                in_education_section = True
                if current_section:
                    education_sections.append(' '.join(current_section))
                    current_section = []
                continue
            
            # Check if we've hit another major section
            if line.isupper() and len(line) > 2 and not any(header.lower() in line.lower() 
                   for header in self.education_keywords['section_headers']):
                if in_education_section:
                    if current_section:
                        education_sections.append(' '.join(current_section))
                    in_education_section = False
                continue
            
            # Collect education information
            if in_education_section:
                # Check for degree types
                is_education_line = False
                for degree_type, keywords in self.education_keywords['degree_types'].items():
                    if any(keyword.lower() in line.lower() for keyword in keywords):
                        is_education_line = True
                        break
                
                # Check for educational institutions
                if any(inst.lower() in line.lower() for inst in self.education_keywords['institutions']):
                    is_education_line = True
                
                # Check for fields of study
                if any(field.lower() in line.lower() for field in self.education_keywords['fields']):
                    is_education_line = True
                
                if is_education_line:
                    if current_section:
                        education_sections.append(' '.join(current_section))
                    current_section = [line]
                else:
                    current_section.append(line)
        
        # Add final section
        if current_section and in_education_section:
            education_sections.append(' '.join(current_section))
        
        # Clean and format sections
        cleaned_sections = []
        for section in education_sections:
            cleaned = ' '.join(section.split())
            cleaned = re.sub(r'---\s*Paragraph\s*\d+\s*---', '', cleaned)
            if cleaned:
                cleaned_sections.append(cleaned)
        
        return cleaned_sections if cleaned_sections else ["No education found"]

    def extract_all(self):
        """Extract all information from the resume"""
        try:
            results = {
                "Name": self.extract_name(),
                "Email": self.extract_emails(),
                "Phone": self.extract_phone_numbers(),
                "Skills": self.extract_skills(),
                "Experience": self.extract_experience(),
                "Education": self.extract_education()
            }
            print("Debug: Extraction complete")
            return results
        except Exception as e:
            print(f"Error in extract_all: {str(e)}")
            return None
