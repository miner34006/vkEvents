# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from meetings.models import ServiceUser, EventMember, Event, Choice
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator

from vkApi.vkUser import VkUser, getUserEvents, getOnlineStatus
from meetings import utils


def initialization(request):
    userId = request.session['userId']
    user = ServiceUser.getServiceUser(userId)

    photo = VkUser(userId).getPhoto()
    if user.serviceUser_image != photo:
        user.serviceUser_image = photo
        user.save()

    template = 'meetings/__l_left_sidebar.html'
    return render(request, template)


def relatedMembers(request):
    """
    relatedMembers view
    :param request: объект запроса
    (
        request.session['userId'] - serviceUser_id (активный пользователь).
    )
    :return: rendered page
    """
    # TODO кэширование eventMembers
    eventMembers = utils.getRelatedMembers(request.session['userId'])

    if request.is_ajax():
        template = 'meetings/infiniteScroll.html'
        context = {
            'eventMembers': Paginator(eventMembers, 32).page(request.GET.get('numPage')),
        }
        return render(request, template, context)

    template = 'meetings/_w_relatedMembers.html'
    context = {
        'eventMembers': Paginator(eventMembers, 32).page(1),
    }
    return render(request, template, context)


@require_http_methods(['POST'])
def rateUser(request):
    """
    Добавление оценки EventMember'у
    :param request: объект запроса
    (
        request.POST['value'] - код оценки (1 - да, 0 - нет);
        request.POST['eventMemberId'] - EventMember, которому дана оценка;
        request.POST['eventId'] - event_id в котором дана оценка;
        request.session['userId'] - serviceUser_id (активный пользователь).
    )
    :return: HttpResponse
    """
    try:
        Choice.makeChoice(
            choice=request.POST.get('value'),
            whoChosen=ServiceUser.getServiceUser(request.session['userId']),
            whomChosen=EventMember.getEventMember(
                request.POST.get('eventMemberId'),
                request.POST.get('eventId'),
            )
        )
        return HttpResponse('Like status changing is successful')
    except:
        # TODO добавить 500 ошибку
        raise Exception


@require_http_methods(['GET'])
def getMemberInfo(request):
    """
    Получение информации о EventMember'e
    :param request: объект запроса
    (
        request.GET['eventMemberId'] - EventMember_id пользователь для поиска;
        request.session['userId'] - serviceUser_id (активный пользователь).
    )
    :return: JsonResponse
    """
    userId = request.session['userId']
    eventMemberId = request.GET.get('eventMemberId')

    event = utils.getSearchableEvent(userId, eventMemberId)
    searchUser = ServiceUser.getServiceUser(eventMemberId)

    return JsonResponse({
        'userData': {
            'firstName': searchUser.serviceUser_firstName,
            'lastName': searchUser.serviceUser_lastName,
            'image': searchUser.serviceUser_image,
            # TODO добавить онлайн статус на сайте
            'onlineStatus': getOnlineStatus(eventMemberId),
        },
        'eventData': {
            'eventName': event.event_name,
            'eventId': event.event_id,
        },
        'choice': Choice.getChoice(
            whoChosen=ServiceUser.getServiceUser(userId),
            whomChosen=EventMember.getEventMember(eventMemberId, event.event_id)
        )
    })


@require_http_methods(['POST'])
def changeEventStatus(request):
    """
    Изменение статуса события для ServiceUser (добавление или удаление
    EventMember'a, связанного с ServiceUser)
    :param request:
    (
        request.POST['response'] - статус (1 - добавить, 0 - удалить);
        request.POST['eventId'] - event_id который необходимо добавить/удалить;
        request.session['userId'] - serviceUser_id (активный пользователь).
    )
    :return: HttpResponse
    """
    eventStatus = False
    if request.POST.get('response') == '1':
        eventStatus = True

    try:
        utils.changeEventStatus(
            eventStatus=eventStatus,
            eventId=request.POST.get('eventId'),
            userId=request.session['userId'],
        )
        return HttpResponse('Event status changing is successful')
    except:
        # TODO добавить 500 ошибку
        raise Exception


def events(request):
    """
    events view
    :param request: объект запроса
    (
        request.session['userId'] - serviceUser_id (активный пользователь).
    )
    :return: rendered page
    """
    userId = request.session['userId']
    user = ServiceUser.objects.get(serviceUser_id=userId)

    vkEvents = utils.addEventStatus(getUserEvents(userId, user.serviceUser_token), userId)
    defaultEvents = Event.getDefaultEvents(userId)

    template = 'meetings/_w_events.html'
    context = {
        'vkEvents': vkEvents,
        'defaultEvents': defaultEvents,
    }
    return render(request, template, context)
