# -*- coding: utf-8 -*-

from django.views.generic import DetailView

from system.library.news.models import LibraryNews


class NewsDetailView(DetailView):
    """
    图文展示页面
    """
    template_name = 'news/detail.html'
    model = LibraryNews
