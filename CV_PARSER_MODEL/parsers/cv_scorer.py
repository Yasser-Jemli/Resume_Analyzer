from pathlib import Path
import json
import logging

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
        """Score a CV based on the criteria"""
        scores = {
            "skills": self._score_skills(cv_data.get("Skills", [])),
            "experience": self._score_experience(cv_data.get("Experience", [])),
            "education": self._score_education(cv_data.get("Education", []))
        }
        
        total_score = sum(scores.values())
        max_possible = len(scores.keys()) * 100
        normalized_score = (total_score / max_possible) * 100
        
        return {
            "total_score": round(normalized_score, 2),
            "detailed_scores": {k: round(v, 2) for k, v in scores.items()},
            "feedback": self._generate_feedback(scores)
        }
    
    def _score_skills(self, skills):
        """Score skills section"""
        if not skills:
            return 0
            
        score = 0
        required_matches = 0
        preferred_matches = 0
        
        skills_lower = [s.lower() for s in skills]
        
        for skill in self.criteria["skills"]["required"]:
            if skill.lower() in skills_lower:
                required_matches += 1
                
        for skill in self.criteria["skills"]["preferred"]:
            if skill.lower() in skills_lower:
                preferred_matches += 1
        
        total_required = len(self.criteria["skills"]["required"])
        total_preferred = len(self.criteria["skills"]["preferred"])
        
        if total_required > 0:
            score += (required_matches / total_required) * 100 * self.criteria["skills"]["weights"]["required"]
        
        if total_preferred > 0:
            score += (preferred_matches / total_preferred) * 100 * self.criteria["skills"]["weights"]["preferred"]
            
        return score / (self.criteria["skills"]["weights"]["required"] + self.criteria["skills"]["weights"]["preferred"])
    
    def _score_experience(self, experience):
        """Score experience section"""
        if not experience:
            return 0
            
        # Simple text-based scoring for demonstration
        score = 0
        text = ' '.join(experience).lower()
        
        # Score based on keywords
        keywords = self.criteria["experience"]["relevant_keywords"]
        keyword_matches = sum(1 for word in keywords if word.lower() in text)
        keyword_score = (keyword_matches / len(keywords)) * 100
        
        return keyword_score
    
    def _score_education(self, education):
        """Score education section"""
        if not education:
            return 0
            
        score = 0
        text = ' '.join(education).lower()
        
        # Score based on required degrees
        degrees = self.criteria["education"]["required_degrees"]
        degree_matches = sum(1 for degree in degrees if degree.lower() in text)
        degree_score = (degree_matches / len(degrees)) * 100
        
        return degree_score
    
    def _generate_feedback(self, scores):
        """Generate feedback based on scores"""
        feedback = []
        
        if scores["skills"] < 50:
            feedback.append("Skills: Consider adding more relevant technical skills")
        elif scores["skills"] < 75:
            feedback.append("Skills: Good foundation, but could be strengthened")
        else:
            feedback.append("Skills: Strong technical skill set")
            
        if scores["experience"] < 50:
            feedback.append("Experience: More relevant experience recommended")
        else:
            feedback.append("Experience: Good experience level")
            
        return feedback