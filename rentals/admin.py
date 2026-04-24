from django.contrib import admin
from .models import Vehicle, Booking, CustomerProfile


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['name', 'make', 'model', 'year', 'vehicle_type', 'daily_rate', 'is_available', 'image_url']
    list_filter = ['vehicle_type', 'is_available', 'fuel_type', 'transmission']
    search_fields = ['name', 'make', 'model', 'license_plate']
    list_editable = ['is_available', 'daily_rate']
    ordering = ['name']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'vehicle', 'start_date', 'end_date', 'total_cost', 'status']
    list_filter = ['status', 'start_date']
    search_fields = ['customer__username', 'vehicle__name', 'vehicle__license_plate']
    list_editable = ['status']
    readonly_fields = ['total_cost', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'license_number']
    search_fields = ['user__username', 'user__email', 'license_number']
