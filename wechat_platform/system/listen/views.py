# -*- coding: utf-8 -*-

from django.views.generic import View


class ListenView(View):
    def post(self, request, *args, **kwargs):
        # 获取公众号ID
        #

        # 获取微信请求中的GET参数
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')

        # 获取请求的XML数据
        xml = request.POST.body

        # 获取当前用户的Session数据
        session = request.session

        return