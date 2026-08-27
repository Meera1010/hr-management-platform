from app import db
from app.models.workforce_analytics import AttritionRiskScore, SalaryBenchmark, WorkforcePlan
from app.models.employee import Employee
import random

class AnalyticsService:
    @staticmethod
    def evaluate_attrition_risk(employee_id):
        emp = Employee.query.get_or_404(employee_id)
        existing = AttritionRiskScore.query.filter_by(employee_id=employee_id).first()

        # Heuristic risk factors (for demo/analytical purposes)
        score = 15.0
        drivers = []

        if emp.joining_date:
            # Tenure in years
            from datetime import datetime
            tenure_years = (datetime.utcnow().date() - emp.joining_date).days / 365.25
            if tenure_years > 3.0:
                score += 15.0
                drivers.append("Stagnant tenure > 3 years")

        if emp.performance_reviews:
            last_review = emp.performance_reviews[-1]
            if last_review.overall_score and last_review.overall_score < 3.0:
                score += 30.0
                drivers.append("Low performance rating (< 3.0)")

        risk_level = "Low"
        if score >= 60.0:
            risk_level = "Critical"
        elif score >= 40.0:
            risk_level = "High"
        elif score >= 25.0:
            risk_level = "Medium"

        driver_str = "; ".join(drivers) if drivers else "Normal tenure and active engagement"
        retention = "Schedule 1-on-1 career mapping sync & salary benchmark review" if score >= 30.0 else "Maintain regular quarterly syncs"

        if not existing:
            risk_record = AttritionRiskScore(
                employee_id=employee_id,
                risk_level=risk_level,
                risk_score_pct=score,
                primary_drivers=driver_str,
                recommended_retention_action=retention
            )
            db.session.add(risk_record)
        else:
            existing.risk_level = risk_level
            existing.risk_score_pct = score
            existing.primary_drivers = driver_str
            existing.recommended_retention_action = retention
            risk_record = existing

        db.session.commit()
        return risk_record
