from datetime import date
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse

from JunJob import models
from JunJob.accounts.forms import MyVacancyForm


class UsersVacancies(ListView):  # Мои вакансии (список)
    template_name = 'about_company/about_vacancies/VacanciesList.html'
    context_object_name = 'vacancies_list'

    def get_queryset(self):
        company = self.request.user.company
        return models.Vacancy.objects.filter(company=company)


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
