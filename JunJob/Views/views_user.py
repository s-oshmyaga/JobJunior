"""
Представления страниц пользователя
"""

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, DatabaseError

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView

from JunJob import models
from JunJob.accounts.forms import ResumeForm, ProfileForm, UserForm


def profile_view(request):  # страница профиля
    form_user = UserForm(instance=request.user)
    try:
        form_profile = ProfileForm(instance=request.user.profile)
    except ObjectDoesNotExist:
        form_profile = ProfileForm
    return render(request, 'accounts/profile.html', {'form_profile': form_profile,
                                                     'form_user': form_user})


def profile_edit(request):  # изменение профиля
    form_user = UserForm(instance=request.user)
    try:
        form_profile = ProfileForm(instance=request.user.profile)
    except ObjectDoesNotExist:
        form_profile = ProfileForm
    if request.method == 'POST':
        try:
            form_profile = ProfileForm(request.POST, instance=request.user.profile)
        except ObjectDoesNotExist:
            form_profile = ProfileForm(request.POST)
        form_user = UserForm(request.POST, instance=request.user)
        if form_profile.is_valid() and form_user.is_valid():
            try:
                profile = form_profile.save(commit=False)
                profile.user = request.user
                profile.save()
                form_user.save()
                return HttpResponseRedirect(reverse('profile'))
            except DatabaseError:
                messages.error(request, 'Ошибка редактирования резюме')
                return render(request, 'accounts/profile_edit.html', {'form_profile': form_profile,
                                                                      'form_user': form_user})
        else:
            messages.error(request, 'Некорректное заполнение формы')
            return render(request, 'accounts/profile_edit.html', {'form_profile': form_profile,
                                                                  'form_user': form_user})
    return render(request, 'accounts/profile_edit.html', {'form_profile': form_profile,
                                                          'form_user': form_user})


def resume_create_form_view(request):  # страница создания резюме
    form = ResumeForm
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume_form = form.save(commit=False)
            resume_form.user = request.user
            try:
                resume_form.save()
                return HttpResponseRedirect(reverse('resume'))
            except IntegrityError:
                messages.error(request, 'У вас уже есть резюме')
                return render(request, 'accounts/resume_create_form.html', {'form': form})
            except DatabaseError:
                messages.error(request, 'Ошибка создания резюме')
                return render(request, 'accounts/resume_create_form.html', {'form': form})
        else:
            messages.error(request, 'Ошибка в заполнении формы')
            return render(request, 'accounts/resume_create_form.html', {'form': form})
    return render(request, 'accounts/resume_create_form.html', {'form': form})


def resume_view(request):  # страница готового резюме
    resume_user = request.user.resume
    form = ResumeForm(instance=resume_user)
    return render(request, 'accounts/resume.html', {'form': form})


class ResumeEdit(UpdateView):  # редактирование резюме
    template_name = 'accounts/resume_edit.html'
    success_url = reverse_lazy('resume')
    model = models.Resume
    form_class = ResumeForm


def resume_delete_view(request):  # удаление резюме
    resume_for_delete = request.user.resume
    try:
        resume_for_delete.delete()
        return HttpResponseRedirect(reverse('profile'))
    except DatabaseError:
        messages.error(request, 'Не удалось удалить резюме')
        return HttpResponseRedirect(reverse('resume'))


def user_answers_view(request):  # просмотр приглашений пользователя
    pass
