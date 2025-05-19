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
        if not cv_data:
            self.logger.warning("Received empty CV data")
            return self._get_default_score_result("No CV data provided")

        try:
            # Handle different parser formats
            if isinstance(cv_data, dict) and "parsers" in cv_data:
                # If we received the full parsing results
                custom_data = cv_data.get("parsers", {}).get("custom", {})
                if not custom_data:
                    return self._get_default_score_result("No custom parser data found")
                cv_data = custom_data

            # Get sections with better error handling
            experience_data = self._safe_get_section(cv_data, "Experience")
            skills_data = self._safe_get_section(cv_data, "Skills")
            education_data = self._safe_get_section(cv_data, "Education")

            # Debug logging
            self.logger.debug(f"Processing CV with: {len(skills_data)} skills, "
                            f"{len(experience_data)} experience entries, "
                            f"{len(education_data)} education entries")

            # Score individual sections
            experience_results = self._score_experience(experience_data)
            skills_score = self._score_skills(skills_data)
            education_score = self._score_education(education_data)
            
            scores = {
                "skills": skills_score,
                "experience": experience_results["score"],
                "education": education_score
            }
            
            # Calculate weighted total with safe weights from criteria
            weights = self.criteria.get("scoring", {}).get("weights", {
                "skills": 0.4,
                "experience": 0.35,
                "education": 0.25
            })
            
            total_score = sum(scores.get(cat, 0) * weights.get(cat, 0) 
                            for cat in scores.keys())
            
            result = {
                "total_score": round(total_score, 2),
                "detailed_scores": {k: round(v, 2) for k, v in scores.items()},
                "experience_metrics": {
                    "years": experience_results["years"],
                    "positions": experience_results["positions"],
                    "details": experience_results["details"]
                },
                "feedback": self._generate_feedback(scores)
            }

            # Log the scoring result
            self.logger.info(f"CV Scoring completed - Total score: {result['total_score']}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in CV scoring: {str(e)}", exc_info=True)
            return self._get_default_score_result(str(e))

    def _safe_get_section(self, data, section_name):
        """Safely extract section data with type checking"""
        try:
            section_data = data.get(section_name, [])
            if section_data is None:
                return []
            if isinstance(section_data, (list, tuple)):
                return section_data
            if isinstance(section_data, str):
                return [section_data]
            return []
        except Exception as e:
            self.logger.warning(f"Error getting {section_name} section: {e}")
            return []

    def _get_default_score_result(self, error_message):
        """Return default scoring result with error message"""
        return {
            "total_score": 0,
            "detailed_scores": {
                "skills": 0,
                "experience": 0,
                "education": 0
            },
            "experience_metrics": {
                "years": 0,
                "positions": 0,
                "details": f"Error: {error_message}"
            },
            "feedback": ["Error occurred during scoring"]
        }

    def _score_skills(self, skills_data):
        """Score skills with improved accuracy"""
        if not skills_data:
            return 0
            
        # Handle both dict and list formats
        all_skills = set()
        if isinstance(skills_data, dict):
            for category in skills_data.values():
                if isinstance(category, list):
                    all_skills.update(s.lower() for s in category)
        elif isinstance(skills_data, list):
            all_skills.update(s.lower() for s in skills_data)
        
        if not all_skills:
            return 0
            
        # Get required and preferred skills
        required_skills = set(s.lower() for s in self.criteria["skills"]["required"])
        preferred_skills = set(s.lower() for s in self.criteria["skills"]["preferred"])
        
        # Calculate matches
        required_matches = len(required_skills.intersection(all_skills))
        preferred_matches = len(preferred_skills.intersection(all_skills))
        
        # Calculate weighted scores
        required_score = (required_matches / len(required_skills)) * 100
        preferred_score = (preferred_matches / len(preferred_skills)) * 100
        
        # Apply weights
        weights = self.criteria["skills"]["weights"]
        total_score = (
            (required_score * weights["required"]) +
            (preferred_score * weights["preferred"])
        ) / (weights["required"] + weights["preferred"])
        
        return min(100, total_score)

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

    def _parse_experience_text(self, experience_data):
        """Parse experience data into text considering different formats"""
        if isinstance(experience_data, str):
            return experience_data.lower()
        
        if isinstance(experience_data, list):
            if all(isinstance(x, str) for x in experience_data):
                return ' '.join(experience_data).lower()
            
            if all(isinstance(x, dict) for x in experience_data):
                text_parts = []
                for exp in experience_data:
                    parts = []
                    if isinstance(exp.get('company'), str):
                        parts.append(exp['company'])
                    if isinstance(exp.get('position'), str):
                        parts.append(exp['position'])
                    if isinstance(exp.get('period'), str):
                        parts.append(exp['period'])
                    if isinstance(exp.get('responsibilities'), list):
                        parts.extend(exp['responsibilities'])
                    text_parts.append(' '.join(parts))
                return ' '.join(text_parts).lower()
        
        return ''

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
            # Safely parse experience entries
            text = self._parse_experience_text(experience)
            
            # Extract years of experience
            total_years = self._extract_years_of_experience(text)
            
            # Count different positions
            position_markers = self.criteria.get("experience", {}).get(
                "relevant_keywords", 
                ["developer", "engineer", "designer", "analyst"]
            )
            positions = sum(1 for marker in position_markers if marker in text)
            
            # Calculate scores with safe weights
            year_score = min(100, (total_years / 5) * 100)
            keyword_score = self._calculate_keyword_score(text)
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

    def _calculate_keyword_score(self, text):
        """Calculate score based on keyword matches"""
        keywords = self.criteria.get("experience", {}).get("relevant_keywords", [])
        if not keywords:
            return 0
            
        keyword_matches = sum(1 for keyword in keywords if keyword.lower() in text)
        return (keyword_matches / len(keywords)) * 100 if keywords else 0

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