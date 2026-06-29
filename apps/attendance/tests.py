from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from apps.corecode.models import StudentClass
from apps.notifications.models import Notification
from apps.staffs.models import Staff
from apps.students.models import Student

from .models import StaffAttendance, StaffLeaveRequest, StudentAttendance


def make_student(klass, registration_number="REG/ATT/0001"):
    return Student.objects.create(
        firstname="Jane", surname="Doe", current_class=klass,
        registration_number=registration_number,
    )


class StudentAttendanceModelTests(TestCase):
    def setUp(self):
        self.klass = StudentClass.objects.create(name="Class 1")
        self.student = make_student(self.klass)

    def test_default_status_is_absent(self):
        attendance = StudentAttendance.objects.create(student=self.student, date=date.today())
        self.assertEqual(attendance.status, 0)

    def test_str_includes_registration_and_date(self):
        attendance = StudentAttendance.objects.create(
            student=self.student, date=date(2026, 6, 1), status=1
        )
        text = str(attendance)
        self.assertIn(self.student.registration_number, text)
        self.assertIn("2026-06-01", text)

    def test_marking_present_then_absent_for_same_day_creates_two_records(self):
        """The model has no unique constraint on (student, date) - duplicate
        attendance records for the same day are possible at the model layer
        and must be prevented at the API/business-logic level instead."""
        StudentAttendance.objects.create(student=self.student, date=date.today(), status=1)
        StudentAttendance.objects.create(student=self.student, date=date.today(), status=0)
        self.assertEqual(
            StudentAttendance.objects.filter(student=self.student, date=date.today()).count(), 2
        )


class StaffAttendanceModelTests(TestCase):
    def setUp(self):
        self.staff = Staff.objects.create(firstname="John", surname="Smith")

    def test_default_status_is_absent(self):
        attendance = StaffAttendance.objects.create(staff=self.staff, date=date.today())
        self.assertEqual(attendance.status, 0)

    def test_default_date_is_today(self):
        attendance = StaffAttendance.objects.create(staff=self.staff)
        self.assertEqual(attendance.date, date.today())


class StaffLeaveRequestModelTests(TestCase):
    def setUp(self):
        self.staff = Staff.objects.create(firstname="John", surname="Smith")
        self.user = User.objects.create_user("leave_user", password="x", is_superuser=True)

    def test_default_status_is_pending(self):
        leave = StaffLeaveRequest.objects.create(
            staff_user=self.user, staff=self.staff,
            start_date=date.today(), end_date=date.today() + timedelta(days=2),
            reason="Medical",
        )
        self.assertEqual(leave.status, 0)

    def test_submitting_leave_request_notifies_superusers(self):
        """
        apps/attendance/signals.py's post_save receiver used to call
        Notification.objects.create(user=..., link=...), but Notification has
        neither field (only `recipients` M2M, no link field) - this crashed
        every leave request submission. It now goes through notify(), which
        creates the Notification correctly and adds the recipient via M2M.
        """
        StaffLeaveRequest.objects.create(
            staff_user=self.user, staff=self.staff,
            start_date=date.today(), end_date=date.today() + timedelta(days=2),
            reason="Medical",
        )
        notification = Notification.objects.filter(
            title="New Leave Request Submitted", recipients=self.user
        ).first()
        self.assertIsNotNone(notification)
        self.assertIn(self.user, notification.recipients.all())


class StudentAttendanceAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.klass_a = StudentClass.objects.create(name="Class A")
        self.klass_b = StudentClass.objects.create(name="Class B")
        self.student_a = make_student(self.klass_a, "REG/ATT/A/0001")
        self.student_b = make_student(self.klass_b, "REG/ATT/B/0001")

        self.admin = User.objects.create_user("att_admin", password="x", is_staff=True)
        self.non_staff = User.objects.create_user("att_plain", password="x")

    def test_unauthenticated_request_rejected(self):
        response = self.client.get("/api/v1/student/attendance/")
        self.assertEqual(response.status_code, 401)

    def test_non_staff_forbidden(self):
        self.client.force_authenticate(self.non_staff)
        response = self.client.get("/api/v1/student/attendance/")
        self.assertEqual(response.status_code, 403)

    def test_staff_can_mark_attendance(self):
        self.client.force_authenticate(self.admin)
        payload = {"student": self.student_a.id, "date": str(date.today()), "status": 1}
        response = self.client.post("/api/v1/student/attendance/", payload, format="json")
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(StudentAttendance.objects.count(), 1)

    def test_filter_by_class_only_returns_that_classes_students(self):
        StudentAttendance.objects.create(student=self.student_a, date=date.today(), status=1)
        StudentAttendance.objects.create(student=self.student_b, date=date.today(), status=1)

        self.client.force_authenticate(self.admin)
        response = self.client.get(f"/api/v1/student/attendance/?class={self.klass_a.id}")
        self.assertEqual(response.status_code, 200)
        results = response.data["results"] if "results" in response.data else response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["student"], self.student_a.id)


class StaffAttendanceAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.staff_user = User.objects.create_user("staff_clockin", password="x")
        self.staff = Staff.objects.create(
            firstname="John", surname="Smith", user=self.staff_user
        )
        self.admin = User.objects.create_user("att_staff_admin", password="x", is_staff=True)
        self.non_staff = User.objects.create_user("att_staff_plain", password="x")

    def test_non_staff_forbidden_from_listing(self):
        self.client.force_authenticate(self.non_staff)
        response = self.client.get("/api/v1/staff/attendance/")
        self.assertEqual(response.status_code, 403)

    def test_admin_can_list_staff_attendance(self):
        StaffAttendance.objects.create(staff=self.staff, date=date.today(), status=1)
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/v1/staff/attendance/")
        self.assertEqual(response.status_code, 200)

    def test_record_time_creates_time_in_on_first_call(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.post("/api/v1/staff/attendance/record-time/")
        self.assertEqual(response.status_code, 200, response.data)
        attendance = StaffAttendance.objects.get(staff=self.staff, date=date.today())
        self.assertIsNotNone(attendance.time_in)
        self.assertIsNone(attendance.time_out)
        self.assertEqual(attendance.status, 1)

    def test_record_time_sets_time_out_on_second_call(self):
        self.client.force_authenticate(self.staff_user)
        self.client.post("/api/v1/staff/attendance/record-time/")
        response = self.client.post("/api/v1/staff/attendance/record-time/")
        self.assertEqual(response.status_code, 200, response.data)
        attendance = StaffAttendance.objects.get(staff=self.staff, date=date.today())
        self.assertIsNotNone(attendance.time_out)
