# DriveEasy - Vehicle Rental System

A full-featured vehicle rental web application built with Django, PostgreSQL, Docker, and Bootstrap 5.

---

## Features

### For Customers
- **Browse Vehicles** — View all available vehicles with photos, specs, and daily rates
- **Search & Filter** — Filter by vehicle type, price range, and availability
- **Live Cost Calculator** — Instantly see the estimated rental cost before booking
- **Book a Vehicle** — Select pickup/drop-off location and dates with validation
- **Manage Bookings** — View all bookings and cancel pending ones
- **User Accounts** — Register, login, and manage your profile (phone, address, driver's license)

### For Admins
- **Admin Dashboard** — Full Django admin panel at `/admin`
- **Fleet Management** — Add, edit, and toggle vehicle availability
- **Booking Oversight** — View and update booking statuses
- **Customer Management** — View customer profiles and booking history

### Vehicle Types Supported
- Sedan, SUV, Truck, Van, Sports Car, Luxury, Electric

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2 |
| Database | PostgreSQL 15 |
| Frontend | Bootstrap 5 + Bootstrap Icons |
| Static Files | WhiteNoise |
| Web Server | Gunicorn |
| Containerization | Docker + Docker Compose |

---

## How to Run

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

### Steps

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd vehicle-rental
```

**2. Start the application**
```bash
docker-compose up --build
```

**3. Open in browser**
```
http://localhost:8000
```

**4. Access the admin panel**
```
http://localhost:8000/admin
Username: admin
Password: admin123
```

> The first run will automatically run migrations, load 8 sample vehicles, and create the admin account.

---

## Stopping & Restarting

```bash
# Stop containers
docker-compose down

# Start again (no rebuild needed)
docker-compose up

# Rebuild after code changes
docker-compose up --build

# Stop and wipe the database
docker-compose down -v
```

---

## Project Structure

```
vehicle-rental/
├── config/                 # Django project settings & URLs
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── rentals/                # Main application
│   ├── models.py           # Vehicle, Booking, CustomerProfile
│   ├── views.py            # All page views
│   ├── forms.py            # Booking, registration, profile forms
│   ├── admin.py            # Admin panel configuration
│   ├── urls.py             # URL routing
│   ├── fixtures/
│   │   └── initial_data.json   # 8 seed vehicles
│   ├── migrations/         # Database migrations
│   └── templates/          # HTML templates
│       ├── rentals/        # App templates
│       └── registration/   # Login & register templates
├── static/                 # Static assets
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh           # Startup script (migrate, seed, serve)
└── requirements.txt
```

---

## Default Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |

Regular users can register at `http://localhost:8000/register`
