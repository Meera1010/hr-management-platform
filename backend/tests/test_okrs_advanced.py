import pytest
from app.services.okr_analytics_engine import OkrAnalyticsEngine

def test_department_okr_health():
    objectives = [
        {'title': 'Uptime 99.9%', 'progress_pct': 100.0, 'status': 'Completed'},
        {'title': 'Reduce Latency', 'progress_pct': 80.0, 'status': 'On Track'},
        {'title': 'Refactor Legacy API', 'progress_pct': 30.0, 'status': 'Behind'}
    ]
    res = OkrAnalyticsEngine.compute_department_okr_health(objectives)
    assert res['total_okrs'] == 3
    assert res['completed'] == 1
    assert res['on_track'] == 1
    assert res['behind'] == 1

def test_360_radar_matrix():
    feedbacks = [
        {'leadership_score': 4.5, 'technical_score': 4.8, 'communication_score': 4.0, 'teamwork_score': 4.5, 'overall_rating': 4.5},
        {'leadership_score': 4.0, 'technical_score': 4.2, 'communication_score': 4.5, 'teamwork_score': 4.5, 'overall_rating': 4.3}
    ]
    matrix = OkrAnalyticsEngine.format_360_radar_matrix(feedbacks)
    assert matrix['leadership'] == 4.25
    assert matrix['technical'] == 4.5
    assert matrix['total_evaluators'] == 2
