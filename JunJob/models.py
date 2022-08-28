from django.db import models
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField

from django.conf import settings

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=45)
    location = models.CharField(max_length=30)
    logo = models.ImageField(upload_to=settings.MEDIA_COMPANY_IMAGE_DIR, max_length=500000)
    description = models.TextField()
    employee_count = models.IntegerField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company', null=True)


class Specialty(models.Model):
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=40)
    picture = models.ImageField(upload_to=settings.MEDIA_SPECIALITY_IMAGE_DIR)


class Vacancy(models.Model):
    title = models.CharField(max_length=60)
    specialty = models.ForeignKey(Specialty, related_name='vacancies', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='vacancies', on_delete=models.CASCADE)
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.FloatField()
    salary_max = models.FloatField()
    published_at = models.DateField()


class Application(models.Model):
    written_username = models.CharField(max_length=70)
    written_phone = PhoneNumberField(unique=True, null=False, blank=False)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, related_name='applications', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='applications', on_delete=models.CASCADE, null=True)
