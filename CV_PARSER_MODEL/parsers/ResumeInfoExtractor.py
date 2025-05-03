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
        self.skill_keywords = self._load_skills()
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

    def extract_name(self):
        # Naive assumption: first non-empty line is the name
        for line in self.text.splitlines():
            if line.strip() and not any(char.isdigit() for char in line):
                return line.strip()
        return "Name not found"

    def extract_emails(self):
        return re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", self.text)

    def extract_phone_numbers(self):
        return re.findall(r"(\+?\d[\d\s\-]{8,}\d)", self.text)

    def extract_skills(self):
        """Extract skills from resume text using loaded keywords"""
        found_skills = []
        for skill in self.skill_keywords:
            if re.search(r'\b' + re.escape(skill) + r'\b', self.text.lower()):
                found_skills.append(skill)
        return found_skills

    def extract_experience(self):
        experience_markers = ['experience', 'work history', 'employment']
        experience_text = []
        
        for para in self.paragraphs:
            if any(marker in para.lower() for marker in experience_markers):
                experience_text.append(para)
        
        return experience_text if experience_text else ["No experience found"]

    def extract_all(self):
        """Extract all information from the resume"""
        try:
            results = {
                "Name": self.extract_name(),
                "Email": self.extract_emails(),
                "Phone": self.extract_phone_numbers(),
                "Skills": self.extract_skills(),
                "Experience": self.extract_experience()
            }
            print("Debug: Extraction complete")
            return results
        except Exception as e:
            print(f"Error in extract_all: {str(e)}")
            return None
