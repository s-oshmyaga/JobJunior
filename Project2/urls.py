"""Project2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include


from JunJob import views


from JunJob.views import custom_handler404
from JunJob.views import custom_handler500


handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_view, name='main'),  # Главная
    path('vacancies', views.vacancies_view, name='vacancies'),  # Все вакансии
    path('vacancies/cat/<int:specialty_id>', views.specialty_view, name='specialty'),  # Специальность
    path('companies/<int:company_id>', views.company_card_view, name='companycard'),  # Вакансии компании
    path('vacancies/<int:vacancy_id>', views.one_vacancy_view, name='onevacancy'),  # Одна вакансия
    # path('vacancies/<int:vacancy_id>/sent/', views.sent_an_application_view, name='sent'),   # Отправка заявки
    # Все о компании
    # path('mycompany/letsstart/', views.my_company_lets_start_view, name='lets_start'),
    path('mycompany/create/', views.my_company_create_view, name='create_a_company'),  # Моя компания - создать
    path('mycompany/', views.my_company_view, name='my_company_form'),  # Моя компания (заполненная форма)

    path('mycompany/vacancies/', views.my_company_vacancies_view, name='my_vacancies'),  # Мои вакансии (список)
    path('mycompany/vacancies/create/', views.my_company_vacancies_create_view, name='create_a_vacancy'),   # Мои вакансии
    path('mycompany/vacancies/<int:vacancy_id>', views.my_company_one_vacancy_view, name='my_one_vacancy'),  # Одна моя
    # вакансия (заполненная форма)
    # аутентификация
    path('login', views.LoginUser.as_view(), name='login'),
    path('register', views.Register.as_view(), name='register'),
    path('logout', LogoutView.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
