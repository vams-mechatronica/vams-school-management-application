from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from apps.result.utils import PermissionRequiredMessageMixin
from .models import Driver, Route, Trip, Vehicle
from .forms import DriverForm, RouteForm, TripForm, VehicleForm

# 🚗 Driver Views
class DriverListView(LoginRequiredMixin, PermissionRequiredMessageMixin, ListView):
    model = Driver
    template_name = 'transport/driver_list.html'
    permission_required = "transport.view_driver"

class DriverCreateView(LoginRequiredMixin, PermissionRequiredMessageMixin, CreateView):
    model = Driver
    form_class = DriverForm
    template_name = 'transport/driver_form.html'
    permission_required = "transport.add_driver"
    success_url = reverse_lazy('driver-list')

class DriverUpdateView(LoginRequiredMixin, PermissionRequiredMessageMixin, UpdateView):
    model = Driver
    form_class = DriverForm
    template_name = 'transport/driver_form.html'
    permission_required = "transport.change_driver"
    success_url = reverse_lazy('driver-list')

class DriverDeleteView(LoginRequiredMixin, PermissionRequiredMessageMixin, DeleteView):
    model = Driver
    template_name = 'transport/driver_confirm_delete.html'
    permission_required = "transport.delete_driver"
    success_url = reverse_lazy('driver-list')

class DriverDetailView(LoginRequiredMixin, PermissionRequiredMessageMixin, DetailView):
    model = Driver
    template_name = 'transport/driver_detail.html'
    permission_required = "transport.view_driver"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all vehicles associated with the driver
        context['vehicles'] = Vehicle.objects.filter(driver=self.object)
        return context


# 🛣️ Route Views
class RouteListView(LoginRequiredMixin, PermissionRequiredMessageMixin, ListView):
    model = Route
    template_name = 'transport/route_list.html'
    permission_required = "transport.view_route"

class RouteCreateView(LoginRequiredMixin, PermissionRequiredMessageMixin, CreateView):
    model = Route
    form_class = RouteForm
    template_name = 'transport/route_form.html'
    permission_required = "transport.add_route"
    success_url = reverse_lazy('route-list')

class RouteUpdateView(LoginRequiredMixin, PermissionRequiredMessageMixin, UpdateView):
    model = Route
    form_class = RouteForm
    template_name = 'transport/route_form.html'
    permission_required = "transport.change_route"
    success_url = reverse_lazy('route-list')

class RouteDeleteView(LoginRequiredMixin, PermissionRequiredMessageMixin, DeleteView):
    model = Route
    template_name = 'transport/route_confirm_delete.html'
    permission_required = "transport.delete_route"
    success_url = reverse_lazy('route-list')

class RouteDetailView(LoginRequiredMixin, PermissionRequiredMessageMixin, DetailView):
    model = Route
    template_name = 'transport/route_detail.html'
    permission_required = "transport.view_route"


# 🚌 Vehicle Views
class VehicleListView(LoginRequiredMixin, PermissionRequiredMessageMixin, ListView):
    model = Vehicle
    template_name = 'transport/vehicle_list.html'
    permission_required = "transport.view_vehicle"

class VehicleCreateView(LoginRequiredMixin, PermissionRequiredMessageMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'transport/vehicle_form.html'
    permission_required = "transport.add_vehicle"
    success_url = reverse_lazy('vehicle-list')

class VehicleUpdateView(LoginRequiredMixin, PermissionRequiredMessageMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'transport/vehicle_form.html'
    permission_required = "transport.change_vehicle"
    success_url = reverse_lazy('vehicle-list')

class VehicleDeleteView(LoginRequiredMixin, PermissionRequiredMessageMixin, DeleteView):
    model = Vehicle
    template_name = 'transport/vehicle_confirm_delete.html'
    permission_required = "transport.delete_vehicle"
    success_url = reverse_lazy('vehicle-list')

class VehicleDetailView(LoginRequiredMixin, PermissionRequiredMessageMixin, DetailView):
    model = Vehicle
    template_name = 'transport/vehicle_detail.html'
    permission_required = "transport.view_vehicle"


# 🚍 Trip Views
class TripListView(LoginRequiredMixin, PermissionRequiredMessageMixin, ListView):
    model = Trip
    template_name = 'transport/trip_list.html'
    permission_required = "transport.view_trip"

class TripCreateView(LoginRequiredMixin, PermissionRequiredMessageMixin, CreateView):
    model = Trip
    form_class = TripForm
    template_name = 'transport/trip_form.html'
    permission_required = "transport.add_trip"
    success_url = reverse_lazy('trip-list')

class TripUpdateView(LoginRequiredMixin, PermissionRequiredMessageMixin, UpdateView):
    model = Trip
    form_class = TripForm
    template_name = 'transport/trip_form.html'
    permission_required = "transport.change_trip"
    success_url = reverse_lazy('trip-list')

class TripDeleteView(LoginRequiredMixin, PermissionRequiredMessageMixin, DeleteView):
    model = Trip
    template_name = 'transport/trip_confirm_delete.html'
    permission_required = "transport.delete_trip"
    success_url = reverse_lazy('trip-list')

class TripDetailView(LoginRequiredMixin, PermissionRequiredMessageMixin, DetailView):
    model = Trip
    template_name = 'transport/trip_detail.html'
    permission_required = "transport.view_trip"
