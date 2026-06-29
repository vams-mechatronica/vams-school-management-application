from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from apps.corecode.models import StudentClass
from .models import Student


def make_student(klass, registration_number="REG/CARD/0001"):
    return Student.objects.create(
        firstname="Jane", surname="Doe", current_class=klass,
        registration_number=registration_number,
    )


class StudentImageFormTests(TestCase):
    def test_student_form_includes_student_image_field(self):
        from .forms import StudentForm
        self.assertIn("student_image", StudentForm.Meta.fields)


class CardViewPermissionTests(TestCase):
    """Card-printing pages require the students.view_student permission,
    same as the existing student detail/list pages."""

    def setUp(self):
        self.klass = StudentClass.objects.create(name="Card Test Class")
        self.student = make_student(self.klass)

        self.viewer = User.objects.create_user("card_viewer", password="x")
        self.viewer.user_permissions.add(
            Permission.objects.get(codename="view_student")
        )
        self.no_perm_user = User.objects.create_user("card_no_perm", password="x")

    def test_id_card_requires_login(self):
        url = reverse("student-id-card", args=[self.student.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_id_card_denies_user_without_permission(self):
        self.client.force_login(self.no_perm_user)
        url = reverse("student-id-card", args=[self.student.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_id_card_renders_for_user_with_permission(self):
        self.client.force_login(self.viewer)
        url = reverse("student-id-card", args=[self.student.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["students"]), [self.student])

    def test_id_card_bulk_renders_all_students_in_class(self):
        other = make_student(self.klass, registration_number="REG/CARD/0002")
        self.client.force_login(self.viewer)
        url = reverse("student-id-card-bulk", args=[self.klass.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context["students"], [self.student, other])

    def test_admit_card_renders_for_user_with_permission(self):
        self.client.force_login(self.viewer)
        url = reverse("student-admit-card", args=[self.student.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["students"]), [self.student])

    def test_admit_card_bulk_renders_all_students_in_class(self):
        other = make_student(self.klass, registration_number="REG/CARD/0003")
        self.client.force_login(self.viewer)
        url = reverse("student-admit-card-bulk", args=[self.klass.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context["students"], [self.student, other])

    def test_class_select_page_lists_classes(self):
        self.client.force_login(self.viewer)
        url = reverse("id-card-select-class")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.klass, response.context["classes"])
        self.assertEqual(response.context["card_type"], "id-card")
