from pathlib import Path
import json
import logging
from typing import Dict, List, Set

class SkillRecommender:
    """Recommends skills based on job position and existing skills"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.skills_data = self._load_skills_data()
        
    def _load_skills_data(self) -> Dict:
        """Load skills data from JSON file"""
        try:
            skills_file = Path(__file__).parent.parent / 'assets' / 'skills_data.json'
            with open(skills_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading skills data: {e}")
            return self._get_default_skills_data()
    
    def _get_default_skills_data(self) -> Dict:
        """Fallback skills data"""
        return {
            "positions": {
                "software_engineer": {
                    "required": ["python", "java", "git"],
                    "preferred": ["docker", "kubernetes", "aws"],
                    "related": ["jenkins", "terraform", "ansible"]
                },
                "embedded_developer": {
                    "required": ["c", "c++", "linux"],
                    "preferred": ["rust", "python", "git"],
                    "related": ["rtos", "arm", "vxworks"]
                },
                "test_engineer": {
                    "required": ["python", "selenium", "git"],
                    "preferred": ["java", "jenkins", "jira"],
                    "related": ["cucumber", "robot", "junit"]
                }
            },
            "skill_relationships": {
                "python": ["django", "flask", "fastapi"],
                "c++": ["qt", "boost", "cmake"],
                "git": ["github", "gitlab", "bitbucket"],
                "linux": ["bash", "systemd", "docker"]
            }
        }
    
    def recommend_skills(self, position: str, current_skills: List[str]) -> Dict:
        """Generate skill recommendations based on position and current skills"""
        position = position.lower().replace(' ', '_')
        current_skills = [skill.lower() for skill in current_skills]
        
        if position not in self.skills_data["positions"]:
            return {
                "status": "error",
                "message": f"Position '{position}' not found in skills database",
                "recommendations": {}
            }
        
        position_skills = self.skills_data["positions"][position]
        
        # Find missing required skills
        missing_required = self._get_missing_skills(
            current_skills, 
            position_skills["required"]
        )
        
        # Find missing preferred skills
        missing_preferred = self._get_missing_skills(
            current_skills, 
            position_skills["preferred"]
        )
        
        # Find related skills based on current skillset
        related_skills = self._get_related_skills(current_skills)
        
        # Generate skill growth path
        skill_path = self._generate_skill_path(
            current_skills,
            position_skills,
            missing_required,
            missing_preferred
        )
        
        return {
            "status": "success",
            "position": position,
            "current_skills": current_skills,
            "recommendations": {
                "missing_required": list(missing_required),
                "missing_preferred": list(missing_preferred),
                "related_skills": list(related_skills),
                "skill_path": skill_path
            }
        }
    
    def _get_missing_skills(self, current: List[str], required: List[str]) -> Set[str]:
        """Find missing skills from required list"""
        return set(required) - set(current)
    
    def _get_related_skills(self, current_skills: List[str]) -> Set[str]:
        """Find related skills based on current skillset"""
        related = set()
        for skill in current_skills:
            if skill in self.skills_data["skill_relationships"]:
                related.update(self.skills_data["skill_relationships"][skill])
        return related - set(current_skills)
    
    def _generate_skill_path(
        self, 
        current: List[str],
        position_skills: Dict,
        missing_required: Set[str],
        missing_preferred: Set[str]
    ) -> List[Dict]:
        """Generate a prioritized skill learning path"""
        path = []
        
        # First priority: missing required skills
        for skill in missing_required:
            path.append({
                "skill": skill,
                "priority": "high",
                "reason": "Required for position"
            })
        
        # Second priority: missing preferred skills
        for skill in missing_preferred:
            path.append({
                "skill": skill,
                "priority": "medium",
                "reason": "Preferred for position"
            })
        
        # Third priority: related skills
        for skill in position_skills["related"]:
            if skill not in current:
                path.append({
                    "skill": skill,
                    "priority": "low",
                    "reason": "Enhances skillset"
                })
        
        return path