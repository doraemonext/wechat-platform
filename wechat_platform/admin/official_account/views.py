# -*- coding: utf-8 -*-

from django.views.generic import TemplateView

from lib.tools.mixin import LoginRequiredMixin


class OfficialAccountIndex(LoginRequiredMixin, TemplateView):
    template_name = 'official_account_index.html'

    def get_context_data(self, **kwargs):
        context = super(OfficialAccountIndex, self).get_context_data(**kwargs)
        return context
