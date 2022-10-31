from django.contrib import admin

from JunJob.models import Company, Resume
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
    module = Resume


admin.site.register(Company, CompanyAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Vacancy, VacancyAdmin)
