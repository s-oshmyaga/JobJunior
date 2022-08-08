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
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from JunJob.views import company_card_view
from JunJob.views import main_view
from JunJob.views import one_vacancy_view
from JunJob.views import specialty_view
from JunJob.views import vacancies_view

from JunJob.views import custom_handler404
from JunJob.views import custom_handler500

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('', main_view, name='main'),
    path('vacancies', vacancies_view, name='vacancies'),
    path('vacancies/cat/<int:specialty_id>', specialty_view, name='specialty'),
    path('companies/<int:company_id>', company_card_view, name='companycard'),
    path('vacancies/<int:vacancy_id>', one_vacancy_view, name='onevacancy'),
]
