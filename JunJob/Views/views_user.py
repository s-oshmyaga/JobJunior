"""
Представления страниц пользователя
"""

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, DatabaseError

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

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
            except DatabaseError:
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
    except DatabaseError:
        messages.error(request, 'Не удалось удалить резюме')
        return HttpResponseRedirect(reverse('resume'))


def user_answers_view(request):  # просмотр приглашений пользователя
    pass
