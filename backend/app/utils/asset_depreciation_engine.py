"""
Asset Depreciation Calculations Engine.
Provides Straight-Line Method (SLM) and Written-Down Value (WDV) depreciation calculations
for IT hardware and enterprise capital assets.
"""

from typing import Dict, Any, List

class AssetDepreciationEngine:

    @staticmethod
    def calculate_straight_line_depreciation(cost: float, salvage_value: float, useful_life_years: int) -> Dict[str, Any]:
        """Calculates Straight-Line Method (SLM) depreciation."""
        if useful_life_years <= 0:
            return {'annual_depreciation': 0.0, 'monthly_depreciation': 0.0}

        annual_dep = max(0.0, cost - salvage_value) / float(useful_life_years)
        monthly_dep = annual_dep / 12.0

        return {
            'cost': cost,
            'salvage_value': salvage_value,
            'useful_life_years': useful_life_years,
            'annual_depreciation': round(annual_dep, 2),
            'monthly_depreciation': round(monthly_dep, 2)
        }

    @staticmethod
    def calculate_wdv_depreciation(cost: float, rate_pct: float, years: int) -> Dict[str, Any]:
        """Calculates Written-Down Value (WDV) / Reducing Balance depreciation schedule."""
        schedule = []
        opening_book_value = cost
        rate = rate_pct / 100.0

        for y in range(1, years + 1):
            dep_amount = round(opening_book_value * rate, 2)
            closing_book_value = round(opening_book_value - dep_amount, 2)

            schedule.append({
                'year': y,
                'opening_book_value': opening_book_value,
                'depreciation_amount': dep_amount,
                'closing_book_value': closing_book_value
            })
            opening_book_value = closing_book_value

        return {
            'cost': cost,
            'rate_pct': rate_pct,
            'years': years,
            'schedule': schedule
        }
