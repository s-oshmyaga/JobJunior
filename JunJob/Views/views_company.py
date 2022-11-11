"""
Представления компании пользователя, приглашения на собеседование
"""

from datetime import date
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, FormView
from django.urls import reverse, reverse_lazy

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


def my_company_create_view(request):  # страница предложения создания компании
    return render(request, 'about_company/CreateCompany.html')


class CompanyCreateView(FormView):  # пустая форма создания компании
    template_name = 'about_company/MyCompany.html'
    form_class = MyCompanyForm
    success_url = reverse_lazy('my_company_edit')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Форма заполнена некорректно')
        return self.render_to_response(self.get_context_data(form=form))


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


class AnswerView(FormView):  # представление написания приглашения на собеседование
    template_name = 'about_company/about_vacancies/answer.html'
    # success_url = reverse_lazy('main')
    form_class = AnswerForm

    def form_valid(self, form):
        application = models.Application.objects.get(id=self.kwargs['application_id'])
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
        return reverse('my_vacancy_view', kwargs={'vacancy_id': vacancy_id})
