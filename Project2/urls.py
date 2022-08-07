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

from JunJob.views import CompanyCardView
from JunJob.views import MainView
from JunJob.views import OneVacancyView
from JunJob.views import SpecialtyView
from JunJob.views import VacanciesView

from JunJob.views import custom_handler404
from JunJob.views import custom_handler500

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('', MainView, name='main'),
    path('vacancies', VacanciesView, name='vacancies'),
    path('vacancies/cat/<int:specialty_id>', SpecialtyView, name='specialty'),
    path('companies/<int:company_id>', CompanyCardView, name='companycard'),
    path('vacancies/<int:vacancy_id>', OneVacancyView, name='onevacancy'),
]
