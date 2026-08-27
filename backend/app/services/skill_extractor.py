import re
from app.models.skill import Skill

class SkillExtractor:
    @staticmethod
    def extract_skills(text: str, available_skills: list = None) -> list:
        """
        AI-assisted rule-based skill extraction using word/phrase boundaries.
        Case-insensitive matching that prevents duplicates.
        """
        if not text:
            return []

        # If available_skills is not provided, fetch from DB
        if available_skills is None:
            try:
                skills_query = Skill.query.all()
                skill_names = [s.name for s in skills_query]
            except Exception:
                skill_names = []
        else:
            skill_names = available_skills

        if not skill_names:
            # Fallback default skills list if DB is empty
            skill_names = [
                'Python', 'Java', 'JavaScript', 'React', 'Node.js', 'Flask', 'Django',
                'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'HTML', 'CSS', 'Git', 'Linux',
                'Docker', 'AWS', 'Azure', 'Cybersecurity', 'Networking', 'Nmap',
                'Wireshark', 'Burp Suite', 'Machine Learning', 'Data Analysis'
            ]

        extracted = []

        for skill in skill_names:
            # Escape skill name for regex and use word boundaries
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text, re.IGNORECASE):
                if skill not in extracted:
                    extracted.append(skill)

        return extracted
