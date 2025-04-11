from django.urls import path
from . import views

urlpatterns = [
    path('notification/create/', views.NotificationCreateView.as_view(), name='notification_create'),
    path('announcement/create/', views.AnnouncementCreateView.as_view(), name='announcement_create'),
    path('shoutout/create/', views.ShoutOutCreateView.as_view(), name='shoutout_create'),
]
