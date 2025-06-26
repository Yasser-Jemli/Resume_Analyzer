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
        """Score a CV with detailed metrics"""
        try:
            experience_results = self._score_experience(cv_data.get("Experience", []))
            skills_score = self._score_skills(cv_data.get("Skills", []))
            education_score = self._score_education(cv_data.get("Education", []))
            
            scores = {
                "skills": skills_score,
                "experience": experience_results["score"],
                "education": education_score
            }
            
            # Calculate weighted total
            weights = self.criteria.get("weights", {
                "skills": 0.4,
                "experience": 0.35,
                "education": 0.25
            })
            total_score = sum(scores[cat] * weights[cat] for cat in scores)
            
            return {
                "total_score": round(total_score, 2),
                "detailed_scores": {k: round(v, 2) for k, v in scores.items()},
                "experience_metrics": {
                    "years": experience_results["years"],
                    "positions": experience_results["positions"],
                    "details": experience_results["details"]
                },
                "feedback": self._generate_feedback(scores)
            }
            
        except Exception as e:
            self.logger.error(f"Error in CV scoring: {str(e)}")
            return {
                "total_score": 0,
                "detailed_scores": {},
                "experience_metrics": {
                    "years": 0,
                    "positions": 0,
                    "details": f"Error: {str(e)}"
                },
                "feedback": ["Error occurred during scoring"]
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
        """Score experience section with detailed metrics"""
        if not experience:
            return {
                "score": 0,
                "years": 0,
                "positions": 0,
                "details": "No experience found"
            }
            
        try:
            # Join experience entries into single text
            text = ' '.join(str(exp) for exp in experience).lower()
            
            # Extract years of experience
            total_years = self._extract_years_of_experience(text)
            
            # Count different positions
            position_markers = ["developer", "engineer", "designer", "analyst"]
            positions = sum(1 for marker in position_markers if marker in text.lower())
            
            # Score based on years (40%)
            year_score = min(100, (total_years / 5) * 100)
            
            # Score based on keywords (40%)
            keywords = self.criteria["experience"]["relevant_keywords"]
            keyword_matches = sum(1 for keyword in keywords if keyword.lower() in text)
            keyword_score = (keyword_matches / len(keywords)) * 100 if keywords else 0
            
            # Score based on positions (20%)
            position_score = min(100, positions * 25)
            
            # Calculate total weighted score
            total_score = (year_score * 0.4) + (keyword_score * 0.4) + (position_score * 0.2)
            
            return {
                "score": round(total_score, 2),
                "years": total_years,
                "positions": positions,
                "details": f"{total_years} years, {positions} positions"
            }
            
        except Exception as e:
            self.logger.error(f"Error scoring experience: {str(e)}")
            return {
                "score": 0,
                "years": 0,
                "positions": 0,
                "details": f"Error: {str(e)}"
            }

    def _score_education(self, education):
        """Improved scoring for education section"""
        if not education:
            return 0

        # If education is a dict with 'entries', use that
        if isinstance(education, dict) and "entries" in education:
            entries = education["entries"]
        else:
            entries = education

        if not entries:
            return 0

        total_points = 0
        max_points = 0

        for entry in entries:
            entry_points = 0
            entry_max = 3  # institution, degree, period

            # 1. Institution present
            if entry.get("institution"):
                entry_points += 1

            # 2. Degree present (partial match, case-insensitive)
            degree = entry.get("degree")
            if degree:
                entry_points += 1

            # 3. Period present (year or date range)
            period = entry.get("period")
            if period:
                entry_points += 1

            # Bonus: Higher education (engineering/university)
            inst = entry.get("institution", "").lower()
            if any(x in inst for x in ["esprit", "engineering", "university", "institute"]):
                entry_points += 0.5
                entry_max += 0.5

            total_points += entry_points
            max_points += entry_max

        # Normalize to 100
        score = (total_points / max_points) * 100 if max_points else 0
        return round(min(100, score), 2)

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