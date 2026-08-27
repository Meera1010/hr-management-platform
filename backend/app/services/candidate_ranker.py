import re
from app.models.candidate import Candidate
from app.models.job import Job
from app.models.application import Application
from app.services.job_matcher import extract_candidate_skills, extract_job_skills, calculate_skill_match

class CandidateRanker:
    @staticmethod
    def parse_required_experience_years(exp_string: str) -> int:
        """
        Extracts minimum required experience years from job experience_required string.
        e.g., '3-5 years' -> 3, '5+ years' -> 5, 'Freshers' -> 0.
        """
        if not exp_string:
            return 0
        numbers = re.findall(r'\d+', str(exp_string))
        if numbers:
            return int(numbers[0])
        return 0

    @staticmethod
    def calculate_experience_score(candidate_exp: int, required_exp: int) -> float:
        """
        Calculates experience score (0 - 100).
        """
        if required_exp <= 0:
            return 100.0
        if candidate_exp >= required_exp:
            return 100.0
        return round((candidate_exp / float(required_exp)) * 100.0, 2)

    @staticmethod
    def calculate_education_score(candidate_edu: str, required_edu: str) -> float:
        """
        Calculates education match score (0 - 100).
        """
        if not required_edu or not required_edu.strip():
            return 100.0
        if not candidate_edu or not candidate_edu.strip():
            return 50.0

        c_edu_lower = candidate_edu.lower()
        r_edu_lower = required_edu.lower()

        # Check exact or keyword match
        r_words = [w.strip() for w in re.split(r'[\s,/]+', r_edu_lower) if len(w.strip()) > 2]
        matched_words = [w for w in r_words if w in c_edu_lower]

        if r_edu_lower in c_edu_lower or len(matched_words) == len(r_words):
            return 100.0
        elif len(matched_words) > 0:
            return 75.0
        else:
            return 50.0

    @classmethod
    def rank_candidate_for_job(cls, candidate: Candidate, job: Job, application_status: str = "Not Applied") -> dict:
        """
        Computes transparent score for a candidate against a job based strictly on:
        - Skill match (60%)
        - Experience match (25%)
        - Education match (15%)
        """
        # 1. Skill Score
        c_skills = extract_candidate_skills(candidate.id)
        j_skills = extract_job_skills(job)
        skill_res = calculate_skill_match(c_skills, j_skills)
        skill_score = float(skill_res["match_percentage"])

        # 2. Experience Score
        req_exp = cls.parse_required_experience_years(job.experience_required)
        exp_score = cls.calculate_experience_score(candidate.experience_years, req_exp)

        # 3. Education Score
        edu_score = cls.calculate_education_score(candidate.education or "", job.education_required or "")

        # 4. Final Weighted Score
        final_score = round((skill_score * 0.60) + (exp_score * 0.25) + (edu_score * 0.15), 2)

        # 5. Explanation Generation
        explanations = []
        if skill_score >= 80:
            explanations.append("Strong skill alignment with required job competencies.")
        elif skill_score >= 50:
            explanations.append("Moderate skill alignment.")
        else:
            explanations.append("Low skill alignment with required competencies.")

        if exp_score >= 100:
            explanations.append("Meets or exceeds required years of experience.")
        else:
            explanations.append(f"Partial experience match ({candidate.experience_years} of {req_exp} years required).")

        if edu_score >= 100:
            explanations.append("Education matches job requirements.")
        elif edu_score >= 75:
            explanations.append("Education partially aligns with requirements.")

        explanation_text = " ".join(explanations)

        return {
            "candidate_id": candidate.id,
            "candidate_code": candidate.candidate_code,
            "candidate_name": f"{candidate.first_name} {candidate.last_name}",
            "email": candidate.email,
            "score": final_score,
            "skill_score": skill_score,
            "experience_score": exp_score,
            "education_score": edu_score,
            "experience_years": candidate.experience_years,
            "education": candidate.education or "N/A",
            "matched_skills": skill_res["matched_skills"],
            "missing_skills": skill_res["missing_skills"],
            "application_status": application_status,
            "explanation": explanation_text
        }

    @classmethod
    def rank_all_candidates_for_job(cls, job_id: int) -> list:
        """
        Ranks all candidates for a specified job ID descending by final score.
        """
        job = Job.query.get(job_id)
        if not job:
            return []

        candidates = Candidate.query.all()
        applications = Application.query.filter_by(job_id=job_id).all()
        app_status_map = {app.candidate_id: (app.status, app.id) for app in applications}

        rankings = []
        for c in candidates:
            app_status, app_id = app_status_map.get(c.id, ("Not Applied", None))
            rank_data = cls.rank_candidate_for_job(c, job, application_status=app_status)
            rank_data["application_id"] = app_id
            rankings.append(rank_data)

        rankings.sort(key=lambda x: x["score"], reverse=True)
        return rankings
