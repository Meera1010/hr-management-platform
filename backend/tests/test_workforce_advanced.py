import pytest
from app.services.workforce_forecasting_engine import WorkforceForecastingEngine

def test_turnover_rate_calculation():
    res = WorkforceForecastingEngine.calculate_turnover_rate(starting_headcount=100, ending_headcount=110, exits_count=5)
    assert res['avg_headcount'] == 105.0
    assert res['turnover_rate_pct'] == 4.8

def test_salary_competitiveness_compa_ratio():
    res1 = WorkforceForecastingEngine.calculate_salary_competitiveness(company_avg_ctc=1650000.0, market_median_ctc=1500000.0)
    assert res1['compa_ratio'] == 1.1
    assert res1['positioning'] == 'Above Market Median'

    res2 = WorkforceForecastingEngine.calculate_salary_competitiveness(company_avg_ctc=1200000.0, market_median_ctc=1500000.0)
    assert res2['compa_ratio'] == 0.8
    assert res2['positioning'] == 'Below Market Median'
