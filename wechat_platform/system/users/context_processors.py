# -*- coding: utf-8 -*-


def current_info(request):
    return {
        'current_official_account': request.session.get('current_official_account', -1),
    }