from pathlib import Path
import json
import logging
import re

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

    def _score_experience(self, experience):
        """Score experience section"""
        if not experience:
            return 0
            
        try:
            text = ' '.join(str(exp) for exp in experience).lower()
            keywords = self.criteria["experience"]["relevant_keywords"]
            
            # Count keyword matches
            matches = sum(1 for keyword in keywords if keyword.lower() in text)
            score = (matches / len(keywords)) * 100 if keywords else 0
            
            return min(100, score)
            
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