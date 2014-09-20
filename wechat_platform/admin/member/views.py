# -*- coding: utf-8 -*-

from django.views.generic import TemplateView

from lib.tools.mixin import LoginRequiredMixin


class MemberListView(LoginRequiredMixin, TemplateView):
    template_name = 'member_list.html'

    def get_context_data(self, **kwargs):
        context = super(MemberListView, self).get_context_data(**kwargs)
        return context
