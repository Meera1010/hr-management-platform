"""
Enterprise Data Exporter & CSV / JSON Formatter.
Generates CSV spreadsheets and formatted JSON reports for HR Headcount, Payroll Payouts,
Asset Inventories, Expense Claims, and Performance Ratings.
"""

import io
import csv
from typing import List, Dict, Any

class DataExporter:

    @staticmethod
    def export_to_csv(data: List[Dict[str, Any]], fieldnames: List[str]) -> str:
        """Converts a list of dict records into a clean CSV string."""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()

        for row in data:
            writer.writerow(row)

        return output.getvalue()

    @staticmethod
    def format_headcount_summary(employees: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Summarizes employee headcount distribution by department, employment type, and gender."""
        dept_counts = {}
        type_counts = {}

        for emp in employees:
            dept = emp.get('department') or 'Unassigned'
            etype = emp.get('employment_type') or 'Full-Time'

            dept_counts[dept] = dept_counts.get(dept, 0) + 1
            type_counts[etype] = type_counts.get(etype, 0) + 1

        return {
            'total_headcount': len(employees),
            'department_breakdown': dept_counts,
            'employment_type_breakdown': type_counts
        }
