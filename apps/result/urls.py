from django.urls import path

from .views import ResultListView, CreateResultView, EditResultsView

urlpatterns = [
    path("create/", CreateResultView.as_view(), name="create-result"),
    path("edit-results/", EditResultsView.as_view(), name="edit-results"),
    path("view/all", ResultListView.as_view(), name="view-results"),
]
