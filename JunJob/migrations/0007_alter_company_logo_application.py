# Generated by Django 4.1 on 2022-08-27 12:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('JunJob', '0006_alter_company_logo_application'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(max_length=500000, upload_to='company_images'),
        ),
    ]
