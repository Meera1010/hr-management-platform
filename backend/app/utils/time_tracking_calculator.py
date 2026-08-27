"""
Time Tracking, Shift Differential & Attendance Hours Calculator.
Calculates net work hours, meal break deductions, night shift differentials,
and flex-time schedule compliance.
"""

from typing import Dict, Any, List
from datetime import datetime, time, timedelta

class TimeTrackingCalculator:

    @staticmethod
    def calculate_net_shift_hours(clock_in: datetime, clock_out: datetime, break_minutes: int = 60) -> Dict[str, Any]:
        """Calculates gross duration, break deduction, and net work hours."""
        if clock_out <= clock_in:
            return {'gross_hours': 0.0, 'net_hours': 0.0, 'break_minutes': break_minutes}

        gross_seconds = (clock_out - clock_in).total_seconds()
        gross_hours = gross_seconds / 3600.0
        break_hours = break_minutes / 60.0

        net_hours = max(0.0, gross_hours - break_hours)

        return {
            'clock_in': clock_in.isoformat(),
            'clock_out': clock_out.isoformat(),
            'gross_hours': round(gross_hours, 2),
            'break_minutes': break_minutes,
            'net_hours': round(net_hours, 2)
        }

    @staticmethod
    def calculate_night_shift_differential(clock_in: datetime, clock_out: datetime, night_start_hour: int = 22, night_end_hour: int = 6) -> float:
        """
        Calculates number of hours worked during night shift window (10:00 PM to 6:00 AM).
        Night shift hours attract a 15% shift differential allowance.
        """
        night_hours = 0.0
        current = clock_in

        while current < clock_out:
            if current.hour >= night_start_hour or current.hour < night_end_hour:
                night_hours += 0.25  # 15 minute interval steps
            current += timedelta(minutes=15)

        return round(night_hours, 2)
