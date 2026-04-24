from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('truck', 'Truck'),
        ('van', 'Van'),
        ('sports', 'Sports Car'),
        ('luxury', 'Luxury'),
        ('electric', 'Electric'),
    ]

    FUEL_TYPES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]

    TRANSMISSION_TYPES = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
    ]

    name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    license_plate = models.CharField(max_length=20, unique=True)
    color = models.CharField(max_length=30)
    seats = models.PositiveIntegerField(default=5)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES, default='petrol')
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_TYPES, default='automatic')
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    mileage = models.PositiveIntegerField(default=0, help_text="Odometer reading in km")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, help_text="External image URL (used when no file is uploaded)")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.year} {self.make} {self.model} ({self.license_plate})"

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url or None

    @property
    def type_badge_color(self):
        colors = {
            'sedan': 'primary', 'suv': 'success', 'truck': 'warning',
            'van': 'info', 'sports': 'danger', 'luxury': 'dark', 'electric': 'secondary',
        }
        return colors.get(self.vehicle_type, 'secondary')


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    pickup_location = models.CharField(max_length=200)
    dropoff_location = models.CharField(max_length=200)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking #{self.pk} - {self.customer.username} | {self.vehicle}"

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            days = (self.end_date - self.start_date).days
            if days > 0:
                self.total_cost = days * self.vehicle.daily_rate
        super().save(*args, **kwargs)

    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days

    @property
    def status_badge_color(self):
        colors = {
            'pending': 'warning', 'confirmed': 'info', 'active': 'success',
            'completed': 'secondary', 'cancelled': 'danger',
        }
        return colors.get(self.status, 'secondary')


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    license_number = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
