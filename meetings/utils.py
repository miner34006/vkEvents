# -*- coding: utf-8 -*-

from meetings.models import Event, EventMember, ChoiceList


def addEventStatus(events, userId):
    """
    Добавление в словарь с ивентами нового ключа - статус ивента в бд
    :param events: список словарей с ивентами
    :param userId: id пользователя, владеющего ивентом
    :return: изменный список
    """
    for elem in events:
        try:
            event = Event.getEvent(elem['event_id'])
            if event.event_members.filter(eventMember_id=userId).exists():
                elem.update({'event_status': True})
            else:
                elem.update({'event_status': False})
        except Event.DoesNotExist:
            elem.update({'event_status': False})

    return events


def changeEventStatus(
        eventStatus: bool,
        eventId: int,
        eventMember: EventMember) -> None:
    """
    Изменение статуса ивента в базе данных
    :param eventStatus: статус ивента (вкл. или выкл.)
    :param eventId: id ивента
    :param eventMember: кому принадлежит ивент
    :return: None
    """
    if eventStatus:
        if Event.eventExist(eventId):
            event = Event.getEvent(eventId)
        else:
            event = Event.createEvent(eventId)
        event.event_members.add(eventMember)
    else:
        if Event.eventExist(eventId):
            event = Event.getEvent(eventId)
            event.event_members.remove(eventMember)


def getRelatedMembers(userId: int) -> EventMember:
    """
    Получение списка уникальных пользователей для выдачи
    :param userId: id пользователя
    :return: список уникальных пользователей
    """
    user = EventMember.getEventMember(userId)

    # Выборка пользователей с общими для user'a группами
    relatedMembers = EventMember.objects.filter(
        event__in=user.event_set.all()
    ).exclude(
        eventMember_id=user.eventMember_id
    ).distinct()

    # Выборка пользователей, которых user уже оценил
    # userChoices = ChoiceList.objects.filter(
    #     choiceList_whoChoosen=user
    # )
    #
    # relatedMembers = relatedMembers.exclude(
    #     eventMember_id__in=userChoices.values('choiceList_whomChoosen'),
    # )

    return relatedMembers
