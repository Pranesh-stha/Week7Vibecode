from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Vehicle, Booking, CustomerProfile
from .forms import BookingForm, RegisterForm, CustomerProfileForm


def home(request):
    featured = Vehicle.objects.filter(is_available=True)[:6]
    total_vehicles = Vehicle.objects.count()
    available_vehicles = Vehicle.objects.filter(is_available=True).count()
    total_bookings = Booking.objects.count()
    return render(request, 'rentals/home.html', {
        'featured_vehicles': featured,
        'total_vehicles': total_vehicles,
        'available_vehicles': available_vehicles,
        'total_bookings': total_bookings,
    })


def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    vehicle_type = request.GET.get('type', '')
    search = request.GET.get('search', '')
    min_rate = request.GET.get('min_rate', '')
    max_rate = request.GET.get('max_rate', '')
    available_only = request.GET.get('available_only', '')

    if vehicle_type:
        vehicles = vehicles.filter(vehicle_type=vehicle_type)
    if search:
        vehicles = vehicles.filter(
            Q(name__icontains=search) | Q(make__icontains=search) |
            Q(model__icontains=search) | Q(description__icontains=search)
        )
    if min_rate:
        vehicles = vehicles.filter(daily_rate__gte=min_rate)
    if max_rate:
        vehicles = vehicles.filter(daily_rate__lte=max_rate)
    if available_only:
        vehicles = vehicles.filter(is_available=True)

    return render(request, 'rentals/vehicle_list.html', {
        'vehicles': vehicles,
        'vehicle_types': Vehicle.VEHICLE_TYPES,
        'selected_type': vehicle_type,
        'search': search,
        'min_rate': min_rate,
        'max_rate': max_rate,
        'available_only': available_only,
    })


def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    related = Vehicle.objects.filter(
        vehicle_type=vehicle.vehicle_type, is_available=True
    ).exclude(pk=pk)[:3]
    return render(request, 'rentals/vehicle_detail.html', {
        'vehicle': vehicle,
        'related_vehicles': related,
    })


@login_required
def book_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, is_available=True)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.vehicle = vehicle
            booking.save()
            vehicle.is_available = False
            vehicle.save()
            messages.success(request, f'Booking confirmed! Your booking ID is #{booking.pk}.')
            return redirect('my_bookings')
    else:
        form = BookingForm()
    return render(request, 'rentals/booking_form.html', {'vehicle': vehicle, 'form': form})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(customer=request.user).select_related('vehicle')
    return render(request, 'rentals/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, customer=request.user)
    if booking.status in ('pending', 'confirmed'):
        booking.status = 'cancelled'
        booking.save()
        booking.vehicle.is_available = True
        booking.vehicle.save()
        messages.success(request, 'Booking cancelled successfully.')
    else:
        messages.error(request, 'This booking cannot be cancelled.')
    return redirect('my_bookings')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            CustomerProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    profile_obj, _ = CustomerProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = CustomerProfileForm(instance=profile_obj)
    bookings_count = request.user.bookings.count()
    return render(request, 'rentals/profile.html', {
        'form': form, 'profile': profile_obj, 'bookings_count': bookings_count,
    })


def calculate_cost(request):
    vehicle_id = request.GET.get('vehicle_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if vehicle_id and start_date and end_date:
        from datetime import date
        try:
            vehicle = Vehicle.objects.get(pk=vehicle_id)
            start = date.fromisoformat(start_date)
            end = date.fromisoformat(end_date)
            days = (end - start).days
            if days > 0:
                cost = days * float(vehicle.daily_rate)
                return JsonResponse({'days': days, 'cost': round(cost, 2), 'daily_rate': float(vehicle.daily_rate)})
        except (Vehicle.DoesNotExist, ValueError):
            pass
    return JsonResponse({'error': 'Invalid data'}, status=400)
