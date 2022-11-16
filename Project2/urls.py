"""Project2 URL Configuration

The `urlpatterns` list routes URLs to Views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function Views
    1. Add an import:  from my_app import Views
    2. Add a URL to urlpatterns:  path('', Views.home, name='home')
Class-based Views
    1. Add an import:  from other_app.Views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import TemplateView

from JunJob.Views import views, views_user, views_company, views_vacancies


from JunJob.Views.views import custom_handler404
from JunJob.Views.views import custom_handler500


handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),
    # Главная
    path('', views.Main.as_view(), name='main'),
    # поиск
    path('search', views.Search.as_view(), name='search'),
    # Все вакансии
    path('vacancies', views.VacanciesListView.as_view(), name='vacancies'),
    # Специальность
    path('vacancies/cat/<int:specialty_id>', views.SpecialtyVacanciesView.as_view(), name='specialty'),
    # Вакансии компании
    path('companies/<int:company_id>', views_company.CompanyCard.as_view(), name='companycard'),
    # Одна вакансия
    path('vacancies/<int:vacancy_id>', views.VacancyView.as_view(), name='onevacancy'),
    # Подтверждение отправления
    path('vacancies/sent', TemplateView.as_view(template_name='common/sent.html'), name='sent'),

    # Все о компании
    # Моя компания - предложение создать
    path('user/company/create/', TemplateView.as_view(template_name='about_company/CreateCompany.html'),
         name='create_a_company'),
    # Моя компания создание
    path('user/company/form', views_company.CompanyCreateView.as_view(), name='my_company_form'),
    # Просмотр информации
    path('user/company/<int:pk>', views_company.UserCompany.as_view(), name='user_company'),
    # Редактирование
    path('user/company/edit/<int:pk>', views_company.CompanyEdit.as_view(), name='my_company_edit'),

    # информации о компании
    # Удаление компании
    path('mycompany/delete', views_company.delete_company_view, name='delete_company'),
    # Мои вакансии
    path('mycompany/vacancies/', views_vacancies.UsersVacancies.as_view(), name='my_vacancies'),
    # Создание вакансии
    path('mycompany/vacancies/create/', views_vacancies.UsersVacancyCreate.as_view(), name='create_a_vacancy'),
    # Редактирование вакансии
    path('mycompany/vacancies/<int:pk>/edit', views_vacancies.VacancyEdit.as_view(), name='my_vacancy_edit'),
    # просмотр вакансии
    path('mycompany/vacancies/<int:pk>', views_vacancies.UserVacancy.as_view(), name='my_vacancy_view'),
    path('mycompany/vacancies/<int:vacancy_id>/delete', views_vacancies.my_vacancy_delete_view,
         name='my_vacancy_delete'),
    # отклик на вакансию
    path('mycompany/vacancies/application/<int:pk>', views_vacancies.Application.as_view(),
         name='application'),
    # резюме откликнувшегося
    path('mycompany/vacancies/application/resume/<int:user_id>', views_vacancies.application_resume_view,
         name='user_resume'),
    # написание ответа на отклик
    path('mycompany/vacancies/answer/<int:application_id>', views_company.AnswerView.as_view(), name='answer'),

    # аутентификация
    path('login', views.LoginUser.as_view(), name='login'),
    path('register', views.Register.as_view(), name='register'),
    path('logout', LogoutView.as_view()),

    # about user
    path('profile', views_user.profile_view, name='profile'),
    path('profile/edit', views_user.profile_edit, name='profile_edit'),
    # страница предложения создания резюме
    path('resume/create', TemplateView.as_view(template_name='accounts/resume_create.html'), name='resume_create'),
    # страница создания резюме
    path('resume/create/form', views_user.resume_create_form_view, name='resume_create_form'),
    path('resume/edit/<int:pk>', views_user.ResumeEdit.as_view(), name='resume_edit'),
    path('resume/', views_user.resume_view, name='resume'),
    path('resume/delete', views_user.resume_delete_view, name='resume_delete')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
