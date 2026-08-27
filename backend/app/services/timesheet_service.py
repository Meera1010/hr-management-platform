from app import db
from app.models.timesheet_shift import Timesheet, TimesheetEntry, Shift, EmployeeShiftRoster, OvertimeClaim
from datetime import datetime

class TimesheetService:
    @staticmethod
    def recalculate_timesheet_totals(timesheet_id):
        timesheet = Timesheet.query.get_or_404(timesheet_id)
        total_hours = sum(entry.hours_logged for entry in timesheet.entries)
        billable_hours = sum(entry.hours_logged for entry in timesheet.entries if entry.is_billable)

        timesheet.total_hours = round(total_hours, 2)
        timesheet.billable_hours = round(billable_hours, 2)
        db.session.commit()
        return timesheet
