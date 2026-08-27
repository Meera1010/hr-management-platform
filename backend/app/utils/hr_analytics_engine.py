"""
HR Core Metrics & Analytical KPI Calculations Engine.
Computes Time-to-Hire, Cost-per-Hire, Offer Acceptance Rate, Training Completion Percentage,
Absenteeism Rate, and Employee Net Promoter Score (eNPS) aggregates.
"""

from typing import Dict, Any, List

def calculate_time_to_hire(applications: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculates average days elapsed between job application submission and offer acceptance."""
    hired = [a for a in applications if a.get('status') == 'Hired' and a.get('days_to_hire')]
    if not hired:
        return {'avg_days_to_hire': 0.0, 'total_hired': 0}

    total_days = sum(a.get('days_to_hire', 0) for a in hired)
    avg_days = round(total_days / float(len(hired)), 1)

    return {
        'avg_days_to_hire': avg_days,
        'total_hired': len(hired)
    }

def calculate_offer_acceptance_rate(offers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Computes offer letter acceptance rate percentage."""
    total = len(offers)
    if total == 0:
        return {'acceptance_rate_pct': 0.0, 'total_offers': 0, 'accepted': 0, 'declined': 0}

    accepted = sum(1 for o in offers if o.get('status') == 'Accepted')
    declined = sum(1 for o in offers if o.get('status') == 'Declined')
    pending = sum(1 for o in offers if o.get('status') in ['Issued', 'Sent'])

    rate = round((accepted / float(total) * 100.0), 1)

    return {
        'total_offers': total,
        'accepted': accepted,
        'declined': declined,
        'pending': pending,
        'acceptance_rate_pct': rate
    }

def calculate_absenteeism_rate(total_expected_workdays: int, total_absent_days: float) -> float:
    """Calculates employee absenteeism rate percentage."""
    if total_expected_workdays <= 0:
        return 0.0
    rate = (total_absent_days / float(total_expected_workdays)) * 100.0
    return round(rate, 2)

def calculate_enps_score(promoters_count: int, passives_count: int, detractors_count: int) -> Dict[str, Any]:
    """Calculates Employee Net Promoter Score (eNPS) = % Promoters - % Detractors."""
    total_responses = promoters_count + passives_count + detractors_count
    if total_responses == 0:
        return {'enps_score': 0.0, 'total_responses': 0}

    promoter_pct = (promoters_count / float(total_responses)) * 100.0
    detractor_pct = (detractors_count / float(total_responses)) * 100.0
    enps = round(promoter_pct - detractor_pct, 1)

    return {
        'enps_score': enps,
        'promoters_count': promoters_count,
        'passives_count': passives_count,
        'detractors_count': detractors_count,
        'total_responses': total_responses
    }
