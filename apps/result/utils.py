def score_grade(score):
    if score <= 10:
        return "A"

from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

def has_permission(permission_name, message="You do not have permission to view this page.", redirect_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.has_perm(permission_name):
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, message)
                if redirect_url:
                    return redirect(redirect_url)
                else:
                    return redirect(request.META.get('HTTP_REFERER', reverse('home')))
        return _wrapped_view
    return decorator

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

class PermissionRequiredMessageMixin(PermissionRequiredMixin):
    permission_denied_message = "You do not have permission to perform this action."
    redirect_url = None  # Set a default redirect URL if needed

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        if self.redirect_url:
            return redirect(self.redirect_url)
        else:
            return redirect(self.request.META.get('HTTP_REFERER', reverse('home')))

