# -*- coding: utf-8 -*-

from django.shortcuts import redirect, HttpResponse
from meetings.models import EventMember

import authorization.utils as utils
from vkApi.vkApi import AUTH_LINK


def authRedirect(request):
    return redirect(AUTH_LINK)


def authorization(request):
    """
    Получаем данные о пользователе (его token и id) и записываем их в куки
    :param request: объект запроса
    :return: redirect на главную страницу
    
    """
    if request.GET.get('error'):
        return HttpResponse('Authorization failed;')

    data = utils.getUserData(request)

    userId = data['userId']
    accessToken = data['accessToken']
    expiresIn = data['expiresIn']

    request = utils.updateSession(request, userId, expiresIn)

    if EventMember.eventMemberExist(userId):
        utils.updateToken(userId, accessToken)
    else:
        EventMember.createEventMember(userId, accessToken)

    return redirect(request.session['activeUrl'])

