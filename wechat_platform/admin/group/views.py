# -*- coding: utf-8 -*-

from django.views.generic import TemplateView

from lib.tools.mixin import LoginRequiredMixin


class GroupIndex(LoginRequiredMixin, TemplateView):
    template_name = 'group_index.html'

    def get_context_data(self, **kwargs):
        context = super(GroupIndex, self).get_context_data(**kwargs)
        return context
