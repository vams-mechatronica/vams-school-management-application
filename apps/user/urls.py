from django.urls import path
from .views import *

urlpatterns = [
    path('create-user/get-users-list/', get_users_list, name='get_users_list'),
    path('list/', UsersListView.as_view(),name="users-list"),
    path('create-user/', UserCreateView.as_view(), name='user-create'),
    path("<int:pk>/update/", UserUpdateView.as_view(), name="user-update"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="user-delete"),
]
