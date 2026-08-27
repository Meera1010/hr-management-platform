"""
Enterprise Skill Gap Matrix & Organizational Proficiency Engine.
Maps team skill competencies against target role benchmarks, calculates team coverage scores,
and generates personalized learning path recommendations.
"""

from typing import Dict, Any, List

class SkillGapMatrixEngine:

    @staticmethod
    def calculate_team_competency_matrix(team_skills: List[Dict[str, Any]], required_role_skills: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluates team skill readiness:
        - team_skills: [{'employee_id': 1, 'skill_name': 'Python', 'proficiency_level': 4}]
        - required_role_skills: [{'skill_name': 'Python', 'min_proficiency': 3}]
        """
        role_map = {s['skill_name'].lower(): s.get('min_proficiency', 3) for s in required_role_skills}
        skill_coverage = {}

        for skill, min_prof in role_map.items():
            matching_members = [
                m for m in team_skills
                if m.get('skill_name', '').lower() == skill and m.get('proficiency_level', 0) >= min_prof
            ]
            skill_coverage[skill] = {
                'min_proficiency_required': min_prof,
                'qualified_member_count': len(matching_members),
                'qualified_employee_ids': [m.get('employee_id') for m in matching_members],
                'is_covered': len(matching_members) > 0
            }

        total_skills = len(role_map)
        covered_count = sum(1 for v in skill_coverage.values() if v['is_covered'])
        coverage_pct = round((covered_count / float(total_skills) * 100.0), 1) if total_skills > 0 else 100.0

        return {
            'total_role_skills': total_skills,
            'covered_skills_count': covered_count,
            'overall_team_coverage_pct': coverage_pct,
            'skill_details': skill_coverage
        }

    @staticmethod
    def recommend_learning_modules(missing_skills: List[str], available_courses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Recommends internal LXP learning courses to bridge identified skill gaps."""
        recommended = []
        missing_set = set(s.lower() for s in missing_skills)

        for course in available_courses:
            c_title = course.get('title', '').lower()
            c_desc = course.get('description', '').lower()
            c_category = course.get('category', '').lower()

            for skill in missing_set:
                if skill in c_title or skill in c_desc or skill in c_category:
                    recommended.append({
                        'course_id': course.get('id'),
                        'course_title': course.get('title'),
                        'course_code': course.get('code'),
                        'duration_hours': course.get('duration_hours'),
                        'target_skill': skill.capitalize()
                    })
                    break

        return recommended
