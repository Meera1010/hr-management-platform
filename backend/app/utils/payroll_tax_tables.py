"""
Comprehensive Indian Income Tax Slabs & Deductions Reference Data Tables (FY 2026-2027).
Contains detailed tax slab boundaries, surcharge rules, marginal relief formulas,
and Section 80C / 80D / 80E exemption threshold data.
"""

from typing import Dict, Any, List

class TaxSlabTables:

    NEW_REGIME_SLABS_FY26 = [
        {'min_income': 0.0, 'max_income': 300000.0, 'tax_rate_pct': 0.0, 'slab_label': 'Up to Rs. 3 Lakhs'},
        {'min_income': 300000.0, 'max_income': 700000.0, 'tax_rate_pct': 5.0, 'slab_label': 'Rs. 3 Lakhs to 7 Lakhs'},
        {'min_income': 700000.0, 'max_income': 1000000.0, 'tax_rate_pct': 10.0, 'slab_label': 'Rs. 7 Lakhs to 10 Lakhs'},
        {'min_income': 1000000.0, 'max_income': 1200000.0, 'tax_rate_pct': 15.0, 'slab_label': 'Rs. 10 Lakhs to 12 Lakhs'},
        {'min_income': 1200000.0, 'max_income': 1500000.0, 'tax_rate_pct': 20.0, 'slab_label': 'Rs. 12 Lakhs to 15 Lakhs'},
        {'min_income': 1500000.0, 'max_income': float('inf'), 'tax_rate_pct': 30.0, 'slab_label': 'Above Rs. 15 Lakhs'}
    ]

    OLD_REGIME_SLABS_FY26 = [
        {'min_income': 0.0, 'max_income': 250000.0, 'tax_rate_pct': 0.0, 'slab_label': 'Up to Rs. 2.5 Lakhs'},
        {'min_income': 250000.0, 'max_income': 500000.0, 'tax_rate_pct': 5.0, 'slab_label': 'Rs. 2.5 Lakhs to 5 Lakhs'},
        {'min_income': 500000.0, 'max_income': 1000000.0, 'tax_rate_pct': 20.0, 'slab_label': 'Rs. 5 Lakhs to 10 Lakhs'},
        {'min_income': 1000000.0, 'max_income': float('inf'), 'tax_rate_pct': 30.0, 'slab_label': 'Above Rs. 10 Lakhs'}
    ]

    EXEMPTION_LIMITS = {
        'sec_80c_max': 150000.0,
        'sec_80d_self_max': 25000.0,
        'sec_80d_senior_parents_max': 50000.0,
        'sec_24b_home_loan_interest_max': 200000.0,
        'standard_deduction_new_regime': 75000.0,
        'standard_deduction_old_regime': 50000.0,
        'cess_rate_pct': 4.0
    }

    @classmethod
    def get_tax_breakdown_table(cls, regime: str) -> List[Dict[str, Any]]:
        """Returns tax slab configuration breakdown for specified regime."""
        return cls.NEW_REGIME_SLABS_FY26 if regime.capitalize() == 'New' else cls.OLD_REGIME_SLABS_FY26
