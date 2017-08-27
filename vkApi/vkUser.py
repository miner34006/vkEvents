# -*- coding: utf-8 -*-

"""

:author: Polianok Bogdan

"""

from vkApi.vkApi import getRequest, TOKEN

def getPhotos(ids):
    fields = 'about, bdate, photo_max, sex'
    parameters = {
        'user_ids': ids,
        'fields': fields,
    }
    return getRequest('users.get', parameters)


def getPhoto(id):
    fields = 'photo_max'
    parameters = {
        'user_id': id,
        'fields': fields,
    }
    return getRequest('users.get', parameters)[0]['photo_max']


def getOnlineStatus(id):
    fields = 'online, last_seen'
    parameters = {
        'user_id': id,
        'fields': fields,
    }
    response = getRequest('users.get', parameters)[0]
    if response['online'] == 1:
        return 'Online'
    else:
        return "Offline"


def getUserEvents(userId: str, token: str) -> list:
    """
    Получение id ивентов пользователя
    :param userId: id пользователя
    :param token: токен пользователя
    :return: список id ивентов
    """
    parameters = {
        'user_id': userId,
        'filter': 'events',
        'access_token': token,
        'extended': '1',
    }
    response = getRequest('groups.get', parameters)

    events = [{
        'event_id': event['gid'],
        'event_name': event['name'],
        'event_image': event['photo_big']} for event in response[1:]]

    return events


class VkUser:
    """Vk user model"""

    def __init__(self, id, token=TOKEN):
        """
        
        :param id: user id
        
        """
        self.id = id
        self.token = token

        fields = 'about, bdate, photo_200, sex'
        parameters = {
        'user_ids': id,
        'fields': fields,
        }
        self.user = getRequest('users.get', parameters)[0]

    def getFirstName(self):
        """ get user's first name
        
        :return: user's first name
        
        """
        return self.user['first_name']

    def getLastName(self):
        """ get user's last name
        
        :return: user's last name
        
        """
        return self.user['last_name']

    def getPhoto(self):
        """ get user's main photo
        
        :return: user's photo
        
        """
        return self.user['photo_200']

    def getBirthday(self):
        """ get user's birthday date
        
        :return: user's birthday date
        
        """
        return self.user['bdate']

    def getEventIds(self):
        """ get user's events
        
        :return: user's events
        
        """
        parameters = {
            'user_id': self.id,
            'filter': 'events',
            'access_token': self.token,
        }
        return getRequest('groups.get', parameters)
