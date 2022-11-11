"""
Представления общих страниц пользователей
"""

from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.views.generic import CreateView, ListView

from JunJob import models
from JunJob import func
from JunJob.accounts.forms import RegisterUserForm, LoginUserForm, ApplicationForm

# Views


def main_view(request):  # главная страница
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


def one_vacancy_view(request, vacancy_id):  # страница с информацией о вакансии
    vacancy = models.Vacancy.objects.get(id=vacancy_id)
    form = ApplicationForm
    can_answer = True
    try:
        if request.user.resume:
            can_answer = True
    except ObjectDoesNotExist:
        can_answer = False
    context = {
        'vacancy': vacancy,
        'form': form,
        'can_answer': can_answer,
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
            except DatabaseError:
                messages.error(request, 'Ошибка добавления отклика')
                return render(request, 'common/Vacancy.html', context=context)

        else:
            messages.error(request, 'Форма не валидна')
            return render(request, 'common/Vacancy.html', context=context)

    return render(request, 'common/Vacancy.html', context=context)


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
def custom_handler404(request, exception):
    return HttpResponseNotFound('Такой страницы не найдено')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка со стороны сервера, приносим свои извинения')
