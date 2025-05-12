"""newapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi




schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

admin.site.site_header = "VAMSConnect"
admin.site.index_title = "VAMSConnect"
admin.site.site_title = "VAMSConnect"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/',include('apps.api.urls')),
    path("", include("apps.corecode.urls")),
    path("users/", include("apps.user.urls")),
    path("transport/", include("apps.transport.urls")),
    path("staff/", include("apps.staffs.urls")),
    path("result/", include("apps.result.urls")),
    path("student/", include("apps.students.urls")),
    path("assignment/", include("apps.project_n_assignments.urls")),
    path("finance/", include("apps.finance.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("attendance/", include("apps.attendance.urls")),
    path("time-table/", include("apps.timetable.urls")),
    path("alerts/", include("apps.notifications.urls")),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


]


# if not settings.DEBUG:
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)