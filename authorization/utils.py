# -*- coding: utf-8 -*-

"""

author: Polianok Bogdan

"""

import requests
from vkApi.vkApi import OAUTH_LINK, CLIENT_SECRET, APP_ID
from meetings.models import EventMember

def getUserData(request):
    """Получение данных о пользователе vk
    
    :param request:  объект запроса
    :return: словарь с значениями userId (id пользователя),
             accessToken (токен пользователя), expiresIn
             (время жизни сессии)
    """
    code = request.GET.get('code')
    url = OAUTH_LINK % (APP_ID, CLIENT_SECRET, code)
    data = requests.get(url).json()

    return {
        'userId': data['user_id'],
        'accessToken': data['access_token'],
        'expiresIn': data['expires_in'],
    }

def updateToken(userId, accessToken):
    """Обновляет значение токена в БД для пользователя
    
    :param userId: id пользователя (ключ)
    :param accessToken: токен пользователя
    :return: None
    """
    eventMember = EventMember.objects.get(eventMember_id=userId)
    eventMember.eventMember_token = accessToken
    eventMember.save()

def updateSession(request, userId, expiresIn):
    """
    Обновляет сессию
    :param request: объект запроса
    :param userId: id пользователя
    :param expiresIn: время жизни сессии
    :return: измененный объект запроса
    """
    request.session["userId"] = userId
    request.session.set_expiry(expiresIn)
    return request
