from app import db
from app.models.learning import Course, CourseEnrollment, Quiz, QuizAttempt, Certificate
from datetime import datetime, date
import uuid

class LearningService:
    @staticmethod
    def grade_quiz_attempt(enrollment_id, quiz_id, submitted_answers):
        """
        submitted_answers: dict of {question_id: selected_option}
        """
        enrollment = CourseEnrollment.query.get_or_404(enrollment_id)
        quiz = Quiz.query.get_or_404(quiz_id)

        total_marks = 0
        earned_marks = 0

        for q in quiz.questions:
            total_marks += q.marks
            user_ans = str(submitted_answers.get(str(q.id)) or submitted_answers.get(q.id) or '').upper()
            if user_ans == str(q.correct_option).upper():
                earned_marks += q.marks

        score_pct = round((earned_marks / total_marks * 100.0), 1) if total_marks > 0 else 0.0
        passed = score_pct >= quiz.passing_score_pct

        if passed:
            enrollment.status = 'Completed'
            enrollment.progress_pct = 100.0
            enrollment.score_achieved = score_pct
            enrollment.completed_at = datetime.utcnow()

            # Generate Certificate
            cert_code = f"CERT-{uuid.uuid4().hex[:8].upper()}"
            certificate = Certificate(
                certificate_number=f"CN-{uuid.uuid4().hex[:10].upper()}",
                enrollment_id=enrollment.id,
                employee_id=enrollment.employee_id,
                course_name=enrollment.course.title if enrollment.course else "Enterprise Course",
                issued_date=datetime.utcnow().date(),
                verification_code=cert_code
            )
            db.session.add(certificate)

        db.session.commit()
        return {
            'passed': passed,
            'score_pct': score_pct,
            'earned_marks': earned_marks,
            'total_marks': total_marks,
            'passing_score_pct': quiz.passing_score_pct
        }
