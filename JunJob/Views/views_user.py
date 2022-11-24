"""
Представления страниц пользователя
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, FormView, ListView

from JunJob import models
from JunJob.accounts.forms import ResumeForm, ProfileForm, UserForm


def profile_view(request):  # страница профиля
    form_user = UserForm(instance=request.user)
    form_profile = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile.html', {'form_profile': form_profile,
                                                     'form_user': form_user})


def profile_edit(request):  # изменение профиля
    form_user = UserForm(instance=request.user)
    form_profile = ProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        form_profile = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        form_user = UserForm(request.POST, instance=request.user)
        if form_profile.is_valid() and form_user.is_valid():
            try:
                profile = form_profile.save(commit=False)
                profile.user = request.user
                profile.save()
                form_user.save()
                messages.success(request, 'Ваш профиль успешно изменен')
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


@login_required
def user_delete(request):
    if request.method == 'POST':
        try:
            user = request.user
            user.delete()
            return HttpResponseRedirect(reverse_lazy('main'))
        except DatabaseError:
            messages.error(request, 'Не удалось удалить профиль')
    return render(request, 'accounts/delete_user.html')


class ResumeCreate(FormView):  # создание резюме
    template_name = 'accounts/resume_create_form.html'
    form_class = ResumeForm
    success_url = reverse_lazy('resume')

    def form_valid(self, form):
        resume_form = form.save(commit=False)
        resume_form.user = self.request.user
        try:
            resume_form.save()
        except DatabaseError:
            messages.error(self.request, 'Ошибка создания резюме')
            return self.render_to_response(self.get_context_data(form=form))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Форма заполнена некорректно')
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # Проверка наличия у пользователя резюме
        # Если уже есть - выведется информация о его наличии
        if models.Resume.objects.filter(user=self.request.user).exists():
            context['has_resume'] = True
        else:
            context['has_resume'] = False
        return context


def resume_view(request):  # страница готового резюме
    resume_user = request.user.resume
    form = ResumeForm(instance=resume_user)
    return render(request, 'accounts/resume.html', {'form': form})


class ResumeEdit(UpdateView):  # редактирование резюме
    template_name = 'accounts/resume_edit.html'
    model = models.Resume
    form_class = ResumeForm
    success_url = reverse_lazy('resume')


def resume_delete_view(request):  # удаление резюме
    resume_for_delete = request.user.resume
    try:
        resume_for_delete.delete()
        return HttpResponseRedirect(reverse('profile'))
    except DatabaseError:
        messages.error(request, 'Не удалось удалить резюме')
        return HttpResponseRedirect(reverse('resume'))


class Applications(ListView):
    template_name = 'accounts/user_applications.html'
    context_object_name = 'application_list'

    def get_queryset(self):
        return models.Application.objects.filter(user=self.request.user)


def application_delete(requset, application_id):
    application = models.Application.objects.get(id=application_id)
    application.delete()
    return HttpResponseRedirect(reverse_lazy('user_applications'))


class Answers(ListView):  # просмотр приглашений пользователя
    template_name = 'accounts/answers.html'
    context_object_name = 'answers_list'

    def get_queryset(self):
        return models.Answer.objects.filter(application__user=self.request.user)
