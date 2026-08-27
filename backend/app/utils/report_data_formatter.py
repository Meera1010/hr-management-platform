"""
Executive Data Formatter & CSV / PDF Export Data Adapter.
Formats raw database query aggregates into clean, localized tabular datasets for executive reporting.
"""

from typing import Dict, Any, List

class ReportDataFormatter:

    @staticmethod
    def format_headcount_summary(departments_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Formats department headcount and salary cost summary table."""
        formatted_rows = []
        grand_headcount = 0
        grand_monthly_cost = 0.0

        for d in departments_data:
            hc = int(d.get('employee_count', 0))
            cost = float(d.get('monthly_payroll_cost', 0.0))
            grand_headcount += hc
            grand_monthly_cost += cost

            formatted_rows.append({
                'department_code': d.get('code', 'N/A'),
                'department_name': d.get('name', 'Unknown'),
                'headcount': hc,
                'monthly_payroll_cost_formatted': f"₹{cost:,.2f}",
                'avg_cost_per_employee': f"₹{(cost / hc if hc > 0 else 0):,.2f}"
            })

        return {
            'grand_headcount': grand_headcount,
            'grand_monthly_cost': grand_monthly_cost,
            'grand_monthly_cost_formatted': f"₹{grand_monthly_cost:,.2f}",
            'rows': formatted_rows
        }

    @staticmethod
    def format_csv_export_string(headers: List[str], rows: List[List[Any]]) -> str:
        """Generates standard RFC 4180 compliant CSV text string."""
        lines = [",".join(f'"{h}"' for h in headers)]

        for r in rows:
            line = ",".join(f'"{str(val)}"' for val in r)
            lines.append(line)

        return "\n".join(lines)
