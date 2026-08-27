import pytest
from app.services.learning_assessment_engine import SkillMatrixAnalyzer

def test_skill_matrix_gap_analysis():
    analysis = SkillMatrixAnalyzer.calculate_employee_skill_gap(
        employee_skills=['Python', 'Flask'],
        required_skills=['Python', 'Flask', 'Docker', 'Kubernetes']
    )
    assert analysis['match_pct'] == 50.0
    assert len(analysis['missing_skills']) == 2
    assert 'docker' in analysis['missing_skills']
