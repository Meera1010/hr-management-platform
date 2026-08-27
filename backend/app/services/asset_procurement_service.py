"""
Asset Procurement, Depreciation Calculator & Warranty Expiration Alert Engine.
Calculates Straight-Line & Written Down Value (WDV) depreciation for IT assets,
and monitors hardware warranty expiration timelines.
"""

from typing import Dict, Any, List
from datetime import datetime, date

class AssetProcurementService:

    @staticmethod
    def calculate_straight_line_depreciation(purchase_cost: float, salvage_value: float, useful_life_years: int, current_age_years: float) -> Dict[str, Any]:
        """Calculates straight-line depreciation per year and current book value."""
        if useful_life_years <= 0:
            useful_life_years = 3

        annual_depreciation = (purchase_cost - salvage_value) / useful_life_years
        accumulated_depreciation = min(purchase_cost - salvage_value, annual_depreciation * current_age_years)
        current_book_value = max(salvage_value, purchase_cost - accumulated_depreciation)

        return {
            'purchase_cost': purchase_cost,
            'salvage_value': salvage_value,
            'useful_life_years': useful_life_years,
            'annual_depreciation': round(annual_depreciation, 2),
            'accumulated_depreciation': round(accumulated_depreciation, 2),
            'current_book_value': round(current_book_value, 2)
        }

    @staticmethod
    def calculate_wdv_depreciation(purchase_cost: float, rate_pct: float, age_years: int) -> Dict[str, Any]:
        """Calculates Written Down Value (WDV) depreciation (standard IT rate = 40%)."""
        current_val = purchase_cost
        schedule = []

        for year in range(1, age_years + 1):
            dep_amount = current_val * (rate_pct / 100.0)
            ending_val = current_val - dep_amount
            schedule.append({
                'year': year,
                'beginning_value': round(current_val, 2),
                'depreciation_amount': round(dep_amount, 2),
                'ending_value': round(ending_val, 2)
            })
            current_val = ending_val

        return {
            'purchase_cost': purchase_cost,
            'depreciation_rate_pct': rate_pct,
            'current_book_value': round(current_val, 2),
            'schedule': schedule
        }

    @staticmethod
    def check_warranty_expirations(assets: List[Dict[str, Any]], days_threshold: int = 60) -> List[Dict[str, Any]]:
        """Identifies IT assets whose hardware warranties expire within N days."""
        expiring = []
        today = date.today()

        for a in assets:
            w_date_str = a.get('warranty_expiry_date')
            if not w_date_str:
                continue

            try:
                w_date = datetime.strptime(w_date_str, '%Y-%m-%d').date()
                days_remaining = (w_date - today).days

                if 0 <= days_remaining <= days_threshold:
                    expiring.append({
                        'asset_tag': a.get('asset_tag'),
                        'name': a.get('name'),
                        'serial_number': a.get('serial_number'),
                        'warranty_expiry_date': w_date_str,
                        'days_remaining': days_remaining,
                        'status': a.get('status')
                    })
            except ValueError:
                continue

        return expiring
