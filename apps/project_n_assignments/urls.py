from django.urls import path
from .views import * 


urlpatterns = [
    path('view/',AssignmentListView.as_view(),name="view-assignments"),
    path('create/',AssignmentCreateView.as_view(),name="create-assignment"),
    path('ajax/load-students/', LoadStudentsView.as_view(), name='ajax_load_students'),
    path("<int:pk>/update/", AssignmentUpdateView.as_view(), name="assignment-update"),
    path("delete/<int:pk>/", AssignmentDeleteView.as_view(), name="assignment-delete"),

]
