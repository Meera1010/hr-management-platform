"""
Advanced Income Tax & Deduction Calculation Engine for Indian Tax Regimes (FY 2026-2027).
Provides detailed calculation breakdowns for Old vs New Tax Regimes, Section 80C, 80D, 24B, 80E exemptions,
Standard Deductions, Surcharge, Health & Education Cess, and Monthly Tax Deduction at Source (TDS) schedules.
"""

from typing import Dict, Any, List

class TaxRegimeCalculator:
    STANDARD_DEDUCTION_NEW_REGIME = 75000.0
    STANDARD_DEDUCTION_OLD_REGIME = 50000.0
    CESS_RATE = 0.04

    @staticmethod
    def calculate_new_regime_tax(gross_annual_income: float) -> Dict[str, Any]:
        """
        Calculates tax under New Tax Regime slabs (FY 2026-27):
        0 - 3,00,000: Nil
        3,00,001 - 7,00,000: 5%
        7,00,001 - 10,00,000: 10%
        10,00,001 - 12,00,000: 15%
        12,00,001 - 15,00,000: 20%
        Above 15,00,000: 30%
        Rebate u/s 87A: Up to Rs. 25,000 for taxable income <= 7,00,000 (effective zero tax up to 7.75 Lakhs with std deduction).
        """
        taxable_income = max(0.0, gross_annual_income - TaxRegimeCalculator.STANDARD_DEDUCTION_NEW_REGIME)
        tax = 0.0
        slabs = []

        if taxable_income > 1500000.0:
            income_in_slab = taxable_income - 1500000.0
            slab_tax = income_in_slab * 0.30
            tax += slab_tax
            slabs.append({'slab': 'Above 15.0L', 'rate': '30%', 'taxable_amount': income_in_slab, 'tax': slab_tax})

        if taxable_income > 1200000.0:
            income_in_slab = min(taxable_income, 1500000.0) - 1200000.0
            slab_tax = income_in_slab * 0.20
            tax += slab_tax
            slabs.append({'slab': '12.0L - 15.0L', 'rate': '20%', 'taxable_amount': income_in_slab, 'tax': slab_tax})

        if taxable_income > 1000000.0:
            income_in_slab = min(taxable_income, 1200000.0) - 1000000.0
            slab_tax = income_in_slab * 0.15
            tax += slab_tax
            slabs.append({'slab': '10.0L - 12.0L', 'rate': '15%', 'taxable_amount': income_in_slab, 'tax': slab_tax})

        if taxable_income > 700000.0:
            income_in_slab = min(taxable_income, 1000000.0) - 700000.0
            slab_tax = income_in_slab * 0.10
            tax += slab_tax
            slabs.append({'slab': '7.0L - 10.0L', 'rate': '10%', 'taxable_amount': income_in_slab, 'tax': slab_tax})

        if taxable_income > 300000.0:
            income_in_slab = min(taxable_income, 700000.0) - 300000.0
            slab_tax = income_in_slab * 0.05
            tax += slab_tax
            slabs.append({'slab': '3.0L - 7.0L', 'rate': '5%', 'taxable_amount': income_in_slab, 'tax': slab_tax})

        # Rebate u/s 87A
        rebate = 0.0
        if taxable_income <= 700000.0:
            rebate = min(tax, 25000.0)

        tax_after_rebate = max(0.0, tax - rebate)
        cess = tax_after_rebate * TaxRegimeCalculator.CESS_RATE
        total_tax = tax_after_rebate + cess

        return {
            'regime': 'New',
            'gross_income': gross_annual_income,
            'standard_deduction': TaxRegimeCalculator.STANDARD_DEDUCTION_NEW_REGIME,
            'taxable_income': taxable_income,
            'slabs': slabs,
            'gross_tax': round(tax, 2),
            'rebate_87a': round(rebate, 2),
            'tax_after_rebate': round(tax_after_rebate, 2),
            'cess': round(cess, 2),
            'total_annual_tax': round(total_tax, 2),
            'monthly_tds': round(total_tax / 12.0, 2)
        }

    @staticmethod
    def calculate_old_regime_tax(gross_annual_income: float, exemptions: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculates tax under Old Tax Regime with deductions:
        - 80C (PPF, ELSS, EPF, LIC) up to 1.5 Lakhs
        - 80D (Health Insurance) up to 25,000 (Self) + 50,000 (Senior Parents)
        - Section 24 (Home Loan Interest) up to 2.0 Lakhs
        - HRA exemption
        """
        sec_80c = min(float(exemptions.get('sec_80c', 0.0)), 150000.0)
        sec_80d = min(float(exemptions.get('sec_80d', 0.0)), 75000.0)
        sec_24b = min(float(exemptions.get('sec_24b', 0.0)), 200000.0)
        hra_exemption = float(exemptions.get('hra_exemption', 0.0))
        other_ex = float(exemptions.get('other_exemptions', 0.0))

        total_deductions = TaxRegimeCalculator.STANDARD_DEDUCTION_OLD_REGIME + sec_80c + sec_80d + sec_24b + hra_exemption + other_ex
        taxable_income = max(0.0, gross_annual_income - total_deductions)

        tax = 0.0
        slabs = []

        if taxable_income > 1000000.0:
            income_in_slab = taxable_income - 1000000.0
            slab_tax = income_in_slab * 0.30
            tax += slab_tax
            slabs.append({'slab': 'Above 10.0L', 'rate': '30%', 'taxable_amount': income_in_slab, 'tax': slab_tax})

        if taxable_income > 500000.0:
            income_in_slab = min(taxable_income, 1000000.0) - 500000.0
            slab_tax = income_in_slab * 0.20
            tax += slab_tax
            slabs.append({'slab': '5.0L - 10.0L', 'rate': '20%', 'taxable_amount': income_in_slab, 'tax': slab_tax})

        if taxable_income > 250000.0:
            income_in_slab = min(taxable_income, 500000.0) - 250000.0
            slab_tax = income_in_slab * 0.05
            tax += slab_tax
            slabs.append({'slab': '2.5L - 5.0L', 'rate': '5%', 'taxable_amount': income_in_slab, 'tax': slab_tax})

        rebate = 0.0
        if taxable_income <= 500000.0:
            rebate = min(tax, 12500.0)

        tax_after_rebate = max(0.0, tax - rebate)
        cess = tax_after_rebate * TaxRegimeCalculator.CESS_RATE
        total_tax = tax_after_rebate + cess

        return {
            'regime': 'Old',
            'gross_income': gross_annual_income,
            'total_exemptions_and_deductions': total_deductions,
            'taxable_income': taxable_income,
            'slabs': slabs,
            'gross_tax': round(tax, 2),
            'rebate_87a': round(rebate, 2),
            'tax_after_rebate': round(tax_after_rebate, 2),
            'cess': round(cess, 2),
            'total_annual_tax': round(total_tax, 2),
            'monthly_tds': round(total_tax / 12.0, 2)
        }

    @staticmethod
    def compare_regimes(gross_annual_income: float, exemptions: Dict[str, float]) -> Dict[str, Any]:
        """Compares New vs Old Tax Regime and recommends the tax-saving option."""
        new_res = TaxRegimeCalculator.calculate_new_regime_tax(gross_annual_income)
        old_res = TaxRegimeCalculator.calculate_old_regime_tax(gross_annual_income, exemptions)

        diff = round(old_res['total_annual_tax'] - new_res['total_annual_tax'], 2)
        recommended = 'New' if new_res['total_annual_tax'] <= old_res['total_annual_tax'] else 'Old'
        savings = abs(diff)

        return {
            'gross_income': gross_annual_income,
            'new_regime': new_res,
            'old_regime': old_res,
            'recommended_regime': recommended,
            'annual_savings': savings,
            'monthly_savings': round(savings / 12.0, 2)
        }
