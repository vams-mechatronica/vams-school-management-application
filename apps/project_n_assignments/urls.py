from django.urls import path
from .views import * 


urlpatterns = [
    path('view/',AssignmentListView.as_view(),name="view-assignments"),
    path('create/',AssignmentCreateView.as_view(),name="create-assignment"),
]
