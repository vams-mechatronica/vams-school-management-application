from django.urls import path
from . import views

urlpatterns = [
    path('notification/create/', views.NotificationCreateView.as_view(), name='notification_create'),
    path('notification/view/', views.NotificationListView.as_view(), name='notification_view'),
    path('announcement/create/', views.AnnouncementCreateView.as_view(), name='announcement_create'),
    path('announcement/view/', views.AnnouncementListView.as_view(), name='announcement_view'),
    path('shoutout/create/', views.ShoutOutCreateView.as_view(), name='shoutout_create'),
    path('shoutout/view/', views.ShoutOutListView.as_view(), name='shoutout_view'),
    path('notifications/mark-read/', views.mark_notifications_read, name='mark_notifications_read')
]
