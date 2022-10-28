# Generated by Django 4.1 on 2022-10-28 10:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('JunJob', '0008_resume_application'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='grade',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='resume',
            name='status',
            field=models.CharField(max_length=30),
        ),
    ]
