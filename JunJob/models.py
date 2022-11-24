from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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


class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume')
    name = models.CharField(max_length=60)
    surname = models.CharField(max_length=60)
    grade = models.CharField(max_length=10)
    status = models.CharField(max_length=30)
    salary = models.FloatField()
    specialty = models.CharField(max_length=20)
    education = models.CharField(max_length=100)
    experience = models.TextField()
    portfolio = models.CharField(max_length=200)


class Application(models.Model):
    written_username = models.CharField(max_length=70)
    written_phone = PhoneNumberField(unique=True, null=False, blank=False)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, related_name='applications', on_delete=models.CASCADE)
    is_viewed = models.BooleanField(blank=True, default=False)
    user = models.ForeignKey(User, related_name='applications', on_delete=models.CASCADE, null=True)
    resume = models.ForeignKey(Resume, related_name='applications', on_delete=models.CASCADE, null=True)


class Profile(models.Model):
    def validate_image(fieldfile_obj):  # проверка размера аватара
        filesize = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError("Максимальный размер файла %sMB" % str(megabyte_limit))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birthday = models.DateField(null=True, blank=True)
    country = models.CharField(null=True, blank=True, max_length=100)
    city = models.CharField(null=True, blank=True, max_length=100)
    avatar = models.ImageField(upload_to=settings.MEDIA_AVATAR_IMAGE_DIR, validators=[validate_image],
                               default='images/avatar.jpg')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Answer(models.Model):  # модель ответа работодателя на отклик
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='answer')
    answer_text = models.TextField()
    date = models.DateField()
