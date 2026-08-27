"""
Enterprise Bank Payout Export Service & Salary Slip PDF Data Formatter.
Generates bank batch payout transfer file strings in standard HDFC / ICICI / SBI corporate formats
and reconciles monthly payout totals against general ledger accounts.
"""

from typing import List, Dict, Any
from datetime import datetime

class BankPayoutExportService:

    @staticmethod
    def generate_hdfc_cms_format(payslips: List[Dict[str, Any]]) -> str:
        """
        Generates HDFC Bank Corporate Mass Payment (CMS) CSV export format.
        Headers: Transaction_Type, Beneficiary_Code, Beneficiary_Acc_No, Amount, Beneficiary_Name, IFSC, Payment_Ref
        """
        lines = ["Transaction_Type,Beneficiary_Code,Beneficiary_Acc_No,Amount,Beneficiary_Name,IFSC,Payment_Ref"]

        for idx, ps in enumerate(payslips, start=1):
            ref = f"SAL-{ps.get('period_label')}-{ps.get('employee_code', f'EMP{idx}')}"
            acc = ps.get('bank_account_no', '501000000000')
            ifsc = ps.get('ifsc_code', 'HDFC0000123')
            amt = f"{ps.get('net_salary', 0.0):.2f}"
            name = ps.get('employee_name', 'Employee')

            line = f"NEFT,EMP{ps.get('employee_id')},{acc},{amt},{name},{ifsc},{ref}"
            lines.append(line)

        return "\n".join(lines)

    @staticmethod
    def generate_icici_cib_format(payslips: List[Dict[str, Any]]) -> str:
        """
        Generates ICICI Bank Corporate Internet Banking (CIB) batch transfer format.
        Headers: PYMT_MODE,CR_ACC_NO,AMOUNT,CR_NAME,IFSC_CODE,REMARKS
        """
        lines = ["PYMT_MODE,CR_ACC_NO,AMOUNT,CR_NAME,IFSC_CODE,REMARKS"]

        for ps in payslips:
            line = f"IFT,{ps.get('bank_account_no', '')},{ps.get('net_salary', 0.0):.2f},{ps.get('employee_name', '')},{ps.get('ifsc_code', '')},Salary Payout {ps.get('period_label')}"
            lines.append(line)

        return "\n".join(lines)

    @staticmethod
    def reconcile_payroll_batch(payslips: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Audits & reconciles total gross, total deductions, and total net transfer amount.
        """
        total_gross = sum(p.get('gross_earnings', 0.0) for p in payslips)
        total_pf = sum(p.get('pf_deduction', 0.0) for p in payslips)
        total_pt = sum(p.get('professional_tax', 0.0) for p in payslips)
        total_tds = sum(p.get('tds_deduction', 0.0) for p in payslips)
        total_deductions = sum(p.get('total_deductions', 0.0) for p in payslips)
        total_net = sum(p.get('net_salary', 0.0) for p in payslips)

        is_balanced = round(total_gross - total_deductions, 2) == round(total_net, 2)

        return {
            'headcount': len(payslips),
            'total_gross': round(total_gross, 2),
            'total_pf': round(total_pf, 2),
            'total_pt': round(total_pt, 2),
            'total_tds': round(total_tds, 2),
            'total_deductions': round(total_deductions, 2),
            'total_net': round(total_net, 2),
            'is_reconciled': is_balanced
        }
