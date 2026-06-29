from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from apps.corecode.models import AcademicSession, AcademicTerm, FeeCategory, StudentClass
from apps.students.models import Student

from .models import Concession, Invoice, InvoiceItem, Receipt


def make_session_and_term():
    session = AcademicSession.objects.create(
        name="2025/2026",
        current=True,
        start_date=timezone.now().date(),
        end_date=timezone.now().date() + timedelta(days=365),
    )
    term = AcademicTerm.objects.create(
        name="Fee Test Term",
        current=True,
        start_date=timezone.now().date(),
        end_date=timezone.now().date() + timedelta(days=90),
    )
    return session, term


def make_student(klass, registration_number="REG/0001"):
    return Student.objects.create(
        firstname="Jane",
        surname="Doe",
        current_class=klass,
        registration_number=registration_number,
    )


class InvoiceModelTests(TestCase):
    """Business-logic tests for fee invoices: balance computation, payment
    tracking, and the auto-closing of older invoices for the same student."""

    def setUp(self):
        self.session, self.term = make_session_and_term()
        self.klass = StudentClass.objects.create(name="Class 1", tuition_fees=Decimal("500.00"))
        self.student = make_student(self.klass)

    def make_invoice(self, previous_balance=Decimal("0.00")):
        return Invoice.objects.create(
            student=self.student,
            session=self.session,
            term=self.term,
            class_for=self.klass,
            previous_balance=previous_balance,
        )

    def test_amount_payable_sums_invoice_items(self):
        invoice = self.make_invoice()
        InvoiceItem.objects.create(invoice=invoice, description="Tuition Fee", amount=Decimal("500.00"))
        InvoiceItem.objects.create(invoice=invoice, description="Library Fee", amount=Decimal("100.00"))
        self.assertEqual(invoice.amount_payable(), 600)

    def test_total_amount_payable_includes_previous_balance(self):
        invoice = self.make_invoice(previous_balance=Decimal("200.00"))
        InvoiceItem.objects.create(invoice=invoice, description="Tuition Fee", amount=Decimal("500.00"))
        self.assertEqual(invoice.total_amount_payable(), 700)

    def test_balance_is_zero_when_fully_paid(self):
        invoice = self.make_invoice()
        InvoiceItem.objects.create(invoice=invoice, description="Tuition Fee", amount=Decimal("500.00"))
        Receipt.objects.create(invoice=invoice, amount_paid=Decimal("500.00"), date_paid=timezone.now())
        self.assertEqual(invoice.balance(), 0)

    def test_balance_reflects_partial_payment(self):
        invoice = self.make_invoice()
        InvoiceItem.objects.create(invoice=invoice, description="Tuition Fee", amount=Decimal("500.00"))
        Receipt.objects.create(invoice=invoice, amount_paid=Decimal("300.00"), date_paid=timezone.now())
        self.assertEqual(invoice.balance(), 200)

    def test_save_sets_total_payable_to_current_balance(self):
        invoice = self.make_invoice(previous_balance=Decimal("100.00"))
        InvoiceItem.objects.create(invoice=invoice, description="Tuition Fee", amount=Decimal("500.00"))
        invoice.save()
        self.assertEqual(invoice.total_payable, invoice.balance())

    def test_new_invoice_marks_previous_invoice_for_student_non_editable(self):
        first = self.make_invoice()
        self.assertTrue(first.is_editable)
        self.make_invoice()
        first.refresh_from_db()
        self.assertFalse(first.is_editable)
        self.assertFalse(first.status)

    def test_disable_editing_after_payment_made(self):
        invoice = self.make_invoice()
        InvoiceItem.objects.create(invoice=invoice, description="Tuition Fee", amount=Decimal("500.00"))
        Receipt.objects.create(invoice=invoice, amount_paid=Decimal("100.00"), date_paid=timezone.now())
        invoice.disable_editing()
        self.assertFalse(invoice.is_editable)

    def test_disable_editing_noop_when_unpaid_and_recent(self):
        invoice = self.make_invoice()
        invoice.disable_editing()
        self.assertTrue(invoice.is_editable)

    def test_disable_editing_after_30_days_old(self):
        invoice = self.make_invoice()
        Invoice.objects.filter(pk=invoice.pk).update(
            created_at=timezone.now() - timedelta(days=31)
        )
        invoice.refresh_from_db()
        invoice.disable_editing()
        self.assertFalse(invoice.is_editable)


class InvoiceAPITests(TestCase):
    """Permission and creation-flow tests for the fees API. Fee line items
    (tuition/computer/admission/exam/misc) are auto-derived from the
    student's class when not supplied explicitly."""

    def setUp(self):
        self.client = APIClient()
        self.session, self.term = make_session_and_term()
        self.klass = StudentClass.objects.create(
            name="Class 1",
            tuition_fees=Decimal("500.00"),
            computer_fees=Decimal("50.00"),
            admission_fees=Decimal("0.00"),
            exam_fees=Decimal("25.00"),
            miscellaneous=Decimal("0.00"),
        )
        self.student = make_student(self.klass)

        self.admin = User.objects.create_user("admin_fee", password="x", is_staff=True)
        self.student_user = User.objects.create_user("student_fee", password="x")
        self.student.user = self.student_user
        self.student.save()

        self.other_student = make_student(self.klass, registration_number="REG/0002")
        self.other_user = User.objects.create_user("other_student_fee", password="x")
        self.other_student.user = self.other_user
        self.other_student.save()

    def test_staff_can_create_invoice_with_class_fees_autofilled(self):
        self.client.force_authenticate(self.admin)
        url = reverse("invoice-list-create")
        payload = {
            "student": self.student.id,
            "session": self.session.id,
            "term": self.term.id,
            "month": "January",
            "class_for": self.klass.id,
            "previous_balance": "0.00",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        invoice = Invoice.objects.get(student=self.student)
        self.assertEqual(invoice.amount_payable(), 575)

    def test_non_staff_cannot_create_invoice(self):
        """
        InvoiceListCreateView.perform_create() used to silently no-op for
        non-staff users instead of rejecting the request, which made DRF
        crash with AttributeError while building the response (it assumed a
        saved Invoice instance). It now raises PermissionDenied up front, so
        non-staff users get a clean 403 and no Invoice is created.
        """
        self.client.force_authenticate(self.student_user)
        url = reverse("invoice-list-create")
        payload = {
            "student": self.student.id,
            "session": self.session.id,
            "term": self.term.id,
            "month": "January",
            "class_for": self.klass.id,
            "previous_balance": "0.00",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Invoice.objects.count(), 0)

    def test_student_only_sees_own_invoices(self):
        own_invoice = Invoice.objects.create(
            student=self.student, session=self.session, term=self.term,
            class_for=self.klass, previous_balance=Decimal("0.00"),
        )
        Invoice.objects.create(
            student=self.other_student, session=self.session, term=self.term,
            class_for=self.klass, previous_balance=Decimal("0.00"),
        )

        self.client.force_authenticate(self.student_user)
        url = reverse("invoice-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"] if "results" in response.data else response.data
        returned_ids = [item["id"] for item in results]
        self.assertIn(own_invoice.id, returned_ids)
        self.assertEqual(len(returned_ids), 1)

    def test_staff_sees_all_invoices(self):
        Invoice.objects.create(
            student=self.student, session=self.session, term=self.term,
            class_for=self.klass, previous_balance=Decimal("0.00"),
        )
        Invoice.objects.create(
            student=self.other_student, session=self.session, term=self.term,
            class_for=self.klass, previous_balance=Decimal("0.00"),
        )

        self.client.force_authenticate(self.admin)
        url = reverse("invoice-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        count = response.data["count"] if "count" in response.data else len(response.data)
        self.assertEqual(count, 2)

    def test_unauthenticated_request_rejected(self):
        url = reverse("invoice-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RTEFeeEnforcementTests(TestCase):
    """RTE students must never be charged tuition, even if the class has a
    nonzero tuition fee or a tuition amount is explicitly supplied."""

    def setUp(self):
        self.client = APIClient()
        self.session, self.term = make_session_and_term()
        self.klass = StudentClass.objects.create(
            name="RTE Class 1", tuition_fees=Decimal("500.00"), computer_fees=Decimal("50.00"),
        )
        self.rte_category = FeeCategory.objects.create(name="RTE", is_rte=True)
        self.general_category = FeeCategory.objects.create(name="General", is_rte=False)
        self.admin = User.objects.create_user("rte_admin", password="x", is_staff=True)

    def create_invoice(self, student, extra=None):
        self.client.force_authenticate(self.admin)
        url = reverse("invoice-list-create")
        payload = {
            "student": student.id,
            "session": self.session.id,
            "term": self.term.id,
            "month": "January",
            "class_for": self.klass.id,
            "previous_balance": "0.00",
        }
        if extra:
            payload.update(extra)
        return self.client.post(url, payload, format="json")

    def test_rte_student_never_charged_tuition_even_when_class_has_fee(self):
        student = make_student(self.klass, registration_number="REG/RTE/0001")
        student.fee_category = self.rte_category
        student.save()

        response = self.create_invoice(student)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        invoice = Invoice.objects.get(student=student)
        tuition_item = invoice.invoice_items.get(description="Tuition Fees")
        self.assertEqual(tuition_item.amount, Decimal("0.00"))

    def test_rte_student_tuition_forced_to_zero_even_if_explicitly_supplied(self):
        student = make_student(self.klass, registration_number="REG/RTE/0002")
        student.fee_category = self.rte_category
        student.save()

        response = self.create_invoice(student, extra={"tuition_fees": "999.00"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        invoice = Invoice.objects.get(student=student)
        tuition_item = invoice.invoice_items.get(description="Tuition Fees")
        self.assertEqual(tuition_item.amount, Decimal("0.00"))

    def test_non_rte_student_still_charged_normal_tuition(self):
        student = make_student(self.klass, registration_number="REG/RTE/0003")
        student.fee_category = self.general_category
        student.save()

        response = self.create_invoice(student)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        invoice = Invoice.objects.get(student=student)
        tuition_item = invoice.invoice_items.get(description="Tuition Fees")
        self.assertEqual(tuition_item.amount, Decimal("500.00"))


class ConcessionDiscountTests(TestCase):
    """Active, verified concessions reduce the invoice total; unverified or
    expired concessions must not."""

    def setUp(self):
        self.client = APIClient()
        self.session, self.term = make_session_and_term()
        self.klass = StudentClass.objects.create(
            name="Concession Class 1", tuition_fees=Decimal("1000.00"),
        )
        self.student = make_student(self.klass, registration_number="REG/CONC/0001")
        self.admin = User.objects.create_user("concession_admin", password="x", is_staff=True)

    def create_invoice(self):
        self.client.force_authenticate(self.admin)
        url = reverse("invoice-list-create")
        payload = {
            "student": self.student.id,
            "session": self.session.id,
            "term": self.term.id,
            "month": "January",
            "class_for": self.klass.id,
            "previous_balance": "0.00",
        }
        return self.client.post(url, payload, format="json")

    def test_active_verified_percentage_concession_reduces_total_payable(self):
        Concession.objects.create(
            student=self.student, concession_type="merit", percentage=Decimal("10.00"),
            valid_from=timezone.now().date() - timedelta(days=1),
            valid_to=timezone.now().date() + timedelta(days=30),
            verified=True,
        )
        response = self.create_invoice()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        invoice = Invoice.objects.get(student=self.student)
        # tuition 1000 - 10% = 900
        self.assertEqual(invoice.previous_balance, Decimal("900.00"))

    def test_active_verified_fixed_concession_reduces_total_payable(self):
        Concession.objects.create(
            student=self.student, concession_type="sibling", fixed_amount=Decimal("200.00"),
            valid_from=timezone.now().date() - timedelta(days=1),
            valid_to=timezone.now().date() + timedelta(days=30),
            verified=True,
        )
        response = self.create_invoice()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        invoice = Invoice.objects.get(student=self.student)
        self.assertEqual(invoice.previous_balance, Decimal("800.00"))

    def test_unverified_concession_not_applied(self):
        Concession.objects.create(
            student=self.student, concession_type="merit", percentage=Decimal("10.00"),
            valid_from=timezone.now().date() - timedelta(days=1),
            valid_to=timezone.now().date() + timedelta(days=30),
            verified=False,
        )
        response = self.create_invoice()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        invoice = Invoice.objects.get(student=self.student)
        self.assertEqual(invoice.previous_balance, Decimal("1000.00"))

    def test_expired_concession_not_applied(self):
        Concession.objects.create(
            student=self.student, concession_type="merit", percentage=Decimal("10.00"),
            valid_from=timezone.now().date() - timedelta(days=60),
            valid_to=timezone.now().date() - timedelta(days=30),
            verified=True,
        )
        response = self.create_invoice()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        invoice = Invoice.objects.get(student=self.student)
        self.assertEqual(invoice.previous_balance, Decimal("1000.00"))


class ConcessionModelTests(TestCase):
    def setUp(self):
        self.klass = StudentClass.objects.create(name="Concession Model Class")
        self.student = make_student(self.klass, registration_number="REG/CONC/MODEL/0001")

    def test_clean_rejects_both_percentage_and_fixed_amount(self):
        concession = Concession(
            student=self.student, concession_type="merit",
            percentage=Decimal("10.00"), fixed_amount=Decimal("100.00"),
            valid_from=timezone.now().date(), valid_to=timezone.now().date() + timedelta(days=30),
        )
        with self.assertRaises(Exception):
            concession.clean()

    def test_clean_rejects_neither_percentage_nor_fixed_amount(self):
        concession = Concession(
            student=self.student, concession_type="merit",
            valid_from=timezone.now().date(), valid_to=timezone.now().date() + timedelta(days=30),
        )
        with self.assertRaises(Exception):
            concession.clean()

    def test_is_active_on_requires_verified_and_within_date_range(self):
        concession = Concession.objects.create(
            student=self.student, concession_type="merit", percentage=Decimal("10.00"),
            valid_from=timezone.now().date(), valid_to=timezone.now().date() + timedelta(days=10),
            verified=True,
        )
        self.assertTrue(concession.is_active_on(timezone.now().date()))
        self.assertFalse(concession.is_active_on(timezone.now().date() + timedelta(days=20)))

        concession.verified = False
        self.assertFalse(concession.is_active_on(timezone.now().date()))


class DefaulterFlagTests(TestCase):
    """Overdue escalation flag computed from due_date + balance."""

    def setUp(self):
        self.session, self.term = make_session_and_term()
        self.klass = StudentClass.objects.create(name="Defaulter Class 1", tuition_fees=Decimal("500.00"))
        self.student = make_student(self.klass, registration_number="REG/DEF/0001")

    def make_unpaid_invoice(self, days_overdue):
        invoice = Invoice.objects.create(
            student=self.student, session=self.session, term=self.term,
            class_for=self.klass, previous_balance=Decimal("0.00"),
            due_date=timezone.now().date() - timedelta(days=days_overdue),
        )
        InvoiceItem.objects.create(invoice=invoice, description="Tuition Fee", amount=Decimal("500.00"))
        invoice.save()
        return invoice

    def test_no_due_date_returns_none(self):
        invoice = Invoice.objects.create(
            student=self.student, session=self.session, term=self.term,
            class_for=self.klass, previous_balance=Decimal("0.00"),
        )
        self.assertIsNone(invoice.defaulter_flag())

    def test_fully_paid_returns_none_even_if_overdue(self):
        invoice = self.make_unpaid_invoice(days_overdue=100)
        Receipt.objects.create(invoice=invoice, amount_paid=Decimal("500.00"), date_paid=timezone.now())
        self.assertIsNone(invoice.defaulter_flag())

    def test_not_yet_overdue_returns_none(self):
        invoice = self.make_unpaid_invoice(days_overdue=3)
        self.assertIsNone(invoice.defaulter_flag())

    def test_yellow_flag_after_7_days(self):
        invoice = self.make_unpaid_invoice(days_overdue=8)
        self.assertEqual(invoice.defaulter_flag(), "yellow")

    def test_orange_flag_after_30_days(self):
        invoice = self.make_unpaid_invoice(days_overdue=31)
        self.assertEqual(invoice.defaulter_flag(), "orange")

    def test_red_flag_after_60_days(self):
        invoice = self.make_unpaid_invoice(days_overdue=61)
        self.assertEqual(invoice.defaulter_flag(), "red")

    def test_critical_flag_after_90_days(self):
        invoice = self.make_unpaid_invoice(days_overdue=91)
        self.assertEqual(invoice.defaulter_flag(), "critical")
