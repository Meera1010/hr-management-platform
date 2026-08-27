from datetime import datetime
from app import db

class WorkforcePlan(db.Model):
    __tablename__ = 'workforce_plans'

    id = db.Column(db.Integer, primary_key=True)
    plan_year = db.Column(db.Integer, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    current_headcount = db.Column(db.Integer, default=0)
    target_headcount = db.Column(db.Integer, default=0)
    approved_budget = db.Column(db.Float, default=0.0)
    hiring_target_q1 = db.Column(db.Integer, default=0)
    hiring_target_q2 = db.Column(db.Integer, default=0)
    hiring_target_q3 = db.Column(db.Integer, default=0)
    hiring_target_q4 = db.Column(db.Integer, default=0)
    status = db.Column(db.String(30), default='Draft')  # Draft, Approved, Closed
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    department = db.relationship('Department', backref='workforce_plans', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'plan_year': self.plan_year,
            'department_id': self.department_id,
            'department_name': self.department.name if self.department else None,
            'current_headcount': self.current_headcount,
            'target_headcount': self.target_headcount,
            'net_addition_needed': self.target_headcount - self.current_headcount,
            'approved_budget': self.approved_budget,
            'hiring_target_q1': self.hiring_target_q1,
            'hiring_target_q2': self.hiring_target_q2,
            'hiring_target_q3': self.hiring_target_q3,
            'hiring_target_q4': self.hiring_target_q4,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class AttritionRiskScore(db.Model):
    __tablename__ = 'attrition_risk_scores'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    risk_level = db.Column(db.String(20), default='Low')  # Low, Medium, High, Critical
    risk_score_pct = db.Column(db.Float, default=15.0)    # 0 to 100%
    primary_drivers = db.Column(db.Text, nullable=True)   # e.g., "Low salary growth, high tenure without promotion, recent low rating"
    last_evaluated_at = db.Column(db.DateTime, default=datetime.utcnow)
    recommended_retention_action = db.Column(db.Text, nullable=True)

    employee = db.relationship('Employee', backref='attrition_risk', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': f"{self.employee.first_name} {self.employee.last_name}" if self.employee else None,
            'department': self.employee.department.name if self.employee and self.employee.department else None,
            'designation': self.employee.designation if self.employee else None,
            'risk_level': self.risk_level,
            'risk_score_pct': self.risk_score_pct,
            'primary_drivers': self.primary_drivers,
            'last_evaluated_at': self.last_evaluated_at.isoformat() if self.last_evaluated_at else None,
            'recommended_retention_action': self.recommended_retention_action
        }


class SalaryBenchmark(db.Model):
    __tablename__ = 'salary_benchmarks'

    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100), nullable=False)
    experience_level = db.Column(db.String(30), default='Mid')  # Junior, Mid, Senior, Lead, Executive
    industry_min_ctc = db.Column(db.Float, default=0.0)
    industry_median_ctc = db.Column(db.Float, default=0.0)
    industry_max_ctc = db.Column(db.Float, default=0.0)
    company_avg_ctc = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(10), default='INR')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        diff_pct = round(((self.company_avg_ctc - self.industry_median_ctc) / self.industry_median_ctc * 100), 1) if self.industry_median_ctc > 0 else 0.0
        return {
            'id': self.id,
            'job_title': self.job_title,
            'experience_level': self.experience_level,
            'industry_min_ctc': self.industry_min_ctc,
            'industry_median_ctc': self.industry_median_ctc,
            'industry_max_ctc': self.industry_max_ctc,
            'company_avg_ctc': self.company_avg_ctc,
            'currency': self.currency,
            'competitive_index_pct': diff_pct,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
