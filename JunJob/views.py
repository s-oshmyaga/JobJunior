from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse

from JunJob import models
from JunJob.accounts import forms

# Create your views here.
from JunJob.accounts.forms import RegisterUserForm, LoginUserForm, ApplicationForm, MyCompanyForm


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
    return render(request, 'about_company/CompanyCard.html', context=context)


def one_vacancy_view(request, vacancy_id):
    vacancy = models.Vacancy.objects.get(id=vacancy_id)
    form = ApplicationForm
    context = {
        'vacancy': vacancy,
        'form': form
    }

    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():  # Проверка валидности формы
            try:   # Если валидна добавляем пользователя и вакансию в форму
                application_form = form.save(commit=False)
                application_form.user = request.user
                application_form.vacancy = vacancy
                application_form.save()
                return render(request, 'sent.html', {'vacancy_id': vacancy.id})
            finally:
                messages.error(request, 'Ошибка добавления отклика')

        else:
            messages.error(request, 'Форма не валидна')
            return render(request, 'Vacancy.html', context=context)

    return render(request, 'Vacancy.html', context=context)


# все о компании
def my_company_create_view(request):  # страница предложения создания компании
    return render(request, 'about_company/CreateCompany.html')


def my_company_form_view(request):   # пустая форма создания компании
    form = MyCompanyForm

    if request.method == 'POST':
        form = MyCompanyForm(request.POST, request.FILES)
        if form.is_valid():
            my_company_form = form.save(commit=False)
            my_company_form.owner = request.user
            try:
                my_company_form.save()
                return HttpResponseRedirect(reverse('main'))
            except:
                messages.error(request, 'Ошибка добавления компании')
                return render(request, 'about_company/MyCompany.html', {'form': form})
        else:
            messages.error(request, 'Форма не валидна')
            return render(request, 'about_company/MyCompany.html', {'form': form})
    else:
        return render(request, 'about_company/MyCompany.html', {'form': form})


def my_company_edit_view(request):   # просмотр и редактирование формы
    my_company = request.user.company
    if request.method == 'POST':
        form = MyCompanyForm(request.POST, request.FILES, instance=my_company)
        if form.is_valid():
            company_form = form.save(commit=False)
            company_form.owner = request.user
            try:
                company_form.save()
                return HttpResponseRedirect(reverse('my_company_edit'))
            except:
                messages.error(request, 'Ошибка редактирования компании')
                return render(request, 'about_company/MyCompany.html', {'form': form})
        else:
            messages.error(request, 'Форма не валидна')
            return render(request, 'about_company/MyCompany.html', {'form': form})
    else:
        form = MyCompanyForm(instance=my_company)
    return render(request, 'about_company/MyCompany.html', {'form': form})


# вакансии
def my_company_vacancies_view(request):  # Мои вакансии (список)
    return render(request, 'about_company/VacanciesList.html')


def my_company_vacancies_create_view(request):  # Мои вакансии (пустая форма)
    pass


def my_company_one_vacancy_view(request, vacancy_id):  # Одна моя вакансия (заполненная форма)
    return render(request, 'about_company/OneMyVacancy.html')


# authentication

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class Register(CreateView):
    template_name = 'accounts/Register.html'
    form_class = RegisterUserForm
    success_url = 'login'


# хэндлеры
def custom_handler404(request, exceprion):
    return HttpResponseNotFound('Такой страницы не найдено')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка со стороны сервера, приносим свои извинения')
