import pytest
from app.services.learning_assessment_engine import SkillMatrixAnalyzer

def test_skill_gap_analysis():
    emp_skills = ['Python', 'Flask', 'SQL', 'Docker']
    req_skills = ['Python', 'Flask', 'SQLAlchemy', 'Docker', 'Kubernetes']

    res = SkillMatrixAnalyzer.calculate_employee_skill_gap(emp_skills, req_skills)
    assert res['match_pct'] == 60.0
    assert 'python' in res['matched_skills']
    assert 'kubernetes' in res['missing_skills']
    assert len(res['missing_skills']) == 2
