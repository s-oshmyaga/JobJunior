from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError

from JunJob import models

# Create your views here.


def MainView(request):
    specialty_list = models.Specialty.objects.all()
    company_list = models.Company.objects.all()
    context = {
        'specialty_list': specialty_list,
        'company_list': company_list,
        }
    return render(request, 'main.html', context=context)


def VacanciesView(request):
    vacancies_list = models.Vacancy.objects.all()
    context = {
        'vacancies_list': vacancies_list,
    }
    return render(request, 'Vacancies.html', context=context)


def SpecialtyView(request, specialty_id):
    specialty = models.Specialty.objects.get(id=specialty_id)
    specialty_vacancies = models.Vacancy.objects.filter(specialty=specialty)
    context = {
        'specialty_vacancies': specialty_vacancies,
        'specialty': specialty,
    }
    return render(request, 'Specialty.html', context=context)


def CompanyCardView(request, company_id):

    return render(request, 'CompanyCard.html')


def OneVacancyView(request, vacancy_id):
    return render(request, 'Vacancy.html')


def custom_handler404(request, exceprion):
    return HttpResponseNotFound('Такой страницы не найдено')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка со стороны сервера, приносим свои извинения')