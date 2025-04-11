from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django import forms
from .models import Notification, Announcement, ShoutOut
from django.urls import reverse_lazy


class BaseNotificationForm(forms.ModelForm):
    class Meta:
        fields = ['title', 'message', 'delivery_type', 'recipients']
        widgets = {
            'recipients': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipients'].required = False

class NotificationForm(BaseNotificationForm):
    class Meta(BaseNotificationForm.Meta):
        model = Notification


class AnnouncementForm(BaseNotificationForm):
    class Meta(BaseNotificationForm.Meta):
        model = Announcement


class ShoutOutForm(BaseNotificationForm):
    class Meta(BaseNotificationForm.Meta):
        model = ShoutOut

class NotificationCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Notification
    form_class = NotificationForm
    template_name = 'notifications/form.html'
    success_message = "Notification sent successfully."
    permission_required = 'notifications.add_notification'
    success_url = reverse_lazy("notification_create")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title()
        return context



class AnnouncementCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'notifications/form.html'
    success_message = "Announcement posted successfully."
    permission_required = 'notifications.add_announcement'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title()
        return context



class ShoutOutCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = ShoutOut
    form_class = ShoutOutForm
    template_name = 'notifications/form.html'
    success_message = "Shoutout created successfully."
    permission_required = 'notifications.add_shoutout'

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name.title()
        return context

