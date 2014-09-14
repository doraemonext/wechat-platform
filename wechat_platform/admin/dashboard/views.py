# -*- coding: utf-8 -*-

from django.http.response import HttpResponse
from django.views.generic import TemplateView


class DashboardView(TemplateView):
    template_name = 'dashboard.html'