from django.urls import path,include
from .views import *
urlpatterns = [
    path('account/',include('dj_rest_auth.urls')),
    path('account/registration/', include('dj_rest_auth.registration.urls')),
    path('students',StudentAPI.as_view()),

]
