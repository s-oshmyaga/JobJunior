from django.contrib import admin

from JunJob.models import Company
from JunJob.models import Specialty
from JunJob.models import Vacancy


# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    model = Company


class SpecialtyAdmin(admin.ModelAdmin):
    model = Specialty


class VacancyAdmin(admin.ModelAdmin):
    model = Vacancy


admin.site.register(Company, CompanyAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Vacancy, VacancyAdmin)
