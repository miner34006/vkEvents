# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponseRedirect


def authMiddleware(get_response):
    def middleware(request):
        path = request.path
        if path == reverse('redirect') or path == reverse('authorization'):
            return get_response(request)

        statement1 = 'userId' in request.session
        if not statement1:
            request.session['activeUrl'] = request.path
            return HttpResponseRedirect(reverse('redirect'))

        return get_response(request)
    return middleware
