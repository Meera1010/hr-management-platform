"""
Learning Experience Platform Assessment Engine & Skill Matrix Gap Analyzer.
Matches employee completed training courses against required departmental skills
and calculates skill proficiency gaps.
"""

from typing import Dict, Any, List

class SkillMatrixAnalyzer:

    @staticmethod
    def calculate_employee_skill_gap(employee_skills: List[str], required_skills: List[str]) -> Dict[str, Any]:
        """Calculates skill coverage percentage and missing skill gaps."""
        emp_set = set(s.strip().lower() for s in employee_skills)
        req_set = set(s.strip().lower() for s in required_skills)

        if not req_set:
            return {'match_pct': 100.0, 'matched_skills': [], 'missing_skills': []}

        matched = emp_set.intersection(req_set)
        missing = req_set - emp_set

        pct = round((len(matched) / len(req_set) * 100.0), 1)

        return {
            'match_pct': pct,
            'matched_skills': list(matched),
            'missing_skills': list(missing),
            'total_required': len(req_set),
            'total_matched': len(matched)
        }
