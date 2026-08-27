import pytest
from app.services.okr_analytics_engine import OkrAnalyticsEngine

def test_department_okr_health_score():
    health = OkrAnalyticsEngine.compute_department_okr_health([
        {'progress_pct': 90.0, 'status': 'Completed'},
        {'progress_pct': 60.0, 'status': 'On Track'},
        {'progress_pct': 30.0, 'status': 'At Risk'}
    ])
    assert health['avg_progress_pct'] == 60.0
    assert health['completed'] == 1
    assert health['at_risk'] == 1

def test_360_feedback_competency_radar():
    radar = OkrAnalyticsEngine.format_360_radar_matrix([
        {'leadership_score': 4.0, 'technical_score': 4.0, 'communication_score': 5.0, 'teamwork_score': 4.0, 'overall_rating': 4.25},
        {'leadership_score': 4.0, 'technical_score': 4.0, 'communication_score': 4.0, 'teamwork_score': 4.0, 'overall_rating': 4.0}
    ])
    assert radar['leadership'] == 4.0
    assert radar['technical'] == 4.0
    assert radar['communication'] == 4.5
