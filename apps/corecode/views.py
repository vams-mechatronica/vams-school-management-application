from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from apps.result.utils import PermissionRequiredMessageMixin
from .forms import (
    AcademicSessionForm,
    AcademicTermForm,
    CurrentSessionForm,
    SiteConfigForm,
    StudentClassForm,
    SubjectForm,
)
from .models import (
    AcademicSession,
    AcademicTerm,
    SiteConfig,
    StudentClass,
    Subject,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from apps.attendance.models import Student, Staff, StudentAttendance, StaffAttendance
from apps.finance.models import Invoice, Receipt
from datetime import timedelta
from django.db.models import F, Case, When, Value, Sum, OuterRef, Subquery, Max
from django.utils import timezone
import logging
logger = logging.getLogger()

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name="Students").exists():
            pk = request.user.pk
            student= Student.objects.get(user= pk)
            return redirect(reverse('student-dashboard', kwargs={'pk': student.pk}))
        return super().dispatch(request, *args, **kwargs)


class SiteConfigView(LoginRequiredMixin, PermissionRequiredMessageMixin, View):
    """Site Config View"""

    form_class = SiteConfigForm
    permission_required = "corecode.add_siteconfig"
    template_name = "corecode/siteconfig.html"

    def get(self, request, *args, **kwargs):
        formset = self.form_class(queryset=SiteConfig.objects.all())
        context = {"formset": formset}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        formset = self.form_class(request.POST, queryset=SiteConfig.objects.all())
        if formset.is_valid():
            formset.save()
            messages.success(request, "Configurations successfully updated")
        else:
            messages.error(request, f"There was an error updating the configurations. Errors: {formset.errors}")
        
        context = {"formset": formset, "title": "Configuration"}
        return render(request, self.template_name, context)


class SessionListView(LoginRequiredMixin,PermissionRequiredMessageMixin, SuccessMessageMixin, ListView):
    model = AcademicSession
    permission_required = "corecode.view_academicsession"
    template_name = "corecode/session_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AcademicSessionForm()
        return context


class SessionCreateView(LoginRequiredMixin,PermissionRequiredMessageMixin, SuccessMessageMixin, CreateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    permission_required = "corecode.add_academicsession"
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("sessions")
    success_message = "New session successfully added"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add new session"
        return context


class SessionUpdateView(LoginRequiredMixin,PermissionRequiredMessageMixin, SuccessMessageMixin, UpdateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    permission_required = "corecode.update_academicsession"
    success_url = reverse_lazy("sessions")
    success_message = "Session successfully updated."
    template_name = "corecode/mgt_form.html"

    def form_valid(self, form):
        obj = self.object
        if obj.current == False:
            terms = (
                AcademicSession.objects.filter(current=True)
                .exclude(name=obj.name)
                .exists()
            )
            if not terms:
                messages.warning(self.request, "You must set a session to current.")
                return redirect("session-list")
        return super().form_valid(form)


class SessionDeleteView(LoginRequiredMixin,PermissionRequiredMessageMixin, DeleteView):
    model = AcademicSession
    permission_required ="corecode.delete_academicsession"
    success_url = reverse_lazy("sessions")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The session {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current == True:
            messages.warning(request, "Cannot delete session as it is set to current")
            return redirect("sessions")
        messages.success(self.request, self.success_message.format(obj.name))
        return super(SessionDeleteView, self).delete(request, *args, **kwargs)


class TermListView(LoginRequiredMixin,PermissionRequiredMessageMixin, SuccessMessageMixin, ListView):
    model = AcademicTerm
    permission_required = "corecode.view_academicterm"
    template_name = "corecode/term_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AcademicTermForm()
        return context


class TermCreateView(LoginRequiredMixin,PermissionRequiredMessageMixin, SuccessMessageMixin, CreateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    permission_required = "corecode.add_academicterm"
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("terms")
    success_message = "New term successfully added"


class TermUpdateView(LoginRequiredMixin,PermissionRequiredMessageMixin, SuccessMessageMixin, UpdateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    permission_required = "corecode.update_academicterm"
    success_url = reverse_lazy("terms")
    success_message = "Term successfully updated."
    template_name = "corecode/mgt_form.html"

    def form_valid(self, form):
        obj = self.object
        if obj.current == False:
            terms = (
                AcademicTerm.objects.filter(current=True)
                .exclude(name=obj.name)
                .exists()
            )
            if not terms:
                messages.warning(self.request, "You must set a term to current.")
                return redirect("term")
        return super().form_valid(form)


class TermDeleteView(LoginRequiredMixin,PermissionRequiredMessageMixin, DeleteView):
    model = AcademicTerm
    permission_required = "corecode.delete_academicterm"
    success_url = reverse_lazy("terms")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The term {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current == True:
            messages.warning(request, "Cannot delete term as it is set to current")
            return redirect("terms")
        messages.success(self.request, self.success_message.format(obj.name))
        return super(TermDeleteView, self).delete(request, *args, **kwargs)


class ClassListView(LoginRequiredMixin,PermissionRequiredMessageMixin, SuccessMessageMixin, ListView):
    model = StudentClass
    permission_required = "corecode.view_studentclass"
    template_name = "corecode/class_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = StudentClassForm()
        return context


class ClassCreateView(LoginRequiredMixin,PermissionRequiredMessageMixin, SuccessMessageMixin, CreateView):
    model = StudentClass
    form_class = StudentClassForm
    permission_required = "corecode.add_studentclass"
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("classes")
    success_message = "New class successfully added"


class ClassUpdateView(LoginRequiredMixin,PermissionRequiredMessageMixin, SuccessMessageMixin, UpdateView):
    model = StudentClass
    fields = '__all__'
    permission_required = "corecode.update_studentclass"
    success_url = reverse_lazy("classes")
    success_message = "class successfully updated."
    template_name = "corecode/mgt_form.html"


class ClassDeleteView(LoginRequiredMixin,PermissionRequiredMessageMixin, DeleteView):
    model = StudentClass
    permission_required = "corecode.delete_studentclass"
    success_url = reverse_lazy("classes")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The class {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        print(obj.name)
        messages.success(self.request, self.success_message.format(obj.name))
        return super(ClassDeleteView, self).delete(request, *args, **kwargs)


class SubjectListView(LoginRequiredMixin,PermissionRequiredMessageMixin, SuccessMessageMixin, ListView):
    model = Subject
    permission_required = "corecode.view_subject"
    template_name = "corecode/subject_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SubjectForm()
        return context


class SubjectCreateView(LoginRequiredMixin,PermissionRequiredMessageMixin, SuccessMessageMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    permission_required = "corecode.add_subject"

    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("subjects")
    success_message = "New subject successfully added"


class SubjectUpdateView(LoginRequiredMixin,PermissionRequiredMessageMixin, SuccessMessageMixin, UpdateView):
    model = Subject
    fields = '__all__'
    permission_required = "corecode.update_subject"

    success_url = reverse_lazy("subjects")
    success_message = "Subject successfully updated."
    template_name = "corecode/mgt_form.html"


class SubjectDeleteView(LoginRequiredMixin,PermissionRequiredMessageMixin, DeleteView):
    model = Subject
    permission_required = "corecode.delete_subject"

    success_url = reverse_lazy("subjects")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The subject {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.name))
        return super(SubjectDeleteView, self).delete(request, *args, **kwargs)


class CurrentSessionAndTermView(LoginRequiredMixin, View):
    """Current SEssion and Term"""

    form_class = CurrentSessionForm
    template_name = "corecode/current_session.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(
            initial={
                "current_session": AcademicSession.objects.get(current=True),
                "current_term": AcademicTerm.objects.get(current=True),
            }
        )
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_Class(request.POST)
        if form.is_valid():
            session = form.cleaned_data["current_session"]
            term = form.cleaned_data["current_term"]
            AcademicSession.objects.filter(name=session).update(current=True)
            AcademicSession.objects.exclude(name=session).update(current=False)
            AcademicTerm.objects.filter(name=term).update(current=True)

        return render(request, self.template_name, {"form": form})


class DashboardDataAPIView(APIView):

    def get(self, request):
        today = now().date()
        # Get the current date and time (timezone-aware)
        nows = timezone.now()

        # Get the first day of the current month
        first_day_of_month = nows.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Calculate the last day of the current month
        next_month = (first_day_of_month + timezone.timedelta(days=31)).replace(day=1)
        last_day_of_month = next_month - timezone.timedelta(days=1)

        total_students = Student.objects.count()
        present_students = StudentAttendance.objects.filter(date=today, status='present').count()
        absent_students = StudentAttendance.objects.filter(date=today, status='absent').count()
        total_staff = Staff.objects.count()
        present_staff = StaffAttendance.objects.filter(time_in__date=today, status='present').count()
        absent_staff = StaffAttendance.objects.filter(time_in__date=today, status='absent').count()
        # Subquery to get the latest invoice for each student
        latest_invoice = Invoice.objects.filter(student=OuterRef('student')).order_by('-created_at')

        # Get the last created invoice for each student
        invoices = Invoice.objects.annotate(
            latest_created_at=Subquery(latest_invoice.values('created_at')[:1])
        ).filter(created_at=F('latest_created_at'))
        fees_balance = sum(invoice.balance() for invoice in invoices if invoice.balance() > 0)
        fees_received = Receipt.objects.filter(
            date_paid__gte=first_day_of_month,
            date_paid__lte=last_day_of_month
        ).aggregate(total_amount_paid=Sum('amount_paid'))['total_amount_paid']

        attendance_graph = {
            'labels': [],  # e.g., ['2023-01-01', '2023-01-02', ...]
            'present': [],  # e.g., [10, 20, ...]
            'absent': []    # e.g., [5, 3, ...]
        }

        # Assuming you have a method to get attendance data for the past week
        past_week_dates = [today - timedelta(days=i) for i in range(7)]
        for date in past_week_dates:
            attendance_graph['labels'].append(date.strftime('%Y-%m-%d'))
            attendance_graph['present'].append(StudentAttendance.objects.filter(date=date, status='present').count())
            attendance_graph['absent'].append(StudentAttendance.objects.filter(date=date, status='absent').count())

        data = {
            'total_students': total_students,
            'present_students': present_students,
            'absent_students': absent_students,
            'total_staff': total_staff,
            'present_staff': present_staff,
            'absent_staff': absent_staff,
            'fees_balance': fees_balance or 0,
            'fees_received': fees_received or 0,
            'attendance_graph': attendance_graph
        }

        return Response(data, status=status.HTTP_200_OK)
