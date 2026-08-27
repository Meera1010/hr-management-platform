"""
Shift Roster Optimization & Conflict Resolution Engine.
Validates shift overlap rules, mandatory rest periods between consecutive shifts (min 11 hours),
and detects employee schedule conflicts.
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta

class ShiftRosterOptimizer:

    @staticmethod
    def validate_rest_period_compliance(previous_shift_end: datetime, next_shift_start: datetime, min_rest_hours: float = 11.0) -> Dict[str, Any]:
        """
        Labor Rule: Minimum 11 consecutive hours of rest required between two daily work shifts.
        """
        if next_shift_start <= previous_shift_end:
            return {'is_compliant': False, 'rest_hours': 0.0, 'reason': 'Shift overlap error'}

        rest_seconds = (next_shift_start - previous_shift_end).total_seconds()
        rest_hours = rest_seconds / 3600.0

        is_compliant = rest_hours >= min_rest_hours

        return {
            'previous_shift_end': previous_shift_end.isoformat(),
            'next_shift_start': next_shift_start.isoformat(),
            'rest_hours': round(rest_hours, 2),
            'min_rest_hours': min_rest_hours,
            'is_compliant': is_compliant,
            'status': 'Compliant Rest Window' if is_compliant else f"Rest violation: Only {round(rest_hours, 1)} hrs rest provided (min {min_rest_hours} hrs required)"
        }
