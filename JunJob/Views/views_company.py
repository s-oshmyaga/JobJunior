"""
Представления компании пользователя (список вакансии компании, создание и редактирование
информации о компании),
создания ответа на отклик.
"""

from datetime import date
from django.contrib import messages
from django.db import DatabaseError
from django.db.transaction import atomic
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, FormView, DetailView, UpdateView

from JunJob import models
from JunJob.accounts.forms import MyCompanyForm, AnswerForm


class CompanyCard(ListView):  # список вакансий компании
    template_name = 'about_company/CompanyCard.html'
    context_object_name = 'company_vacancies_list'

    def get_queryset(self):
        company = models.Company.objects.get(id=self.kwargs['company_id'])
        return models.Vacancy.objects.filter(company=company).order_by('-published_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = models.Company.objects.get(id=self.kwargs['company_id'])
        return context


class CompanyCreateView(FormView):  # форма создания компании
    template_name = 'about_company/CreateCompanyForm.html'
    form_class = MyCompanyForm
    success_url = reverse_lazy('my_company_edit')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Форма заполнена некорректно')
        return self.render_to_response(self.get_context_data(form=form))


# просмотр информации о компании
class UserCompany(DetailView):
    model = models.Company
    context_object_name = 'company'
    template_name = 'about_company/MyCompany.html'


# редактирование информации о компании
class CompanyEdit(UpdateView):
    model = models.Company
    form_class = MyCompanyForm
    template_name = 'about_company/UserCompanyEdit.html'

    def get_success_url(self):
        return reverse('user_company', kwargs={'pk': self.request.user.company.id})


def delete_company_view(request):  # удаление компании
    company_for_delete = request.user.company
    try:
        company_for_delete.delete()
        return HttpResponseRedirect(reverse('main'))
    except DatabaseError:
        messages.error(request, 'Не удалось удалить компанию')
        return HttpResponseRedirect(reverse('my_company_edit'))


class AnswerView(FormView):  # представление написания ответа на отклик
    template_name = 'about_company/about_vacancies/answer.html'
    form_class = AnswerForm

    def form_valid(self, form):
        with atomic():
            application = models.Application.objects.get(id=self.kwargs['application_id'])
            # ответ на отклик отправлен, больше оклик выводить не надо
            application.is_viewed = True
            answer_form = form.save(commit=False)
            answer_form.application = application
            answer_form.date = date.today()
            answer_form.save()
            application.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка заполнения формы')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        application = models.Application.objects.get(id=self.kwargs['application_id'])
        vacancy_id = application.vacancy.id
        return reverse('my_vacancy_view', kwargs={'pk': vacancy_id})
