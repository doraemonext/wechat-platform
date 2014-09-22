# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

from lib.tools.mixin import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
