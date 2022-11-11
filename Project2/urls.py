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


from JunJob.Views import views, views_user, views_company, views_vacancies


from JunJob.Views.views import custom_handler404
from JunJob.Views.views import custom_handler500


handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),
    # Главная
    path('', views.main_view, name='main'),
    # поиск
    path('search', views.search_view, name='search'),
    # Все вакансии
    path('vacancies', views.VacanciesListView.as_view(), name='vacancies'),
    # Специальность
    path('vacancies/cat/<int:specialty_id>', views.SpecialtyVacanciesView.as_view(), name='specialty'),
    # Вакансии компании
    path('companies/<int:company_id>', views_company.CompanyCard.as_view(), name='companycard'),
    # Одна вакансия
    path('vacancies/<int:vacancy_id>', views.one_vacancy_view, name='onevacancy'),

    # Все о компании
    # Моя компания - создать
    path('mycompany/create/', views_company.my_company_create_view, name='create_a_company'),
    # Моя компания создание
    path('mycompany/', views_company.CompanyCreateView.as_view(), name='my_company_form'),
    # Редактирование
    path('mycompany/edit', views_company.my_company_edit_view, name='my_company_edit'),

    # информации о компании
    # Удаление компании
    path('mycompany/delete', views_company.delete_company_view, name='delete_company'),
    # Мои вакансии
    path('mycompany/vacancies/', views_vacancies.UsersVacancies.as_view(), name='my_vacancies'),
    # Создание вакансии
    path('mycompany/vacancies/create/', views_vacancies.UsersVacancyCreate.as_view(), name='create_a_vacancy'),
    # Редактирование вакансии (заполненная форма)
    path('mycompany/vacancies/<int:vacancy_id>/edit', views_vacancies.my_vacancy_edit_view, name='my_vacancy_edit'),
    # просмотр вакансии
    path('mycompany/vacancies/<int:vacancy_id>', views_vacancies.my_vacancy_view, name='my_vacancy_view'),
    path('mycompany/vacancies/<int:vacancy_id>/delete', views_vacancies.my_vacancy_delete_view,
         name='my_vacancy_delete'),
    # отклик на вакансию
    path('mycompany/vacancies/application/<int:application_id>', views_vacancies.application_view, name='application'),
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
    path('resume/create', views_user.resume_create_view, name='resume_create'),
    path('resume/edit', views_user.resume_edit_view, name='resume_edit'),
    path('resume', views_user.resume_view, name='resume'),
    path('resume/delete', views_user.resume_delete_view, name='resume_delete')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
