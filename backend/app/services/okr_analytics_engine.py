"""
OKR Alignment Tree & 360 Feedback Competency Matrix Analytics Engine.
Computes objective alignment across organizational levels and formats
360-degree review radar chart datasets.
"""

from typing import Dict, Any, List

class OkrAnalyticsEngine:

    @staticmethod
    def compute_department_okr_health(objectives: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregates OKR progress statistics per department."""
        total = len(objectives)
        if total == 0:
            return {'total_okrs': 0, 'avg_progress_pct': 0.0, 'completed': 0, 'on_track': 0, 'at_risk': 0, 'behind': 0}

        avg_progress = sum(o.get('progress_pct', 0.0) for o in objectives) / total
        completed = sum(1 for o in objectives if o.get('status') == 'Completed')
        on_track = sum(1 for o in objectives if o.get('status') == 'On Track')
        at_risk = sum(1 for o in objectives if o.get('status') == 'At Risk')
        behind = sum(1 for o in objectives if o.get('status') == 'Behind')

        return {
            'total_okrs': total,
            'avg_progress_pct': round(avg_progress, 1),
            'completed': completed,
            'on_track': on_track,
            'at_risk': at_risk,
            'behind': behind
        }

    @staticmethod
    def format_360_radar_matrix(feedbacks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculates average competency scores across Leadership, Technical, Communication, and Teamwork."""
        if not feedbacks:
            return {'leadership': 0.0, 'technical': 0.0, 'communication': 0.0, 'teamwork': 0.0, 'overall': 0.0}

        n = len(feedbacks)
        lead = sum(f.get('leadership_score', 0.0) for f in feedbacks) / n
        tech = sum(f.get('technical_score', 0.0) for f in feedbacks) / n
        comm = sum(f.get('communication_score', 0.0) for f in feedbacks) / n
        team = sum(f.get('teamwork_score', 0.0) for f in feedbacks) / n
        overall = sum(f.get('overall_rating', 0.0) for f in feedbacks) / n

        return {
            'leadership': round(lead, 2),
            'technical': round(tech, 2),
            'communication': round(comm, 2),
            'teamwork': round(team, 2),
            'overall': round(overall, 2),
            'total_evaluators': n
        }
