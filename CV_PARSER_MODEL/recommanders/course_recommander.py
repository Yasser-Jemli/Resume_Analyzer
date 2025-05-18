from pathlib import Path
import json
import logging
from typing import Dict, List

class CourseRecommender:
    """Recommends courses and learning resources based on skill recommendations"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.courses_data = self._load_courses_data()
        
    def _load_courses_data(self) -> Dict:
        """Load courses data from JSON file"""
        try:
            courses_file = Path(__file__).parent.parent / 'assets' / 'courses_data.json'
            with open(courses_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading courses data: {e}")
            return {"platforms": {}}
            
    def recommend_courses(self, skill_recommendations: Dict) -> Dict:
        """Generate course recommendations based on skill recommendations"""
        try:
            if skill_recommendations["status"] != "success":
                return {"status": "error", "message": "Invalid skill recommendations"}
                
            recommendations = {
                "status": "success",
                "high_priority": self._get_courses_for_skills(
                    skill_recommendations["recommendations"]["missing_required"]
                ),
                "medium_priority": self._get_courses_for_skills(
                    skill_recommendations["recommendations"]["missing_preferred"]
                ),
                "additional_learning": self._get_courses_for_skills(
                    skill_recommendations["recommendations"]["related_skills"][:3]
                )
            }
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating course recommendations: {e}")
            return {"status": "error", "message": str(e)}
            
    def _get_courses_for_skills(self, skills: List[str]) -> Dict:
        """Get course recommendations for specific skills"""
        courses = {}
        
        for skill in skills:
            skill_courses = {
                "udemy": self._get_platform_courses("udemy", skill),
                "coursera": self._get_platform_courses("coursera", skill),
                "youtube": self._get_youtube_channels(skill),
                "certificates": self._get_certificates(skill)
            }
            courses[skill] = skill_courses
            
        return courses
        
    def _get_platform_courses(self, platform: str, skill: str) -> List[Dict]:
        """Get courses from a specific platform for a skill"""
        platform_data = self.courses_data["platforms"].get(platform, {})
        courses = platform_data.get("courses", {}).get(skill, [])
        base_url = platform_data.get("base_url", "")
        
        return [
            {
                "title": course.replace("-", " ").title(),
                "url": f"{base_url}{course}"
            } for course in courses
        ]
        
    def _get_youtube_channels(self, skill: str) -> List[str]:
        """Get recommended YouTube channels for a skill"""
        return self.courses_data["platforms"].get("youtube", {}).get("channels", {}).get(skill, [])
        
    def _get_certificates(self, skill: str) -> List[str]:
        """Get recommended certificates for a skill"""
        return self.courses_data["platforms"].get("certificates", {}).get(skill, [])