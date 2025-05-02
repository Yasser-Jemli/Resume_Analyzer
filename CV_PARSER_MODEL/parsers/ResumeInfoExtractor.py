# -*- coding: utf-8 -*-
# @Author  : Yasser JEMLI
# @File    : ResumeInfoExtractor.py
# @Description: Extracts structured information from resume paragraphs.

#!/usr/bin/python3
import re

class ResumeInfoExtractor:
    def __init__(self, paragraphs):
        self.paragraphs = paragraphs
        self.text = "\n".join(paragraphs)

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
        skill_keywords = ["Python", "Java", "SQL", "Machine Learning", "C++", "Excel", "Docker", "Git"]
        found = set()
        for word in skill_keywords:
            if re.search(rf"\b{re.escape(word)}\b", self.text, re.IGNORECASE):
                found.add(word)
        return list(found)

    def extract_experience(self):
        experience_section = []
        capture = False
        for para in self.paragraphs:
            if "experience" in para.lower():
                capture = True
            elif capture and (para.strip() == "" or len(para.split()) < 3):
                break
            if capture:
                experience_section.append(para)
        return "\n".join(experience_section) or "Experience section not found."

    def extract_all(self):
        return {
            "Name": self.extract_name(),
            "Email(s)": self.extract_emails(),
            "Phone(s)": self.extract_phone_numbers(),
            "Skills": self.extract_skills(),
            "Experience": self.extract_experience()
        }
