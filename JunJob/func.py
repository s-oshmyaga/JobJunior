"""
Функции для обработки запроса поиска
"""

from django.db.models import Q
from JunJob import models


def for_search_str(string):
    result = [x.strip(',:;!.') for x in string.split()]
    return result


def request_to_bd(string):
    search_vacancy = for_search_str(string)
    search_question = Q(title__icontains=search_vacancy[0]) | Q(skills__icontains=search_vacancy[0])
    len_search_vacancy = len(search_vacancy)
    if len_search_vacancy > 1:
        for i in range(1, len_search_vacancy):
            search_question |= Q(title__icontains=search_vacancy[i]) | \
                              Q(skills__icontains=search_vacancy[i])
    search_result = models.Vacancy.objects.filter(search_question)

    return search_result

