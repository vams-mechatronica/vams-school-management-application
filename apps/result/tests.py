from datetime import timedelta

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from apps.corecode.models import AcademicSession, AcademicTerm, StudentClass, Subject
from apps.students.models import Student

from .models import Result


def make_session_and_term():
    session = AcademicSession.objects.create(
        name="2025/2026",
        current=True,
        start_date=timezone.now().date(),
        end_date=timezone.now().date() + timedelta(days=365),
    )
    term = AcademicTerm.objects.create(
        name="Result Test Term",
        current=True,
        start_date=timezone.now().date(),
        end_date=timezone.now().date() + timedelta(days=90),
    )
    return session, term


class ResultModelTests(TestCase):
    """Marks/grading logic on the Result model."""

    def setUp(self):
        self.session, self.term = make_session_and_term()
        self.klass = StudentClass.objects.create(name="Class 1")
        self.subject = Subject.objects.create(
            name="Result Test Mathematics", test_max_marks=50, exam_max_marks=100
        )
        self.student = Student.objects.create(
            firstname="Jane", surname="Doe", current_class=self.klass,
            registration_number="REG/RESULT/0001",
        )

    def make_result(self, test_score, exam_score):
        return Result.objects.create(
            student=self.student, session=self.session, term=self.term,
            current_class=self.klass, subject=self.subject,
            test_score=test_score, exam_score=exam_score,
        )

    def test_total_score_sums_test_and_exam(self):
        result = self.make_result(test_score=40, exam_score=80)
        self.assertEqual(result.total_score(), 120)

    def test_calc_grade_a_plus_for_perfect_score(self):
        result = self.make_result(test_score=50, exam_score=100)
        self.assertEqual(result.calc_grade(), "A+")

    def test_calc_grade_a_for_90_to_99_percent(self):
        result = self.make_result(test_score=45, exam_score=90)  # 135/150 = 90%
        self.assertEqual(result.calc_grade(), "A")

    def test_calc_grade_b_plus_for_80_to_89_percent(self):
        result = self.make_result(test_score=40, exam_score=80)  # 120/150 = 80%
        self.assertEqual(result.calc_grade(), "B+")

    def test_calc_grade_c_for_50_to_59_percent(self):
        result = self.make_result(test_score=25, exam_score=50)  # 75/150 = 50%
        self.assertEqual(result.calc_grade(), "C")

    def test_calc_grade_d_for_33_to_39_percent(self):
        result = self.make_result(test_score=10, exam_score=40)  # 50/150 = 33.3%
        self.assertEqual(result.calc_grade(), "D")

    def test_calc_grade_f_below_33_percent(self):
        result = self.make_result(test_score=0, exam_score=10)  # 10/150 = 6.7%
        self.assertEqual(result.calc_grade(), "F")

    def test_grade_matches_calc_grade(self):
        """
        Result.grade() used to delegate to the now-removed apps/result/utils.
        score_grade, which only special-cased scores <= 10 and returned None
        for every realistic score. grade() now delegates to calc_grade() (the
        correct, percentage-based implementation) so it returns a real letter
        grade for normal scores.
        """
        result = self.make_result(test_score=45, exam_score=90)  # 135/150 = 90%
        self.assertEqual(result.grade(), "A")
        self.assertEqual(result.grade(), result.calc_grade())


class StudentResultAPITests(TestCase):
    """API-level checks for the results/marks endpoint."""

    def setUp(self):
        self.client = APIClient()
        self.session, self.term = make_session_and_term()
        self.klass = StudentClass.objects.create(name="Class 1")
        self.maths = Subject.objects.create(name="API Test Mathematics", test_max_marks=50, exam_max_marks=100)
        self.english = Subject.objects.create(name="API Test English", test_max_marks=50, exam_max_marks=100)

        student_group, _ = Group.objects.get_or_create(name="Student")
        self.student_user = User.objects.create_user("result_student", password="x")
        self.student_user.groups.add(student_group)
        self.student = Student.objects.create(
            firstname="Jane", surname="Doe", current_class=self.klass,
            registration_number="REG/RESULT/API/0001", user=self.student_user,
        )

        Result.objects.create(
            student=self.student, session=self.session, term=self.term,
            current_class=self.klass, subject=self.maths,
            test_score=45, exam_score=90,  # 135/150
        )
        Result.objects.create(
            student=self.student, session=self.session, term=self.term,
            current_class=self.klass, subject=self.english,
            test_score=25, exam_score=50,  # 75/150
        )

        admin_group, _ = Group.objects.get_or_create(name="admin")
        self.admin = User.objects.create_user("result_admin", password="x", is_staff=True)
        self.admin.groups.add(admin_group)

    def test_unauthenticated_request_rejected(self):
        response = self.client.get("/api/v1/results/")
        self.assertEqual(response.status_code, 401)

    def test_admin_can_fetch_results_for_specific_student(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get(f"/api/v1/results/?student_id={self.student.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

        student_result = response.data["results"][0]
        self.assertEqual(student_result["overall"]["total_score"], 210)
        self.assertEqual(student_result["overall"]["max_score"], 300)
        self.assertEqual(student_result["overall"]["grade"], "B")
        self.assertEqual(student_result["overall"]["remarks"], "Pass")

    def test_student_sees_only_their_own_results(self):
        self.client.force_authenticate(self.student_user)
        response = self.client.get("/api/v1/results/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["student_id"], self.student.id)

    def test_subject_search_filters_results(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get(
            f"/api/v1/results/?student_id={self.student.id}&search=API Test English"
        )
        self.assertEqual(response.status_code, 200)
        subjects = response.data["results"][0]["academic_results"][0]["terms"][0]["subjects"]
        self.assertEqual(len(subjects), 1)
        self.assertEqual(subjects[0]["subject"], "API Test English")
