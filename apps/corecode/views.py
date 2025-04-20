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
    SchoolDetailForm,HolidaysForm
)
from .models import (
    AcademicSession,
    AcademicTerm,
    SiteConfig,
    StudentClass,
    Subject,SchoolDetail, Holiday
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from apps.attendance.models import Student, Staff, StudentAttendance, StaffAttendance
from apps.finance.models import Invoice, Receipt
from datetime import timedelta

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

class SchoolDetailView(LoginRequiredMixin, SuccessMessageMixin, View):
    """Create or Update School Configuration"""

    template_name = "corecode/school_detail.html"
    success_message = "Configuration successfully updated"

    def get(self, request):
        school_detail = SchoolDetail.objects.first()
        form = SchoolDetailForm(instance=school_detail)  # Prefill form if data exists
        edit_mode = request.GET.get("edit", False)  # Check if edit mode is requested
        return render(request, self.template_name, {"form": form, "school_detail": school_detail, "edit_mode": edit_mode})

    def post(self, request):
        school_detail = SchoolDetail.objects.first()
        form = SchoolDetailForm(request.POST, request.FILES, instance=school_detail)

        if form.is_valid():
            form.save()
            return redirect("school-configs")  # Redirect after save

        return render(request, self.template_name, {"form": form, "school_detail": school_detail, "edit_mode": True})


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


class HolidayListView(ListView):
    model = Holiday
    template_name = 'holidays/holiday_list.html'
    context_object_name = 'holidays'
    queryset = Holiday.objects.order_by('date')

class HolidayCreateView(LoginRequiredMixin,PermissionRequiredMessageMixin, SuccessMessageMixin, CreateView):
    model = Holiday
    form_class = HolidaysForm
    permission_required = "corecode.add_holiday"

    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("holidays-list")
    success_message = "New holiday successfully added"