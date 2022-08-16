from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.views.generic import CreateView

from JunJob import models

# Create your views here.


def main_view(request):
    specialty_list = models.Specialty.objects.all()
    company_list = models.Company.objects.all()
    context = {
        'specialty_list': specialty_list,
        'company_list': company_list,
        }
    return render(request, 'main.html', context=context)


def vacancies_view(request):
    vacancies_list = models.Vacancy.objects.all()
    context = {
        'vacancies_list': vacancies_list,
    }
    return render(request, 'Vacancies.html', context=context)


def specialty_view(request, specialty_id):
    specialty = models.Specialty.objects.get(id=specialty_id)
    specialty_vacancies = models.Vacancy.objects.filter(specialty=specialty)
    context = {
        'specialty_vacancies': specialty_vacancies,
        'specialty': specialty,
    }
    return render(request, 'Specialty.html', context=context)


def company_card_view(request, company_id):
    company = models.Company.objects.get(id=company_id)
    company_vacancies_list = models.Vacancy.objects.filter(company=company)
    context = {
        'company': company,
        'company_vacancies_list': company_vacancies_list,
    }
    return render(request, 'CompanyCard.html', context=context)


def one_vacancy_view(request, vacancy_id):
    vacancy = models.Vacancy.objects.get(id=vacancy_id)
    context = {
        'vacancy': vacancy,
    }
    return render(request, 'Vacancy.html', context=context)


def send_an_application_view(request):  # Отправка заявки
    return render(request, 'send.html')


def my_company_lets_start_view(request):  # Моя компания (предложение создать)
    pass


def my_company_create_view(request):  # Моя компания (пустая форма)
    pass


def my_company_form_view(request):  # Моя компания (заполненная форма)
    return render(request, 'MyCompany.html')


def my_company_vacancies_view(request):  # Мои вакансии (список)
    return render(request, 'VacanciesList.html')


def my_company_vacancies_create_view(request):  # Мои вакансии (пустая форма)
    pass


def my_company_one_vacancy_view(request, vacancy_id):  # Одна моя вакансия (заполненная форма)
    return render(request, 'OneMyVacancy.html')


# authentication
class UserLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'Login.html'


class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'Register.html'


# хэндлеры
def custom_handler404(request, exceprion):
    return HttpResponseNotFound('Такой страницы не найдено')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка со стороны сервера, приносим свои извинения')
