from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError

# Create your views here.



def MainView(request):
    return render(request, 'main.html')

def VacanciesView(request):
    return render(request, 'Vacancies.html')

def SpecialtyView(request):
    return render(request, 'Specialty.html')

def CompanyCardView(request):
    return render(request, 'CompanyCard.html')

def OneVacancyView(request):
    return render(request, 'Vacancy.html')

def custom_handler404(request, exceprion):
    return HttpResponseNotFound('Такой страницы не найдено')

def custom_handler500(request):
    return HttpResponseServerError('Ошибка со стороны сервера, приносим свои извинения')