from django.contrib import admin

from JunJob.models import Company, Resume, Profile, Answer
from JunJob.models import Specialty
from JunJob.models import Vacancy
from JunJob.models import Application


# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    model = Company


class SpecialtyAdmin(admin.ModelAdmin):
    model = Specialty


class VacancyAdmin(admin.ModelAdmin):
    model = Vacancy


class ApplicationAdmin(admin.ModelAdmin):
    model = Application


class ResumeAdmin(admin.ModelAdmin):
    model = Resume


class ProfileAdmin(admin.ModelAdmin):
    model = Profile


class AnswerAdmin(admin.ModelAdmin):
    model = Answer


admin.site.register(Company, CompanyAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Answer, AnswerAdmin)
