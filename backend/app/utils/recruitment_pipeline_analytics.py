"""
Recruitment ATS Pipeline Conversion & Sourcing Analytics Engine.
Calculates applicant conversion funnel rates, stage dropoff percentages,
and recruiter sourcing efficiency KPIs.
"""

from typing import Dict, Any, List

class RecruitmentPipelineAnalytics:

    @staticmethod
    def calculate_funnel_conversion(applications: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculates stage-by-stage ATS applicant conversion funnel metrics."""
        total_applied = len(applications)
        if total_applied == 0:
            return {'total_applied': 0, 'funnel_stages': []}

        shortlisted = sum(1 for a in applications if a.get('status') in ['Shortlisted', 'Screening', 'Interview Scheduled', 'Offered', 'Accepted', 'Hired'])
        interviewed = sum(1 for a in applications if a.get('status') in ['Interview Scheduled', 'Offered', 'Accepted', 'Hired'])
        offered = sum(1 for a in applications if a.get('status') in ['Offered', 'Accepted', 'Hired'])
        hired = sum(1 for a in applications if a.get('status') == 'Hired')

        return {
            'total_applied': total_applied,
            'shortlisted': shortlisted,
            'interviewed': interviewed,
            'offered': offered,
            'hired': hired,
            'shortlist_rate_pct': round((shortlisted / float(total_applied)) * 100.0, 1),
            'interview_rate_pct': round((interviewed / float(total_applied)) * 100.0, 1),
            'offer_conversion_rate_pct': round((offered / float(total_applied)) * 100.0, 1),
            'hire_conversion_rate_pct': round((hired / float(total_applied)) * 100.0, 1)
        }
