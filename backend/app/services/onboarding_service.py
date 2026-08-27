from app import db
from app.models.onboarding_exit import OnboardingChecklist, OnboardingTask, ResignationRequest, ExitClearance, FnFSettlement
from datetime import datetime, timedelta

class OnboardingService:
    @staticmethod
    def generate_default_onboarding_plan(employee_id, hr_coordinator_id=None, buddy_employee_id=None):
        checklist = OnboardingChecklist(
            employee_id=employee_id,
            title="Standard Employee Onboarding Checklist",
            target_completion_date=datetime.utcnow().date() + timedelta(days=14),
            overall_status='In Progress',
            hr_coordinator_id=hr_coordinator_id,
            buddy_employee_id=buddy_employee_id
        )
        db.session.add(checklist)
        db.session.flush()

        default_tasks = [
            ("Submit Identity Proof & Tax Documents", "Documentation", "Employee", 2),
            ("IT Asset Handover & Email Setup", "IT Setup", "IT Admin", 1),
            ("HR Benefits & Policy Orientation", "HR Orientation", "HR", 3),
            ("Team Introductions & Buddy Coffee Chat", "Manager Sync", "Employee", 2),
            ("Complete Mandatory Data Privacy & Security Course", "Training", "Employee", 7),
            ("First Week Manager 1-on-1 Goal Setting", "Manager Sync", "Employee", 5)
        ]

        for name, category, role, days in default_tasks:
            task = OnboardingTask(
                checklist_id=checklist.id,
                task_name=name,
                category=category,
                assigned_role=role,
                due_date=datetime.utcnow().date() + timedelta(days=days)
            )
            db.session.add(task)

        db.session.commit()
        return checklist

    @staticmethod
    def initiate_resignation(employee_id, reason, last_working_day, notice_days=60):
        resignation = ResignationRequest(
            employee_id=employee_id,
            submission_date=datetime.utcnow().date(),
            reason=reason,
            notice_period_days=notice_days,
            requested_last_working_day=last_working_day,
            status='Submitted'
        )
        db.session.add(resignation)
        db.session.flush()

        # Create clearance items for standard departments
        depts = ["IT", "HR", "Finance", "Admin", "Reporting Manager"]
        for dept in depts:
            clearance = ExitClearance(
                resignation_request_id=resignation.id,
                department_name=dept,
                status='Pending'
            )
            db.session.add(clearance)

        db.session.commit()
        return resignation
