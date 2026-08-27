from app import db
from app.models.okr_performance import Objective, KeyResult, Feedback360

class OkrService:
    @staticmethod
    def recalculate_objective_progress(objective_id):
        objective = Objective.query.get_or_404(objective_id)
        key_results = objective.key_results
        if not key_results:
            objective.progress_pct = 0.0
            db.session.commit()
            return 0.0

        total_weighted_progress = 0.0
        total_weight = 0.0

        for kr in key_results:
            kr_progress = min(100.0, (kr.current_value / kr.target_value * 100.0)) if kr.target_value > 0 else 0.0
            total_weighted_progress += kr_progress * kr.weight
            total_weight += kr.weight

        overall = round(total_weighted_progress / total_weight, 1) if total_weight > 0 else 0.0
        objective.progress_pct = overall

        if overall >= 100.0:
            objective.status = 'Completed'
        elif overall >= 75.0:
            objective.status = 'On Track'
        elif overall >= 40.0:
            objective.status = 'At Risk'
        else:
            objective.status = 'Behind'

        db.session.commit()
        return overall
