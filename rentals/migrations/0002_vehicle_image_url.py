from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='image_url',
            field=models.URLField(blank=True, help_text='External image URL (used when no file is uploaded)', max_length=500),
        ),
    ]
