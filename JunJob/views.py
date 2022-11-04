from datetime import date
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, ListView
from django.urls import reverse

from JunJob import models
from JunJob import func
from JunJob.accounts.forms import RegisterUserForm, LoginUserForm, ApplicationForm, MyCompanyForm, MyVacancyForm, \
    ResumeForm


# views


def main_view(request):
    specialty_list = models.Specialty.objects.all()
    company_list = models.Company.objects.all()
    context = {
        'specialty_list': specialty_list,
        'company_list': company_list,
        }
    if request.GET.get('q'):
        search = request.GET.get('q')
        return search_view(request, query=search)
    return render(request, 'common/main.html', context=context)


def search_view(request, query=None):  # поиск
    if query:
        search_result = func.request_to_bd(query)
        return render(request, 'common/search.html', {'search_result': search_result,
                                                      'query': query})

    if request.GET.get('q'):
        search_vacancy = request.GET.get('q')
        search_result = func.request_to_bd(search_vacancy)
        return render(request, 'common/search.html', {'search_result': search_result,
                                                      'query': search_vacancy})

    return render(request, 'common/search.html')


class VacanciesListView(ListView):  # список вакансий
    model = models.Vacancy
    template_name = 'common/Vacancies.html'
    context_object_name = 'vacancies_list'

    def get_queryset(self):
        return models.Vacancy.objects.order_by('-published_at')


class SpecialtyVacanciesView(ListView):  # вакансии по специальности
    model = models.Vacancy
    template_name = 'common/Specialty.html'
    context_object_name = 'specialty_vacancies'

    def get_queryset(self):
        specialty = models.Specialty.objects.get(id=self.kwargs['specialty_id'])
        return models.Vacancy.objects.filter(specialty=specialty).order_by('-published_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specialty'] = models.Specialty.objects.get(id=self.kwargs['specialty_id'])
        return context


def company_card_view(request, company_id):  # список вакансий компании
    company = models.Company.objects.get(id=company_id)
    company_vacancies_list = models.Vacancy.objects.filter(company=company)
    context = {
        'company': company,
        'company_vacancies_list': company_vacancies_list,
    }
    return render(request, 'about_company/CompanyCard.html', context=context)


def one_vacancy_view(request, vacancy_id):  # страница с информацией о вакансии
    vacancy = models.Vacancy.objects.get(id=vacancy_id)
    form = ApplicationForm
    context = {
        'vacancy': vacancy,
        'form': form
    }

    if request.method == "POST":   # отклик на вакансию
        form = ApplicationForm(request.POST)
        if form.is_valid():  # Проверка валидности формы
            try:   # Если валидна добавляем пользователя и вакансию в форму
                application_form = form.save(commit=False)
                application_form.user = request.user
                application_form.vacancy = vacancy
                application_form.save()
                return render(request, 'common/sent.html', {'vacancy_id': vacancy.id})
            except:
                messages.error(request, 'Ошибка добавления отклика')
                return render(request, 'common/Vacancy.html', context=context)

        else:
            messages.error(request, 'Форма не валидна')
            return render(request, 'common/Vacancy.html', context=context)

    return render(request, 'common/Vacancy.html', context=context)


# все о компании пользователя
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
                return HttpResponseRedirect(reverse('my_company_edit'))
            except:
                messages.error(request, 'Ошибка добавления компании')
                return render(request, 'about_company/MyCompany.html', {'form': form})
        else:
            messages.error(request, 'Форма не валидна')
            return render(request, 'about_company/MyCompany.html', {'form': form})
    else:
        return render(request, 'about_company/MyCompany.html', {'form': form})


def my_company_edit_view(request):   # просмотр и редактирование формы компании
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


def delete_company_view(request):  # удаление компании
    company_for_delete = request.user.company
    try:
        company_for_delete.delete()
        return HttpResponseRedirect(reverse('main'))
    except:
        messages.error(request, 'Не удалось удалить компанию')
        return HttpResponseRedirect(reverse('my_company_edit'))


# мои вакансии
def my_company_vacancies_view(request):  # Мои вакансии (список)
    my_company = request.user.company
    vacancies_list = models.Vacancy.objects.filter(company=my_company)
    return render(request, 'about_company/about_vacancies/VacanciesList.html', {'vacancies_list': vacancies_list})


def my_vacancy_create_view(request):  # Моя вакансия создание
    form = MyVacancyForm

    if request.method == 'POST':
        form = MyVacancyForm(request.POST)
        if form.is_valid():
            vacancy_form = form.save(commit=False)
            id_specialty = int(request.POST.get('specialty'))
            vacancy_form.specialty = models.Specialty.objects.get(id=id_specialty)
            vacancy_form.company = request.user.company
            vacancy_form.published_at = date.today()
            try:
                vacancy_form.save()
                return HttpResponseRedirect(reverse('my_vacancies'))
            except:
                messages.error(request, 'Ошибка создания вакансии')
                return render(request, 'about_company/about_vacancies/CreateVacancy.html', {'form': form})
        else:
            messages.error(request, 'Форма не валидна')
            return render(request, 'about_company/about_vacancies/CreateVacancy.html', {'form': form})
    else:
        return render(request, 'about_company/about_vacancies/CreateVacancy.html', {'form': form})


def my_vacancy_edit_view(request, vacancy_id):  # моя вакансия редактирование
    vacancy = models.Vacancy.objects.get(id=vacancy_id)
    if request.method == 'POST':
        form = MyVacancyForm(request.POST, instance=vacancy)
        if form.is_valid():
            vacancy_form = form.save(commit=False)
            id_specialty = int(request.POST.get('specialty'))
            vacancy_form.specialty = models.Specialty.objects.get(id=id_specialty)
            vacancy_form.company = request.user.company
            vacancy_form.published_at = date.today()
            try:
                vacancy_form.save()
                return HttpResponseRedirect(reverse('my_vacancies'))
            except:
                messages.error(request, 'Ошибка создания вакансии')
                return render(request, 'about_company/about_vacancies/MyVacancyEdit.html', {'form': form,
                                                                                            'vacancy': vacancy})
        else:
            messages.error(request, 'Форма не валидна')
            return render(request, 'about_company/about_vacancies/MyVacancyEdit.html', {'form': form,
                                                                                        'vacancy': vacancy})
    else:
        form = MyVacancyForm(instance=vacancy)
        return render(request, 'about_company/about_vacancies/MyVacancyEdit.html', {'form': form,
                                                                                    'vacancy': vacancy})


def my_vacancy_view(request, vacancy_id):  # страница просмотра информации о вакансии
    vacancy = models.Vacancy.objects.get(id=vacancy_id)
    form = MyVacancyForm(instance=vacancy)
    applications = models.Application.objects.filter(vacancy=vacancy)
    return render(request, 'about_company/about_vacancies/MyVacancy.html', {'form': form,
                                                                            'vacancy': vacancy,
                                                                            'applications': applications})


def my_vacancy_delete_view(request, vacancy_id):  # удаление вакансии
    vacancy_for_delete = models.Vacancy.objects.get(id=vacancy_id)
    try:
        vacancy_for_delete.delete()
        return HttpResponseRedirect(reverse('my_vacancies'))
    except:
        messages.error(request, 'Не удалось удалить вакансию')
        return HttpResponseRedirect(reverse('my_vacancies'))


# authentication

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class Register(CreateView):
    template_name = 'accounts/Register.html'
    form_class = RegisterUserForm
    success_url = 'login'


# Все о пользователе
def profile_view(request):  # страница профиля
    return render(request, 'accounts/profile.html')


def resume_create_view(request):  # страница предложения создания резюме
    return render(request, 'accounts/resume_create.html')


def resume_edit_view(request):  # страница создания и редактирования резюме
    try:
        user_resume = models.Resume.objects.get(user=request.user)
    except ObjectDoesNotExist:
        user_resume = None
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=user_resume)
        if form.is_valid():
            resume_form = form.save(commit=False)
            resume_form.user = request.user
            try:
                resume_form.save()
                return HttpResponseRedirect(reverse('resume'))
            except IntegrityError:
                messages.error(request, 'У вас уже есть резюме')
                return render(request, 'accounts/resume_edit.html', {'form': form})
            except:
                messages.error(request, 'Ошибка создания резюме')
                return render(request, 'accounts/resume_edit.html', {'form': form})
        else:
            messages.error(request, 'Ошибка в заполнении формы')
            return render(request, 'accounts/resume_edit.html', {'form': form})
    form = ResumeForm(instance=user_resume)
    return render(request, 'accounts/resume_edit.html', {'form': form})


def resume_view(request):  # страница готового резюме
    resume_user = request.user.resume
    form = ResumeForm(instance=resume_user)
    return render(request, 'accounts/resume.html', {'form': form})


def resume_delete_view(request):  # удаление резюме
    resume_for_delete = request.user.resume
    try:
        resume_for_delete.delete()
        return HttpResponseRedirect(reverse('profile'))
    except:
        messages.error(request, 'Не удалось удалить резюме')
        return HttpResponseRedirect(reverse('resume'))


# хэндлеры
def custom_handler404(request, exception):
    return HttpResponseNotFound('Такой страницы не найдено')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка со стороны сервера, приносим свои извинения')
