# Generated by Django 4.1 on 2022-11-23 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('JunJob', '0014_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='resume',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='applications', to='JunJob.resume'),
        ),
    ]