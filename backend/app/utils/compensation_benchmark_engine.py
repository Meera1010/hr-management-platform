"""
Compensation Benchmark & Compa-Ratio Analytics Engine.
Calculates employee salary competitiveness ratios against market median pay benchmarks,
salary band percentile distributions, and merit increase budget allocations.
"""

from typing import Dict, Any, List

class CompensationBenchmarkEngine:

    @staticmethod
    def calculate_compa_ratio(annual_ctc: float, market_median_ctc: float) -> Dict[str, Any]:
        """
        Calculates Compa-Ratio:
        Compa-Ratio = (Annual CTC / Market Median CTC) * 100
        - < 80%: Below Market Standard (High Attrition Risk)
        - 80% - 120%: Within Competitive Market Range
        - > 120%: Premium Market Segment
        """
        if market_median_ctc <= 0:
            return {'compa_ratio_pct': 100.0, 'competitiveness_band': 'At Market Median'}

        compa_ratio = (annual_ctc / float(market_median_ctc)) * 100.0
        compa_ratio_round = round(compa_ratio, 1)

        if compa_ratio_round < 80.0:
            band = 'Below Market'
        elif compa_ratio_round <= 120.0:
            band = 'Competitive Market'
        else:
            band = 'Above Market'

        return {
            'annual_ctc': annual_ctc,
            'market_median_ctc': market_median_ctc,
            'compa_ratio_pct': compa_ratio_round,
            'competitiveness_band': band
        }

    @staticmethod
    def calculate_merit_increase_matrix(performance_score: float, current_compa_ratio: float) -> float:
        """
        Merit Matrix Rule Engine:
        Higher performance score + lower compa-ratio yields higher salary percentage increase.
        """
        base_increase = (performance_score / 5.0) * 10.0  # Max 10% base

        if current_compa_ratio < 80.0:
            adjustment = 2.5  # Salary adjustment boost
        elif current_compa_ratio > 110.0:
            adjustment = -1.5 # Salary cap slowdown
        else:
            adjustment = 0.0

        recommended_increase_pct = max(0.0, base_increase + adjustment)
        return round(recommended_increase_pct, 2)
