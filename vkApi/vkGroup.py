# -*- coding: utf-8 -*-

from vkApi.vkApi import getRequest


def getEvent(eventId: list) -> list:
    """
    Получение информации об инвенте по его id (с помощью vkApi)
    :param eventId: id ивента 
    :return: ивент с информацией о нем (id, name, image ...) 
    """
    parameters = {
        'group_id': eventId,
    }
    response = getRequest('groups.getById', parameters)
    return response[0]


def getEvents(eventIds: list) -> list:
    """
    Получение информации об инвентах по их id (с помощью vkApi)
    :param eventIds: список id ивентов
    :return: список ивентов с информацией о них (id, name, image ...) 
    """
    if len(eventIds) == 0:
        return []

    parameters = {
        'group_ids': ','.join([str(eventId) for eventId in eventIds]),
    }
    events = getRequest('groups.getById', parameters)
    return [{
            'event_id': event['id'],
            'event_name': event['name'],
            'event_image': event['photo_200']} for event in events]
