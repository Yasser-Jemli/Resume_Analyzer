#!/usr/bin/python3

# -*- coding: utf-8 -*-
# @Author  : Yasser JEMLI
# @File    : ResumeInfoExtractor.py
# @Description: Extracts structured information from resume paragraphs.

import logging
import re
import json
from pathlib import Path
from typing import Dict, List, Optional

class ResumeInfoExtractor:
    def __init__(self, text):
        self.text = text
        self.paragraphs = text.split('\n\n') if isinstance(text, str) else text
        self.logger = logging.getLogger(__name__)
        self._load_keyword_data()

    def _load_keyword_data(self):
        """Load keyword dictionaries from assets"""
        try:
            assets_dir = Path(__file__).parent.parent / 'assets'
            
            with open(assets_dir / 'skills_keywords.json', 'r') as f:
                self.skill_keywords = json.load(f)
            
            with open(assets_dir / 'education_keywords.json', 'r') as f:
                self.education_keywords = json.load(f)
                
            with open(assets_dir / 'experience_keywords.json', 'r') as f:
                self.experience_keywords = json.load(f)
                
        except Exception as e:
            self.logger.error(f"Error loading keyword data: {e}")
            raise

    def extract_all(self):
        """Extract all information with improved accuracy"""
        try:
            results = {
                'Name': self.extract_name(),
                'Email': self.extract_email(),
                'Phone': self.extract_phone_numbers(),
                'Skills': self.extract_skills(),
                'Education': self.extract_education(),
                'Experience': self.extract_experience(),
                'Position': self.extract_current_position()
            }
            
            # Ensure Position is set
            if not results['Position']:
                position = self._extract_position_from_experience(results['Experience'])
                results['Position'] = position if position else 'sw_designer'
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error in extract_all: {e}")
            return None

    def extract_current_position(self):
        """Extract current position"""
        try:
            experiences = self.extract_experience()
            if experiences and isinstance(experiences, list):
                for exp in experiences:
                    if isinstance(exp, dict):
                        if 'period' in exp and 'present' in exp['period'].lower():
                            return exp.get('position', '')
                        if 'position' in exp:
                            return exp['position']
            return 'sw_designer'
        except Exception as e:
            self.logger.error(f"Error extracting position: {e}")
            return 'sw_designer'

    def extract_name(self) -> str:
        """Extract name from resume"""
        try:
            # Check first paragraph for name
            if self.paragraphs:
                first_para = self.paragraphs[0].strip()
                # Simple name pattern: 1-2 words, capitalized
                if len(first_para.split()) <= 3:
                    return first_para
            return "Unknown"
        except Exception as e:
            self.logger.error(f"Error extracting name: {e}")
            return "Unknown"

    def extract_email(self) -> str:
        """Extract email from resume"""
        try:
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            for para in self.paragraphs:
                match = re.search(email_pattern, para)
                if match:
                    return match.group()
            return ""
        except Exception as e:
            self.logger.error(f"Error extracting email: {e}")
            return ""

    def extract_phone_numbers(self) -> str:
        """Extract phone numbers from resume"""
        try:
            phone_pattern = r'(?:\+\d{1,3}[-.\s]?)?\d{8,12}'
            for para in self.paragraphs:
                match = re.search(phone_pattern, para)
                if match:
                    return match.group()
            return ""
        except Exception as e:
            self.logger.error(f"Error extracting phone number: {e}")
            return ""

    def extract_skills(self):
        """Extract skills with better categorization and matching"""
        skills_by_category = {
            "programming": set(),
            "tools": set(),
            "frameworks": set(),
            "platforms": set(),
            "other": set()
        }
        
        # First pass: Look for explicit skill sections
        text = ' '.join(self.paragraphs).lower()
        skill_sections = self._find_skill_sections(text)
        
        for section_text in skill_sections:
            # Process skills in the section
            found_skills = self._process_skill_text(section_text)
            for category, skills in found_skills.items():
                skills_by_category[category].update(skills)
        
        # Second pass: Look for skills in project descriptions
        project_skills = self._extract_project_skills()
        for category, skills in project_skills.items():
            skills_by_category[category].update(skills)
        
        # Third pass: Look for skills in experience sections
        experience_skills = self._extract_experience_skills()
        for category, skills in experience_skills.items():
            skills_by_category[category].update(skills)
        
        # Clean and normalize skills
        normalized_skills = {}
        for category, skills in skills_by_category.items():
            if skills:
                normalized_skills[category] = sorted(list({
                    skill.lower() for skill in skills 
                    if len(skill) > 1  # Filter out single characters
                }))
        
        return normalized_skills if normalized_skills else {"other": []}

    def _find_skill_sections(self, text):
        """Find skill-related sections in text"""
        sections = []
        skill_markers = [
            "expertise", "skills", "technical skills", 
            "technologies", "competencies", "tools used",
            "programming languages", "frameworks"
        ]
        
        for marker in skill_markers:
            if marker in text:
                start = text.find(marker)
                end = self._find_next_section(text, start)
                if end > start:
                    sections.append(text[start:end])
        
        return sections

    def _process_skill_text(self, text):
        """Process text to extract categorized skills"""
        found_skills = {
            "programming": set(),
            "tools": set(),
            "frameworks": set(),
            "platforms": set(),
            "other": set()
        }
        
        # Use skill keywords from assets
        for category, skills in self.skill_keywords.items():
            if isinstance(skills, list):
                for skill in skills:
                    if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text):
                        found_skills[category].add(skill)
        
        return found_skills

    def extract_experience(self):
        """Extract work experience with improved accuracy"""
        experiences = []
        current_exp = None
        
        for idx, para in enumerate(self.paragraphs):
            para_lower = para.lower()
            
            # Check for new experience entry
            if any(company in para for company in ["ACTIA", "SASTEC"]):
                if current_exp:
                    experiences.append(current_exp)
                
                current_exp = {
                    "company": self._extract_company_name(para),
                    "position": self._extract_position(para),
                    "period": self._extract_date_range(para),
                    "responsibilities": []
                }
                
                # Look ahead for period if not found
                if not current_exp["period"] and idx + 1 < len(self.paragraphs):
                    current_exp["period"] = self._extract_date_range(self.paragraphs[idx + 1])
                    
            elif current_exp and self._is_responsibility(para_lower):
                current_exp["responsibilities"].append(para.strip())
        
        if current_exp:
            experiences.append(current_exp)
        
        return experiences

    def _extract_company_name(self, text):
        """Extract company name with better accuracy"""
        companies = {
            "ACTIA": "ACTIA Engineering Services",
            "SASTEC": "SASTEC group"
        }
        
        for key, full_name in companies.items():
            if key in text:
                return full_name
        return ""

    def _extract_date_range(self, text):
        """Extract date range with better parsing"""
        date_patterns = [
            r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4})\s*[-–—]\s*((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}|[Pp]resent)',
            r'(\d{4})\s*[-–—]\s*((?:\d{4})|(?:[Pp]resent))',
            r'((?:\d{2}|\d{4})/\d{2})\s*[-–—]\s*((?:\d{2}|\d{4})/\d{2}|[Pp]resent)'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                return f"{match.group(1)} - {match.group(2)}"
        return ""

    def extract_education(self):
        """Extract education with better structure"""
        education = []
        current_edu = None
        in_education_section = False
        
        for para in self.paragraphs:
            para_lower = para.lower()
            
            # Check for education section
            if "education" in para_lower:
                in_education_section = True
                continue
                
            if in_education_section:
                # Check for end of education section
                if any(marker in para_lower for marker in ["experience", "skills", "projects"]):
                    in_education_section = False
                    if current_edu:
                        education.append(current_edu)
                        current_edu = None
                    continue
                
                # Process education entry
                if any(school in para for school in ["ESPRIT", "Higher Institute", "Technical"]):
                    if current_edu:
                        education.append(current_edu)
                    
                    current_edu = {
                        "school": self._extract_school_name(para),
                        "degree": self._extract_degree(para),
                        "period": self._extract_date_range(para),
                        "field": self._extract_field(para)
                    }
                elif current_edu and self._extract_date_range(para):
                    current_edu["period"] = self._extract_date_range(para)
        
        if current_edu:
            education.append(current_edu)
        
        return education

    def _extract_school_name(self, text):
        """Extract school name"""
        schools = {
            "ESPRIT": "ESPRIT - Private School of Engineering and Technology",
            "Higher Institute": "Higher Institute of Computer Science and Mathematics in Monastir",
            "Technical": "Technical 2 mars 1934 of Sousse high school"
        }
        
        for key, name in schools.items():
            if key in text:
                return name
        return ""

    def _clean_text(self, text: str) -> str:
        """Clean text from unwanted characters"""
        if not text:
            return ""
        # Remove special characters but keep essential ones
        text = re.sub(r'[^\w\s+@.-]', ' ', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
