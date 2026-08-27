import re

class CareerRecommender:
    """
    Transparent, decision-support career recommendation engine.
    Matches Candidate/Employee skills, education, and experience against open Job requirements.
    
    DATA PRIVACY COMPLIANCE:
    Candidate/Employee scoring strictly uses ONLY professional qualifications:
    - Skill overlap & technical alignment
    - Relevant experience years
    - Education match
    
    DOES NOT USE OR EVALUATE: Gender, Religion, Caste, Race, Disability, Medical info,
    Political affiliation, Marital status, Age, or Financial background.
    """

    @staticmethod
    def extract_keywords(text):
        if not text:
            return set()
        # Clean text and extract alphanumeric skill keywords
        cleaned = re.sub(r'[^a-zA-Z0-9\+\#\s]', ' ', text.lower())
        tokens = [t.strip() for t in cleaned.split() if len(t.strip()) > 1]
        return set(tokens)

    @classmethod
    def calculate_job_match(cls, user_skills_str, user_exp_years, user_education_str, job):
        """
        Calculate match metrics between a candidate/employee and a target Job.
        Returns match_score (0-100), matched_skills, missing_skills, recommendation_reason.
        """
        job_text = f"{job.title} {job.description or ''} {job.department.name if job.department else ''}"
        job_keywords = cls.extract_keywords(job_text)
        
        user_skills = cls.extract_keywords(user_skills_str or '')
        
        if not job_keywords:
            return {
                'match_score': 50.0,
                'matched_skills': list(user_skills)[:5],
                'missing_skills': [],
                'growth_tier': 'Moderate Match',
                'reasoning': 'General match based on open job position.'
            }

        # Matched skills
        matched = user_skills.intersection(job_keywords)
        missing = job_keywords.difference(user_skills)

        # Base skill overlap ratio
        skill_score = (len(matched) / max(len(job_keywords), 1)) * 70.0
        
        # Experience bonus (up to 20 points)
        exp_score = min((user_exp_years or 0) * 4.0, 20.0)

        # Education bonus (up to 10 points)
        edu_keywords = cls.extract_keywords(user_education_str or '')
        edu_score = 10.0 if len(edu_keywords.intersection(job_keywords)) > 0 else 5.0

        total_score = min(round(skill_score + exp_score + edu_score, 1), 99.0)

        if total_score >= 75.0:
            growth_tier = 'High Match'
            reasoning = f'Strong skill alignment ({len(matched)} matching skill areas) and solid background.'
        elif total_score >= 50.0:
            growth_tier = 'Moderate Match'
            reasoning = f'Good foundation with {len(matched)} matching skills. Potential for rapid onboarding.'
        else:
            growth_tier = 'Potential Growth Match'
            reasoning = f'Partial skill alignment. Up-skilling in missing areas recommended.'

        return {
            'match_score': total_score,
            'matched_skills': [s.capitalize() for s in sorted(list(matched))[:8]],
            'missing_skills': [s.capitalize() for s in sorted(list(missing))[:8]],
            'growth_tier': growth_tier,
            'reasoning': reasoning
        }
