# -*- coding: utf-8 -*-

from meetings.models import ServiceUser, Event, EventMember, Choice


def addEventStatus(events, userId):
    """
    Добавление в словарь с ивентами нового ключа - статус ивента в бд
    :param events: список словарей с ивентами
    :param userId: id пользователя, владеющего ивентом
    :return: изменный список
    """
    for elem in events:
        try:
            if EventMember.eventMemberExists(userId, elem['event_id']):
                elem.update({'event_status': True})
            else:
                elem.update({'event_status': False})
        except Event.DoesNotExist:
            elem.update({'event_status': False})

    return events


def changeEventStatus(
        eventStatus: bool,
        eventId: int,
        userId: int) -> None:
    """
    Изменение статуса Event в БД
    :param eventStatus: статус (1 - добавить, 0 - удалить)
    :param eventId: event_id который необходимо добавить/удалить
    :param userId: serviceUser_id (активный пользователь)
    :return: None
    """
    if eventStatus:
        if not Event.eventExists(eventId):
            Event.createEvent(eventId)
        if not EventMember.eventMemberExists(userId, eventId):
            EventMember.createEventMember(userId, eventId)
    else:
        if Event.eventExists(eventId):
            eventMember = EventMember.getEventMember(userId, eventId)
            eventMember.delete()


def getRelatedMembers(userId: int) -> EventMember:
    """
    Получение списка EventMember для выдачи
    :param userId: id пользователя
    :return: список EventMember
    """
    user = ServiceUser.getServiceUser(userId)

    userEvents = EventMember.objects.filter(
        eventMember_owner=user
    ).values('eventMember_event')

    commonEventsMembers= EventMember.objects.filter(
        eventMember_event__in=userEvents
    ).exclude(eventMember_owner=user)

    ratedUsers = Choice.objects.filter(
        choiceList_whoChosen=user,
    ).values('choiceList_whomChosen__id')

    return commonEventsMembers\
        .exclude(id__in=ratedUsers)\
        .distinct('eventMember_owner')


def getSearchableEvent(userId, eventMemberId):
    # ивенты пользователя
    userEvents = EventMember.objects.filter(
        eventMember_owner=ServiceUser.getServiceUser(userId)
    ).values('eventMember_event')

    # EventMember с общей группой
    searchEventMembers = EventMember.objects.filter(
        eventMember_owner=ServiceUser.getServiceUser(eventMemberId),
        eventMember_event__in=userEvents,
    )

    finishEvent = None
    for eventMember in searchEventMembers:
        if Choice.objects.filter(
            choiceList_whoChosen=ServiceUser.getServiceUser(userId),
            choiceList_whomChosen=eventMember,
        ).exists():
            pass
        else:
            finishEvent = eventMember.eventMember_event
            break

    return finishEvent
