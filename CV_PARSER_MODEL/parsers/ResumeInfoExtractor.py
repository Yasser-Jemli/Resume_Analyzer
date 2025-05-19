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
        """Extract skills with improved categorization"""
        try:
            all_skills = {
                "programming": set(),
                "tools": set(),
                "frameworks": set(),
                "platforms": set(),
                "other": set()
            }
            
            # Extract from explicit skills sections
            sections = self._split_into_sections('\n'.join(self.paragraphs))
            skills_text = sections.get('skills', '') or sections.get('expertise', '')
            
            if skills_text:
                explicit_skills = self._process_skill_text(skills_text.lower())
                for category, skills in explicit_skills.items():
                    all_skills[category].update(skills)
            
            # Extract from projects
            project_skills = self._extract_project_skills()
            for category, skills in project_skills.items():
                all_skills[category].update(skills)
            
            # Extract from experience
            experience_skills = self._extract_experience_skills()
            for category, skills in experience_skills.items():
                all_skills[category].update(skills)
            
            # Clean and normalize results
            result = {}
            for category, skills in all_skills.items():
                if skills:
                    cleaned_skills = {
                        skill.lower() for skill in skills 
                        if len(skill) > 1
                    }
                    if cleaned_skills:
                        result[category] = sorted(list(cleaned_skills))
            
            return result if result else {"other": []}
            
        except Exception as e:
            self.logger.error(f"Error extracting skills: {str(e)}")
            return {"other": []}

    def _extract_project_skills(self):
        """Extract skills from project descriptions"""
        project_skills = {
            "programming": set(),
            "tools": set(),
            "frameworks": set(),
            "platforms": set(),
            "other": set()
        }
        
        # Find projects section
        sections = self._split_into_sections('\n'.join(self.paragraphs))
        project_text = sections.get('projects', '')
        
        if not project_text:
            return project_skills
            
        # Look for skill indicators
        skill_indicators = [
            "skills:", "technologies:", "tools:", 
            "built with:", "developed using:", "implemented with:"
        ]
        
        for line in project_text.lower().split('\n'):
            # Check if line contains skill indicators
            if any(indicator in line for indicator in skill_indicators):
                skills_found = self._process_skill_text(line)
                for category, skills in skills_found.items():
                    project_skills[category].update(skills)
        
        return project_skills

    def _extract_experience_skills(self):
        """Extract skills from experience descriptions"""
        experience_skills = {
            "programming": set(),
            "tools": set(),
            "frameworks": set(),
            "platforms": set(),
            "other": set()
        }
        
        # Find experience section
        sections = self._split_into_sections('\n'.join(self.paragraphs))
        experience_text = sections.get('experience', '')
        
        if not experience_text:
            return experience_skills
        
        # Process each paragraph in experience section
        for para in experience_text.split('\n'):
            skills_found = self._process_skill_text(para.lower())
            for category, skills in skills_found.items():
                experience_skills[category].update(skills)
        
        return experience_skills

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
        """Extract work experience with improved company detection"""
        experiences = []
        current_exp = None
        
        for idx, para in enumerate(self.paragraphs):
            # Check for new experience entry
            if self._is_company_name(para):
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
                    
            elif current_exp and self._is_responsibility(para.lower()):
                current_exp["responsibilities"].append(para.strip())
        
        if current_exp:
            experiences.append(current_exp)
        
        return experiences

    def _extract_company_name(self, text):
        """Extract company name from text using keyword dictionary"""
        text = text.upper()  # Normalize for comparison
        
        # Check company names from keywords dictionary
        for industry, companies in self.experience_keywords.get('company_names', {}).items():
            for short_name, full_name in companies.items():
                if short_name.upper() in text:
                    return full_name
        
        # Fallback: Try to extract using company indicators
        words = text.split()
        for i, word in enumerate(words):
            # Look for company indicators
            for indicator in self.experience_keywords.get('company_indicators', []):
                if indicator.upper() in word:
                    # Try to construct company name from preceding words
                    start = max(0, i-3)  # Look up to 3 words before
                    company_name = ' '.join(words[start:i+1])
                    return company_name.title()
        
        return text.strip()

    def _is_company_name(self, text):
        """Check if text contains a known company name"""
        text = text.upper()
        
        # Check against known company names
        for industry, companies in self.experience_keywords.get('company_names', {}).items():
            if any(name.upper() in text for name in companies.keys()):
                return True
                
        # Check for company indicators
        return any(indicator.upper() in text.upper() 
                  for indicator in self.experience_keywords.get('company_indicators', []))

    def _extract_date_range(self, text):
        """Extract date range with better parsing"""
        date_patterns = [
            r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4})\s*[-–—]\s*((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}|[Pp]resent)',
            r'(\d{4})\s*[-–—]\s*((?:\d{4})|(?:[Pp]present))',
            r'((?:\d{2}|\d{4})/\d{2})\s*[-–—]\s*((?:\d{2}|\d{4})/\d{2}|[Pp]present)'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                return f"{match.group(1)} - {match.group(2)}"
        return ""

    def extract_education(self):
        """Extract education information with improved section handling"""
        education = []
        
        # Get education section content
        sections = self._split_into_sections('\n'.join(self.paragraphs))
        education_text = sections.get('education', '')
        
        if not education_text:
            return []
        
        # Process education entries
        current_edu = None
        for para in education_text.split('\n'):
            para = para.strip()
            if not para:
                continue
                
            # Check if this is a new education entry
            for school_type, schools in self.education_keywords["schools"].items():
                for key in schools.keys():
                    if key in para:
                        if current_edu:
                            self._validate_and_append_education(current_edu, education)
                        
                        current_edu = {
                            "school": self._extract_school_name(para),
                            "degree": self._extract_degree(para),
                            "period": self._extract_date_range(para),
                            "field": self._extract_field(para),
                            "type": school_type
                        }
                        break
            
            # If we have a current entry, check for additional info
            if current_edu:
                # Update period if found
                if not current_edu["period"]:
                    period = self._extract_date_range(para)
                    if period:
                        current_edu["period"] = period
                
                # Update field if found
                if not current_edu["field"]:
                    field = self._extract_field(para)
                    if field:
                        current_edu["field"] = field
                        
                # Update degree if found
                if not current_edu["degree"]:
                    degree = self._extract_degree(para)
                    if degree:
                        current_edu["degree"] = degree
        
        # Add last entry if exists
        if current_edu:
            self._validate_and_append_education(current_edu, education)
        
        return education

    def _validate_and_append_education(self, edu_entry, education_list):
        """Validate and clean education entry before adding"""
        if edu_entry.get("school") and (edu_entry.get("degree") or edu_entry.get("field")):
            # Clean and validate degree
            if edu_entry["degree"]:
                edu_entry["degree"] = self._normalize_degree(edu_entry["degree"])
            
            # Clean and validate field
            if edu_entry["field"]:
                edu_entry["field"] = self._normalize_field(edu_entry["field"])
            
            education_list.append(edu_entry)

    def _extract_degree(self, text):
        """Extract degree with improved matching"""
        text_lower = text.lower()
        
        # Check all degree types
        for degree_type, degrees in self.education_keywords["degrees"].items():
            for degree in degrees:
                if degree.lower() in text_lower:
                    return degree
        
        # Look for common degree patterns
        degree_patterns = [
            r"(bachelor|master|phd|doctorate|license|engineering|bsc|msc)(?:\sin|\sof)?\s([^,\.]*)",
            r"(B\.|M\.|Ph\.D\.|BSc|MSc|MBA)\sin\s([^,\.]*)"
        ]
        
        for pattern in degree_patterns:
            match = re.search(pattern, text_lower)
            if match:
                return f"{match.group(1)} {match.group(2)}".strip().title()
        
        return ""

    def _extract_field(self, text):
        """Extract field of study with improved matching"""
        text_lower = text.lower()
        
        # Check all fields
        for field_type, fields in self.education_keywords["fields"].items():
            for field in fields:
                if field.lower() in text_lower:
                    return field
        
        # Look for field patterns after degree keywords
        field_patterns = [
            r"(?:in|of)\s+([\w\s]+(?:Science|Engineering|Technology|Development)[\w\s]*)",
            r"(?:bachelor|master|phd|license)\s+(?:in|of)\s+([\w\s]+)"
        ]
        
        for pattern in field_patterns:
            match = re.search(pattern, text_lower)
            if match:
                return match.group(1).strip().title()
        
        return ""

    def _normalize_degree(self, degree):
        """Normalize degree naming"""
        degree_lower = degree.lower()
        
        # Map common variations
        degree_map = {
            "bachelor": "Bachelor's Degree",
            "master": "Master's Degree",
            "phd": "PhD",
            "doctorate": "PhD",
            "license": "Bachelor's Degree",
            "engineering": "Engineering Degree",
            "bsc": "Bachelor of Science",
            "msc": "Master of Science",
            "mba": "Master of Business Administration"
        }
        
        for key, value in degree_map.items():
            if key in degree_lower:
                return value
        
        return degree.title()

    def _clean_text(self, text: str) -> str:
        """Clean text from unwanted characters"""
        if not text:
            return ""
        # Remove special characters but keep essential ones
        text = re.sub(r'[^\w\s+@.-]', ' ', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text

    def _find_next_section(self, text, start_pos):
        """Find the start of the next section after a given position"""
        section_markers = [
            "education",
            "experience",
            "skills",
            "expertise",
            "projects",
            "certifications",
            "languages",
            "interests",
            "publications",
            "references"
        ]
        
        # Find all section starts after the given position
        next_pos = float('inf')
        for marker in section_markers:
            pos = text.find(marker, start_pos + 1)  # +1 to avoid finding current section
            if pos != -1:  # Found a section
                next_pos = min(next_pos, pos)
                
        return next_pos if next_pos != float('inf') else len(text)

    def _is_section_header(self, text):
        """Check if text is a section header"""
        section_markers = [
            "education",
            "experience",
            "skills",
            "expertise",
            "projects",
            "certifications",
            "languages",
            "interests"
        ]
        
        text_lower = text.lower().strip()
        return any(marker == text_lower for marker in section_markers)

    def _extract_section_content(self, text, section_name):
        """Extract content between section headers"""
        text_lower = text.lower()
        start_pos = text_lower.find(section_name.lower())
        
        if start_pos == -1:
            return ""
            
        # Find where this section ends
        end_pos = self._find_next_section(text_lower, start_pos)
        
        # Extract and clean the section content
        section_text = text[start_pos:end_pos].strip()
        # Remove the section header
        lines = section_text.split('\n')[1:]
        return '\n'.join(lines).strip()

    def _split_into_sections(self, text):
        """Split text into labeled sections"""
        sections = {}
        current_pos = 0
        text_lower = text.lower()
        
        section_markers = [
            "education",
            "experience",
            "skills",
            "expertise",
            "projects",
            "certifications",
            "languages",
            "interests"
        ]
        
        # Find all section starts
        section_positions = []
        for marker in section_markers:
            pos = text_lower.find(marker, current_pos)
            if pos != -1:
                section_positions.append((pos, marker))
        
        # Sort positions by their location in text
        section_positions.sort()
        
        # Extract each section
        for i, (start, marker) in enumerate(section_positions):
            # Fix the ternary operator syntax
            end = section_positions[i + 1][0] if i + 1 < len(section_positions) else len(text)
            content = text[start:end].strip()
            sections[marker] = content
        
        return sections
