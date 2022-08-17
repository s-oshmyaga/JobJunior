from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from JunJob import models
from JunJob.accounts import forms

# Create your views here.
from JunJob.accounts.forms import RegisterUserForm, LoginUserForm


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

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'
    redirect_authenticated_user = True


class Register(CreateView):
    template_name = 'Register.html'
    form_class = RegisterUserForm
    success_url = 'login'


# хэндлеры
def custom_handler404(request, exceprion):
    return HttpResponseNotFound('Такой страницы не найдено')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка со стороны сервера, приносим свои извинения')
