"""
Представления вакансий компании пользователя, откликов на вакансии
"""


from datetime import date
from django.db import DatabaseError
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, FormView, DetailView, UpdateView
from django.urls import reverse, reverse_lazy

from JunJob import models
from JunJob.accounts.forms import MyVacancyForm, ResumeForm


class UsersVacancies(ListView):  # Вакансии пользователя (список)
    template_name = 'about_company/about_vacancies/VacanciesList.html'
    context_object_name = 'vacancies_list'

    def get_queryset(self):
        company = self.request.user.company
        return models.Vacancy.objects.filter(company=company)


class UsersVacancyCreate(FormView):  # Вакансия пользователя создание
    template_name = 'about_company/about_vacancies/CreateVacancy.html'
    form_class = MyVacancyForm
    success_url = reverse_lazy('my_vacancies')

    def form_valid(self, form):
        vacancy_form = form.save(commit=False)
        id_specialty = int(self.request.POST.get('specialty'))
        vacancy_form.specialty = models.Specialty.objects.get(id=id_specialty)
        vacancy_form.company = self.request.user.company
        vacancy_form.published_at = date.today()
        vacancy_form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Форма заполнена некорректно')
        return self.render_to_response(self.get_context_data(form=form))


class UserVacancy(DetailView):  # страница просмотра информации о вакансии
    # если есть отклики, на которые еще не ответили, они тоже выводятся
    model = models.Vacancy
    context_object_name = 'vacancy'
    template_name = 'about_company/about_vacancies/MyVacancy.html'

    def get_context_data(self, **kwargs):
        context = super(UserVacancy, self).get_context_data()
        vacancy = models.Vacancy.objects.get(id=self.kwargs['pk'])
        context['applications'] = models.Application.objects.filter(Q(vacancy=vacancy) & Q(is_viewed=False))
        return context


# редактирование вакансии
class VacancyEdit(UpdateView):
    template_name = 'about_company/about_vacancies/VacancyEdit.html'
    model = models.Vacancy
    form_class = MyVacancyForm

    def form_valid(self, form):
        vacancy_form = form.save(commit=False)
        id_specialty = int(self.request.POST.get('specialty'))
        vacancy_form.specialty = models.Specialty.objects.get(id=id_specialty)
        vacancy_form.company = self.request.user.company
        vacancy_form.published_at = date.today()
        vacancy_form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my_vacancy_view', kwargs={'pk': self.kwargs['pk']})


def my_vacancy_delete_view(request, vacancy_id):  # удаление вакансии
    vacancy_for_delete = models.Vacancy.objects.get(id=vacancy_id)
    try:
        vacancy_for_delete.delete()
        return HttpResponseRedirect(reverse('my_vacancies'))
    except DatabaseError:
        messages.error(request, 'Не удалось удалить вакансию')
        return HttpResponseRedirect(reverse('my_vacancies'))


class Application(DetailView):
    model = models.Application
    template_name = 'about_company/about_vacancies/Application.html'
    context_object_name = 'application'

    def get_context_data(self, **kwargs):
        context = super(Application, self).get_context_data()
        context['vacancy'] = models.Vacancy.objects.get(applications__id=self.kwargs['pk'])
        return context


def application_resume_view(request, user_id):  # просмотр резюме откликнувшегося
    user = models.User.objects.get(id=user_id)
    resume = models.Resume.objects.get(user=user)
    form = ResumeForm(instance=resume)
    return render(request, 'about_company/about_vacancies/Application-resume.html', {'form': form})
