from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse

from JunJob import models
from JunJob.accounts.forms import MyCompanyForm


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
