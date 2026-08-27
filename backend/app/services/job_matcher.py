import re
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.resume import Resume
from app.models.application import Application

def extract_candidate_skills(candidate_id: int) -> list:
    """
    Extracts all normalized candidate skills from Candidate model profile 
    and all parsed candidate resumes.
    """
    skills_set = set()
    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        return []

    # Profile skills
    if candidate.skills:
        # Candidate skills are typically comma-separated string
        parts = [s.strip().lower() for s in re.split(r'[,;\n]', candidate.skills) if s.strip()]
        skills_set.update(parts)

    # Resume skills
    resumes = Resume.query.filter_by(candidate_id=candidate_id).all()
    for resume in resumes:
        r_skills = resume.get_skills_list()
        for s in r_skills:
            if s and isinstance(s, str):
                skills_set.add(s.strip().lower())

    return sorted(list(skills_set))


def extract_job_skills(job: Job) -> list:
    """
    Extracts and normalizes required skills from Job model into a lowercase list.
    """
    if not job or not job.required_skills:
        return []

    raw_skills = job.required_skills
    if isinstance(raw_skills, list):
        parts = [s.strip().lower() for s in raw_skills if s and str(s).strip()]
    else:
        parts = [s.strip().lower() for s in re.split(r'[,;\n]', str(raw_skills)) if s.strip()]

    # Normalize: lowercase, strip, deduplicate preserving order
    seen = set()
    normalized = []
    for s in parts:
        if s not in seen:
            seen.add(s)
            normalized.append(s)

    return normalized


def calculate_skill_match(candidate_skills: list, job_skills: list) -> dict:
    """
    Calculates match percentage between candidate skills and job required skills.
    Formula: match_percentage = (matched_required_skills / total_required_skills) * 100
    If total_required_skills == 0, returns match_percentage = 0.
    """
    c_skills_lower = set([s.strip().lower() for s in candidate_skills if s])
    j_skills_lower = [s.strip().lower() for s in job_skills if s]

    if not j_skills_lower:
        return {
            "match_percentage": 0,
            "matched_skills": [],
            "missing_skills": []
        }

    matched = []
    missing = []

    for req_skill in j_skills_lower:
        if req_skill in c_skills_lower:
            matched.append(req_skill)
        else:
            missing.append(req_skill)

    total_required = len(j_skills_lower)
    matched_count = len(matched)

    match_percentage = int(round((matched_count / total_required) * 100))

    return {
        "match_percentage": match_percentage,
        "matched_skills": matched,
        "missing_skills": missing
    }


def get_candidate_job_matches(candidate_id: int) -> list:
    """
    Calculates job matches for a specific candidate across all open jobs.
    Returns list sorted descending by match_percentage.
    """
    c_skills = extract_candidate_skills(candidate_id)
    open_jobs = Job.query.filter(Job.status != 'Archived').all()

    matches = []
    for job in open_jobs:
        j_skills = extract_job_skills(job)
        calc = calculate_skill_match(c_skills, j_skills)

        matches.append({
            "job_id": job.id,
            "job_code": job.job_code,
            "job_title": job.title,
            "department": job.department.name if job.department else "N/A",
            "location": job.location or "N/A",
            "required_skills": job.required_skills,
            "match_percentage": calc["match_percentage"],
            "matched_skills": calc["matched_skills"],
            "missing_skills": calc["missing_skills"]
        })

    matches.sort(key=lambda x: x["match_percentage"], reverse=True)
    return matches


def rank_candidates_for_job(job_id: int) -> list:
    """
    Ranks candidates for a given job ID based on skill match.
    Returns candidate list sorted descending by match_percentage.
    """
    job = Job.query.get(job_id)
    if not job:
        return []

    j_skills = extract_job_skills(job)
    candidates = Candidate.query.all()

    # Get application status mapping for this job if candidate applied
    applications = Application.query.filter_by(job_id=job_id).all()
    app_status_map = {app.candidate_id: app.status for app in applications}

    rankings = []
    for candidate in candidates:
        c_skills = extract_candidate_skills(candidate.id)
        calc = calculate_skill_match(c_skills, j_skills)

        rankings.append({
            "candidate_id": candidate.id,
            "candidate_code": candidate.candidate_code,
            "candidate_name": f"{candidate.first_name} {candidate.last_name}",
            "email": candidate.email,
            "experience_years": candidate.experience_years,
            "education": candidate.education or "N/A",
            "current_role": candidate.current_role or "N/A",
            "match_percentage": calc["match_percentage"],
            "matched_skills": calc["matched_skills"],
            "missing_skills": calc["missing_skills"],
            "application_status": app_status_map.get(candidate.id, "Not Applied")
        })

    rankings.sort(key=lambda x: x["match_percentage"], reverse=True)
    return rankings
