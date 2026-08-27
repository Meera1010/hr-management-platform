import pytest
from datetime import datetime
from app.utils.payroll_tax_tables import TaxSlabTables
from app.utils.compensation_benchmark_engine import CompensationBenchmarkEngine
from app.utils.recruitment_pipeline_analytics import RecruitmentPipelineAnalytics
from app.utils.shift_roster_optimizer import ShiftRosterOptimizer

def test_tax_slab_tables_new_regime():
    slabs = TaxSlabTables.get_tax_breakdown_table('New')
    assert len(slabs) == 6
    assert slabs[0]['tax_rate_pct'] == 0.0

def test_compa_ratio_calculation():
    comp = CompensationBenchmarkEngine.calculate_compa_ratio(1200000.0, 1200000.0)
    assert comp['compa_ratio_pct'] == 100.0
    assert comp['competitiveness_band'] == 'Competitive Market'

def test_merit_increase_matrix():
    pct = CompensationBenchmarkEngine.calculate_merit_increase_matrix(performance_score=4.5, current_compa_ratio=75.0)
    assert pct > 10.0  # Includes low compa-ratio boost

def test_recruitment_funnel_conversion():
    funnel = RecruitmentPipelineAnalytics.calculate_funnel_conversion([
        {'status': 'Applied'},
        {'status': 'Shortlisted'},
        {'status': 'Interview Scheduled'},
        {'status': 'Hired'}
    ])
    assert funnel['total_applied'] == 4
    assert funnel['hired'] == 1
    assert funnel['hire_conversion_rate_pct'] == 25.0

def test_rest_period_compliance_valid():
    prev_end = datetime(2026, 5, 1, 18, 0, 0)
    next_start = datetime(2026, 5, 2, 9, 0, 0) # 15 hrs rest
    res = ShiftRosterOptimizer.validate_rest_period_compliance(prev_end, next_start)
    assert res['is_compliant'] is True
    assert res['rest_hours'] == 15.0

def test_rest_period_compliance_violation():
    prev_end = datetime(2026, 5, 1, 23, 0, 0)
    next_start = datetime(2026, 5, 2, 6, 0, 0) # 7 hrs rest
    res = ShiftRosterOptimizer.validate_rest_period_compliance(prev_end, next_start)
    assert res['is_compliant'] is False
    assert res['rest_hours'] == 7.0
