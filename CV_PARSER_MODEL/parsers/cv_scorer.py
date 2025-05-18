from pathlib import Path
import json
import logging
import re
from datetime import datetime

class CVScorer:
    """CV scoring system with configurable criteria"""
    
    def __init__(self, custom_criteria=None):
        self.logger = logging.getLogger(__name__)
        self.criteria = self._load_default_criteria()
        
        if custom_criteria:
            self.criteria.update(custom_criteria)
    
    def _load_default_criteria(self):
        """Load default scoring criteria from JSON file"""
        try:
            criteria_file = Path(__file__).parent.parent / 'assets' / 'scoring_criteria.json'
            with open(criteria_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading default criteria: {e}")
            return self._get_fallback_criteria()
    
    def _get_fallback_criteria(self):
        """Fallback scoring criteria if JSON file is not available"""
        return {
            "skills": {
                "required": ["python", "c++", "git"],
                "preferred": ["rust", "android", "linux"],
                "weights": {
                    "required": 2.0,
                    "preferred": 1.0
                }
            },
            "experience": {
                "minimum_years": 2,
                "preferred_years": 4,
                "relevant_keywords": ["software", "developer", "engineer"],
                "weights": {
                    "years": 1.5,
                    "relevance": 1.0
                }
            },
            "education": {
                "required_degrees": ["bachelor", "master", "engineering"],
                "weights": {
                    "degree": 1.0
                }
            }
        }
    
    def score_cv(self, cv_data):
        """Score a CV based on criteria"""
        if not cv_data:
            self.logger.error("No CV data provided")
            return {
                "total_score": 0,
                "detailed_scores": {},
                "feedback": ["No CV data to analyze"]
            }

        try:
            scores = {
                "skills": self._score_skills(cv_data.get("Skills", [])),
                "experience": self._score_experience(cv_data.get("Experience", [])),
                "education": self._score_education(cv_data.get("Education", []))
            }
            
            # Calculate total score with weights
            weights = self.criteria.get("weights", {"skills": 0.4, "experience": 0.35, "education": 0.25})
            total_score = sum(scores[cat] * weights[cat] for cat in scores)
            
            return {
                "total_score": round(total_score, 2),
                "detailed_scores": {k: round(v, 2) for k, v in scores.items()},
                "feedback": self._generate_feedback(scores)
            }
            
        except Exception as e:
            self.logger.error(f"Error scoring CV: {str(e)}")
            return {
                "total_score": 0,
                "detailed_scores": {},
                "feedback": [f"Error scoring CV: {str(e)}"]
            }

    def _score_skills(self, skills):
        """Score skills section"""
        if not skills:
            return 0
        
        try:
            skills_lower = [s.lower() for s in skills]
            required_skills = self.criteria["skills"]["required"]
            
            # Count matching required skills
            matches = sum(1 for skill in required_skills 
                         if any(skill.lower() in s for s in skills_lower))
            
            # Calculate percentage score
            score = (matches / len(required_skills)) * 100 if required_skills else 0
            
            return min(100, score)
            
        except Exception as e:
            self.logger.error(f"Error scoring skills: {str(e)}")
            return 0

    def _extract_years_of_experience(self, experience_text):
        """Extract total years of experience from text"""
        total_years = 0
        try:
            # Pattern for date ranges like "2020 - 2023" or "2020-present"
            date_pattern = r'(\d{4})\s*[-–—]\s*((?:\d{4})|(?:present|current|now))'
            
            # Find all date ranges
            matches = re.finditer(date_pattern, experience_text.lower())
            
            current_year = datetime.now().year
            
            for match in matches:
                start_year = int(match.group(1))
                end_str = match.group(2)
                
                # Handle 'present' or current year
                if end_str in ['present', 'current', 'now']:
                    end_year = current_year
                else:
                    end_year = int(end_str)
                
                # Add years from this position
                if start_year <= end_year:
                    total_years += end_year - start_year
            
            # Also look for explicit mentions of experience
            year_patterns = [
                r'(\d+)\+?\s*years? of experience',
                r'(\d+)\+?\s*years? in',
                r'experienced (\d+)\+?\s*years?'
            ]
            
            for pattern in year_patterns:
                matches = re.finditer(pattern, experience_text.lower())
                for match in matches:
                    years = int(match.group(1))
                    total_years = max(total_years, years)
            
            return total_years
            
        except Exception as e:
            self.logger.error(f"Error extracting years of experience: {str(e)}")
            return 0

    def _score_experience(self, experience):
        """Score experience section with years calculation"""
        if not experience:
            return 0
            
        try:
            # Join experience entries into single text
            text = ' '.join(str(exp) for exp in experience).lower()
            
            # Get years of experience
            years = self._extract_years_of_experience(text)
            
            # Score based on years (assuming ideal is 5+ years)
            year_score = min(100, (years / 5) * 100)
            
            # Score based on keywords
            keywords = self.criteria["experience"]["relevant_keywords"]
            keyword_matches = sum(1 for keyword in keywords if keyword.lower() in text)
            keyword_score = (keyword_matches / len(keywords)) * 100 if keywords else 0
            
            # Combined score (60% years, 40% keywords)
            total_score = (year_score * 0.6) + (keyword_score * 0.4)
            
            self.logger.info(f"Experience score breakdown - Years: {years} ({year_score}%), "
                            f"Keywords: {keyword_score}%, Total: {total_score}%")
            
            return min(100, total_score)
            
        except Exception as e:
            self.logger.error(f"Error scoring experience: {str(e)}")
            return 0

    def _score_education(self, education):
        """Score education section"""
        if not education:
            return 0
            
        try:
            text = ' '.join(str(edu) for edu in education).lower()
            required_degrees = self.criteria["education"]["required_degrees"]
            
            # Count matching degrees
            matches = sum(1 for degree in required_degrees 
                         if degree.lower() in text)
            
            score = (matches / len(required_degrees)) * 100 if required_degrees else 0
            
            return min(100, score)
            
        except Exception as e:
            self.logger.error(f"Error scoring education: {str(e)}")
            return 0

    def _generate_feedback(self, scores):
        """Generate simple feedback based on scores"""
        feedback = []
        
        for category, score in scores.items():
            if score < 50:
                feedback.append(f"{category.title()}: Needs improvement")
            elif score < 75:
                feedback.append(f"{category.title()}: Satisfactory")
            else:
                feedback.append(f"{category.title()}: Excellent")
        
        return feedback