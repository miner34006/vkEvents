# -*- coding: utf-8 -*-


def urlAdress(request):
    return {'url': request.resolver_match.url_name}