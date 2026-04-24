from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('vehicles/<int:pk>/book/', views.book_vehicle, name='book_vehicle'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('bookings/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('api/calculate-cost/', views.calculate_cost, name='calculate_cost'),
]
