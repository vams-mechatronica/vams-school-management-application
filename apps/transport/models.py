from django.db import models

# Driver model
class Driver(models.Model):
    name = models.CharField(max_length=100)
    driver_photo = models.ImageField(upload_to="transport/driver/",null=True,blank=True)
    license_number = models.CharField(max_length=50, unique=True)
    upload_dl = models.ImageField(upload_to="transport/driver/dl/",null=True,blank=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.license_number})"

# Vehicle model
class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('bus', 'Bus'),
        ('van', 'Van'),
        ('car', 'Car'),
    ]

    vehicle_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    vehicle_image = models.ImageField(upload_to="transport/vehicle/",null=True,blank=True)
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.vehicle_number} - {self.vehicle_type}"

# Route model
class Route(models.Model):
    name = models.CharField(max_length=100, unique=True)
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    stops = models.TextField(help_text="Enter stop locations separated by commas")
    is_active = models.BooleanField(default=True)

    
    def __str__(self):
        return f"{self.name}: {self.start_location} to {self.end_location}"

# Trip model for Pickup and Drop Timings
class Trip(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    pickup_time = models.TimeField()
    drop_time = models.TimeField()
    days_operating = models.CharField(max_length=100, help_text="E.g., Monday-Friday")

    def __str__(self):
        return f"{self.route.name} - {self.vehicle.vehicle_number} ({self.pickup_time} / {self.drop_time})"
