"""
Представления общих страниц пользователей (главной страницы, страницы поиска,
списка вакансий и информации об одной вакансии с возможностью оставить отклик
"""

from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from django.http import HttpResponseNotFound, HttpResponseServerError
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
        context['company_list'] = models.Company.objects.all()
        return context


class Search(ListView):
    # поиск
    template_name = 'common/search.html'
    model = models.Vacancy
    context_object_name = 'search_result'

    def get_queryset(self):
        query = self.request.GET.get('q')
        search_result = func.request_to_bd(query)
        return search_result

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Search, self).get_context_data()
        context['query'] = self.request.GET.get('q')
        return context


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


class VacancyView(FormView):
    # просмотр информации о вакансии и возможность оставить отклик
    template_name = 'common/Vacancy.html'
    form_class = ApplicationForm
    success_url = reverse_lazy('sent')

    def get_context_data(self, **kwargs):
        # если у пользователя есть резюме, can_answer выведет возможность откликнуться на вакансию
        context = super(VacancyView, self).get_context_data()
        try:
            if self.request.user.resume:
                can_answer = True
        except ObjectDoesNotExist:
            can_answer = False
        context['can_answer'] = can_answer
        context['vacancy'] = models.Vacancy.objects.get(id=self.kwargs['vacancy_id'])
        return context

    def form_valid(self, form):
        application_form = form.save(commit=False)
        application_form.user = self.request.user
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


class Register(CreateView):
    template_name = 'accounts/Register.html'
    form_class = RegisterUserForm
    success_url = 'login'


# хэндлеры
def custom_handler404(request, exception):
    return HttpResponseNotFound('Такой страницы не найдено')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка со стороны сервера, приносим свои извинения')
