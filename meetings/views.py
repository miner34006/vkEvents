# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from meetings.models import EventMember, Event, ChoiceList
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator


from vkApi.vkUser import VkUser, getUserEvents
from meetings.utils import changeEventStatus, addEventStatus, getRelatedMembers


def initialization(request):
    userId = request.session['userId']
    user = EventMember.getEventMember(userId)

    photo = VkUser(userId).getPhoto()
    if user.eventMember_image != photo:
        user.eventMember_image = photo
        user.save()

    template = 'meetings/__l_left_sidebar.html'
    context = {
        'option': None,
    }
    return render(request, template)


def showMembers(request):
    if request.method == 'POST':
        eventId = request.POST.get('eventId')
        userId = request.session['userId']
        eventMembers = Event.getEventMembers(eventId, userId)

        template = 'meetings/_w_template.html'
        context = {
            'eventMembers': eventMembers,
        }
        return render(request, template, context)


def relatedMembers(request):
    """
    Отображение страницы "Ищут пару"
    :param request: объект запроса
    :return: страница с пользователями, ищущими пару
    """
    userId = request.session['userId']
    eventMembers = getRelatedMembers(userId)

    if request.is_ajax():
        numPage = request.GET.get('numPage')

        paginator = Paginator(eventMembers, 14).page(numPage)

        template = 'meetings/infiniteScroll.html'
        context = {
            'eventMembers': paginator,
        }
        return render(request, template, context)

    paginator = Paginator(eventMembers, 14)
    template = 'meetings/_w_relatedMembers.html'
    context = {
        'eventMembers': paginator.page(1),
    }
    return render(request, template, context)


@require_http_methods(["POST"])
def rateUser(request):
    try:
        user = EventMember.getEventMember(request.session['userId'])
        eventMember = EventMember.getEventMember(request.POST.get('userId'))
        ChoiceList.makeChoice(
            choice=int(request.POST.get('value')),
            whoChoosen=user,
            whomChoosen=eventMember,
            event=None,
        )
        return HttpResponse("Like status changing is successful.")
    except:
        return HttpResponse("An error occurred while changing the like status.")


@require_http_methods(["GET"])
def getMemberInfo(request):
    userId = request.session['userId']
    searchUserId = request.GET.get('userId')

    eventMember = EventMember.getEventMember(searchUserId)

    try:
        choice = ChoiceList.objects.get(
            choiceList_whoChoosen=EventMember.getEventMember(userId),
            choiceList_whomChoosen=EventMember.objects.get(eventMember_id=searchUserId)
        ).choiceList_choice
    except ChoiceList.DoesNotExist:
        choice = None

    response = JsonResponse({
        'firstName': eventMember.eventMember_firstName,
        'lastName': eventMember.eventMember_lastName,
        'image': eventMember.eventMember_image,
        'choice': choice
    })
    return response


@require_http_methods(["POST"])
def changeEventStatus(request):
    """
    Обработка запроса на добавление или удаления события
    :param request: объект запроса
    :return: None
    """
    if request.POST.get('response') == '1':
        eventStatus = True
    else:
        eventStatus = False

    response = "Event status changing is successful."
    try:
        changeEventStatus(
            eventStatus,
            eventId=request.POST.get('eventId'),
            eventMember=EventMember.getEventMember(request.session['userId']),
        )
    except:
        response = "An error occurred while changing the event status."
    return HttpResponse(response)


def events(request):
    """
    Отображение событий пользователя
    :param request: объект запроса
    :return: страница с событиями пользователя
    """
    userId = request.session['userId']
    user = EventMember.getEventMember(userId)

    vkEvents = addEventStatus(getUserEvents(userId, user.eventMember_token), userId)
    defaultEvents = Event.getDefaultEvents(userId)

    template = 'meetings/_w_events.html'
    context = {
        'vkEvents': vkEvents,
        'defaultEvents': defaultEvents,
    }
    return render(request, template, context)
