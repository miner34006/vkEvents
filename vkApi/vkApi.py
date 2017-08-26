# -*- coding: utf-8 -*-

"""

:author: Polianok Bogdan

"""

import requests
import json

CLIENT_SECRET = 'rOvhkbKHGeP5I172l68U'

APP_ID = '6135462'

OAUTH_LINK = 'https://oauth.vk.com/access_token?client_id=%s&client_secret=%s' \
             '&redirect_uri=http://vkmeeting.ru/auth' \
             '&code=%s'

AUTH_LINK = 'https://oauth.vk.com/authorize?client_id=6135462&display=page&redirect_uri=http://vkmeeting.ru/auth&scope=groups&response_type=code&v=5.64'

# Link to API
LINK = "https://api.vk.com/method/"

# Secret token
TOKEN = 'bcf301e9bcf301e9bcf301e9b5bcae9f4fbbcf3bcf301e9e571871fde94e467be7f72ca'

# API version
V = '5.68'


def getRequest(method, parameters={}):
    """Get request from vk server
      
    :param get: method for vkApi
    :param parameters: parameters for vkApi
    
    :return: answer from vkApi
    
    """

    if not ('access_token' in parameters):
        parameters.update({'access_token': TOKEN, 'v': V})
    response = requests.get(LINK + method, parameters)
    data = json.loads(response.text)

    if 'response' in data:
        return data['response']
    elif 'error' in data:
        raise Warning(data['error'])
