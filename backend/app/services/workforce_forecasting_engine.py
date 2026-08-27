"""
Workforce Headcount Forecasting & Market Salary Parity Analytics Engine.
Calculates quarterly headcount projections, annual turnover percentages,
and salary parity disparity indices against market medians.
"""

from typing import Dict, Any, List

class WorkforceForecastingEngine:

    @staticmethod
    def calculate_turnover_rate(starting_headcount: int, ending_headcount: int, exits_count: int) -> Dict[str, Any]:
        """Calculates annual employee turnover rate percentage."""
        avg_headcount = (starting_headcount + ending_headcount) / 2.0
        if avg_headcount <= 0:
            return {'turnover_rate_pct': 0.0, 'avg_headcount': 0}

        rate = round((exits_count / avg_headcount * 100.0), 1)
        return {
            'starting_headcount': starting_headcount,
            'ending_headcount': ending_headcount,
            'exits_count': exits_count,
            'avg_headcount': avg_headcount,
            'turnover_rate_pct': rate
        }

    @staticmethod
    def calculate_salary_competitiveness(company_avg_ctc: float, market_median_ctc: float) -> Dict[str, Any]:
        """Calculates competitive ratio (Compa-Ratio) and market parity gap."""
        if market_median_ctc <= 0:
            return {'compa_ratio': 1.0, 'parity_gap_pct': 0.0, 'positioning': 'Market Parity'}

        compa_ratio = round(company_avg_ctc / market_median_ctc, 2)
        parity_gap_pct = round(((company_avg_ctc - market_median_ctc) / market_median_ctc * 100.0), 1)

        positioning = 'Above Market Median' if compa_ratio > 1.05 else ('Below Market Median' if compa_ratio < 0.95 else 'Market Parity')

        return {
            'company_avg_ctc': company_avg_ctc,
            'market_median_ctc': market_median_ctc,
            'compa_ratio': compa_ratio,
            'parity_gap_pct': parity_gap_pct,
            'positioning': positioning
        }
