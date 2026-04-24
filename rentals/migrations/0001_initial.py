from django.db import migrations, models
import django.core.validators
import django.db.models.deletion
import decimal


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('vehicle_type', models.CharField(choices=[('sedan', 'Sedan'), ('suv', 'SUV'), ('truck', 'Truck'), ('van', 'Van'), ('sports', 'Sports Car'), ('luxury', 'Luxury'), ('electric', 'Electric')], max_length=20)),
                ('make', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('year', models.PositiveIntegerField()),
                ('license_plate', models.CharField(max_length=20, unique=True)),
                ('color', models.CharField(max_length=30)),
                ('seats', models.PositiveIntegerField(default=5)),
                ('fuel_type', models.CharField(choices=[('petrol', 'Petrol'), ('diesel', 'Diesel'), ('electric', 'Electric'), ('hybrid', 'Hybrid')], default='petrol', max_length=20)),
                ('transmission', models.CharField(choices=[('automatic', 'Automatic'), ('manual', 'Manual')], default='automatic', max_length=20)),
                ('daily_rate', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(decimal.Decimal('0.01'))])),
                ('mileage', models.PositiveIntegerField(default=0, help_text='Odometer reading in km')),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='vehicles/')),
                ('is_available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('address', models.TextField(blank=True)),
                ('license_number', models.CharField(blank=True, max_length=50)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('pickup_location', models.CharField(max_length=200)),
                ('dropoff_location', models.CharField(max_length=200)),
                ('total_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('active', 'Active'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='auth.user')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='rentals.vehicle')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
