from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from apps.result.utils import PermissionRequiredMessageMixin
from django.http import JsonResponse
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from apps.attendance.models import Student, Staff, StudentAttendance, StaffAttendance
from apps.finance.models import Invoice, Receipt
from datetime import timedelta
from django.db.models import F, Case, When, Value, Sum, OuterRef, Subquery, Max
from django.utils import timezone
from .forms import UserForm, UserCreateForm
from django.forms import widgets
from django.contrib.auth import get_user_model
user = get_user_model()


class UsersListView(LoginRequiredMixin,PermissionRequiredMessageMixin, SuccessMessageMixin, ListView):
    model = user
    context_object_name = "users"
    permission_required = "auth.view_user"
    template_name = "user/users_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        for user in queryset:
            if user.is_superuser:
                user.role = 'Admin'
            elif user.is_staff:
                user.role = 'Staff'
            else:
                user.role = 'Student'
        return queryset

class UserCreateView(LoginRequiredMixin, PermissionRequiredMessageMixin, SuccessMessageMixin, CreateView):
    model = user
    form_class = UserCreateForm
    template_name = 'user/user_form.html'
    success_message = "New user successfully added."
    permission_required = 'auth.add_user'
    success_url = reverse_lazy('users-list')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['student_or_staff'].widget.attrs.update({'onchange': 'updateUserList(this)'})
        return form

    def form_valid(self, form):
        selected_role = form.cleaned_data.get('student_or_staff')
        selected_person_id = form.cleaned_data.get('selected_person')
        password = form.cleaned_data.get('password')
        
        # Set first_name and last_name based on selected student or staff
        if selected_role == 'student':
            selected_person = Student.objects.get(id=selected_person_id)
            group_name = 'Students'
            if selected_person.user:
                form.add_error(None, f"A user account already exists for the student {selected_person.firstname} {selected_person.surname}.")
                return self.form_invalid(form)
        elif selected_role == 'staff':
            selected_person = Staff.objects.get(id=selected_person_id)
            group_name = 'Staff'
            if selected_person.user:
                form.add_error(None, f"A user account already exists for the staff member {selected_person.firstname} {selected_person.surname}.")
                return self.form_invalid(form)
        else:
            group_name = 'Admin'  # Default or Admin group

        form.instance.first_name = selected_person.firstname
        form.instance.last_name = selected_person.surname
        form.instance.password = make_password(password)

        # Assign the user to the appropriate group
        group, _ = Group.objects.get_or_create(name=group_name)
        form.instance.save()
        form.instance.groups.add(group)

        # Associate the user with the selected student or staff
        selected_person.user = form.instance
        selected_person.save()

        return super(UserCreateView, self).form_valid(form)

class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin,PermissionRequiredMessageMixin, UpdateView):
    model = user
    fields = ("is_active","username")
    success_message = "Record successfully updated."
    template_name = "user/user_form.html"
    permission_required = 'auth.update_user'
    success_url = reverse_lazy('users-list')

class UserDeleteView(LoginRequiredMixin,PermissionRequiredMessageMixin, DeleteView):
    permission_required = 'auth.delete_user' 
    model = user
    template_name = "user/user_confirm_delete.html"
    success_url = reverse_lazy("users-list")

def get_users_list(request):
    role = request.GET.get('role')
    if role == 'student':
        users = Student.objects.all().values('id', 'firstname', 'surname','other_name','registration_number')
        users_list = [{'id': user['id'], 'name': f"{user['surname']} {user['firstname']} {user['other_name']} ({user['registration_number']})"} for user in users]
    else:
        users = Staff.objects.all().values('id', 'firstname', 'surname','other_name')
        users_list = [{'id': user['id'], 'name': f"{user['surname']} {user['firstname']} {user['other_name']}"} for user in users]
    
   
    
    return JsonResponse(users_list, safe=False)