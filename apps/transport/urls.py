from django.urls import path
from .views import (
    DriverListView, DriverCreateView, DriverUpdateView, DriverDeleteView, DriverDetailView,
    RouteListView, RouteCreateView, RouteUpdateView, RouteDeleteView, RouteDetailView,
    VehicleListView, VehicleCreateView, VehicleUpdateView, VehicleDeleteView, VehicleDetailView,
    TripListView, TripCreateView, TripUpdateView, TripDeleteView, TripDetailView
)

urlpatterns = [
    # Driver URLs
    path('drivers/', DriverListView.as_view(), name='driver-list'),
    path('drivers/new/', DriverCreateView.as_view(), name='driver-create'),
    path('drivers/<int:pk>/edit/', DriverUpdateView.as_view(), name='driver-update'),
    path('drivers/<int:pk>/delete/', DriverDeleteView.as_view(), name='driver-delete'),
    path('drivers/<int:pk>/', DriverDetailView.as_view(), name='driver-detail'),

    # Route URLs
    path('routes/', RouteListView.as_view(), name='route-list'),
    path('routes/new/', RouteCreateView.as_view(), name='route-create'),
    path('routes/<int:pk>/edit/', RouteUpdateView.as_view(), name='route-update'),
    path('routes/<int:pk>/delete/', RouteDeleteView.as_view(), name='route-delete'),
    path('routes/<int:pk>/', RouteDetailView.as_view(), name='route-detail'),

    # Vehicle URLs
    path('vehicles/', VehicleListView.as_view(), name='vehicle-list'),
    path('vehicles/new/', VehicleCreateView.as_view(), name='vehicle-create'),
    path('vehicles/<int:pk>/edit/', VehicleUpdateView.as_view(), name='vehicle-update'),
    path('vehicles/<int:pk>/delete/', VehicleDeleteView.as_view(), name='vehicle-delete'),
    path('vehicles/<int:pk>/', VehicleDetailView.as_view(), name='vehicle-detail'),

    # Trip URLs
    path('trips/', TripListView.as_view(), name='trip-list'),
    path('trips/new/', TripCreateView.as_view(), name='trip-create'),
    path('trips/<int:pk>/edit/', TripUpdateView.as_view(), name='trip-update'),
    path('trips/<int:pk>/delete/', TripDeleteView.as_view(), name='trip-delete'),
    path('trips/<int:pk>/', TripDetailView.as_view(), name='trip-detail'),
]
