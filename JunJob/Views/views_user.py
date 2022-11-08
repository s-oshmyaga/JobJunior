from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from JunJob import models
from JunJob.accounts.forms import ResumeForm


def profile_view(request):  # страница профиля
    return render(request, 'accounts/profile.html')


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
            except:
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
    except:
        messages.error(request, 'Не удалось удалить резюме')
        return HttpResponseRedirect(reverse('resume'))
