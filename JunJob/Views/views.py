"""
Представления общих страниц пользователей (главной страницы, страницы поиска,
списка вакансий и информации об одной вакансии с возможностью оставить отклик
"""
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.db import DatabaseError
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView

from JunJob import models
from JunJob import func
from JunJob.accounts.forms import RegisterUserForm, LoginUserForm, ApplicationForm

# Views


class Main(ListView):
    # главная страница
    template_name = 'common/main.html'
    context_object_name = 'specialty_list'
    model = models.Specialty

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Main, self).get_context_data()
        # выводятся только первые 8 компаний
        if models.Company.objects.all()[:8].exists():
            context['company_list'] = models.Company.objects.all()[:8]
        else:  # если в базе данных меньше 8 компаний, пусть вернет все
            context['company_list'] = models.Company.objects.all()
        return context


class Search(ListView):
    # поиск
    template_name = 'common/search.html'
    model = models.Vacancy
    context_object_name = 'search_result'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            search_result = func.request_to_bd(query)
        else:  # если запрос отсутствует - вернуть пустой QuerySet
            search_result = models.Vacancy.objects.none()
        return search_result

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Search, self).get_context_data()
        context['query'] = self.request.GET.get('q')
        return context


class VacanciesListView(ListView):  # список вакансий
    model = models.Vacancy
    template_name = 'common/Vacancies.html'
    context_object_name = 'vacancies_list'
    paginate_by = 5

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


class VacancyView(FormView):
    # просмотр информации о вакансии и возможность оставить отклик
    template_name = 'common/Vacancy.html'
    form_class = ApplicationForm
    success_url = reverse_lazy('sent')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # если у пользователя есть резюме, can_answer выведет возможность откликнуться на вакансию
        if models.Resume.objects.filter(user=self.request.user).exists():
            can_answer = True
        else:
            can_answer = False
        context['can_answer'] = can_answer

        vacancy = models.Vacancy.objects.get(id=self.kwargs['vacancy_id'])
        # если у пользователя уже есть отклик на эту вакансию, второй оставить нельзя
        if models.Application.objects.filter(Q(vacancy=vacancy) & Q(user=self.request.user)).exists():
            has_application = True
        else:
            has_application = False
        context['has_application'] = has_application
        context['vacancy'] = vacancy
        return context

    def form_valid(self, form):
        application_form = form.save(commit=False)
        user = self.request.user
        application_form.user = user
        application_form.resume = user.resume
        application_form.vacancy = models.Vacancy.objects.get(id=self.kwargs['vacancy_id'])
        try:
            application_form.save()
        except DatabaseError:
            messages.error(self.request, 'Ошибка добавления отклика')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Форма не валидна')
        return self.render_to_response(self.get_context_data(form=form))


# authentication

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, 'Неверный логин или пароль')
        return self.render_to_response(self.get_context_data(form=form))


class Register(CreateView):
    template_name = 'accounts/Register.html'
    form_class = RegisterUserForm
    success_url = 'login'

    def form_valid(self, form):
        # автоматический вход при удачной регистрации
        user = form.save()
        login(self.request, user)
        return redirect('main')


# хэндлеры
def custom_handler404(request, exception):
    return render(request, 'Errors/404.html')


def custom_handler500(request):
    return render(request, 'Errors/500.html')


def custom_handler403(request, exception):
    return render(request, 'Errors/403.html')


def custom_handler400(request, exception):
    return render(request, 'Errors/400.html')
