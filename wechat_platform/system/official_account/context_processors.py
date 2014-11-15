# -*- coding: utf-8 -*-

from system.official_account.models import OfficialAccount


def official_account(request):
    return {
        'official_account': OfficialAccount.manager.get_all()
    }