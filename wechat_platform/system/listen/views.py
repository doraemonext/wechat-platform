# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponseBadRequest
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError

from system.core.exceptions import WechatException
from system.core.control import ControlCenter
from system.official_account.models import OfficialAccount


class ListenView(View):
    def post(self, request, *args, **kwargs):
        # 获取公众号 ID
        iden = request.GET.get('iden')
        # 获取微信请求中的 GET 参数
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        # 获取请求的 XML 数据
        xml = request.body

        # 根据 iden 获取对应的公众账号
        try:
            official_account = OfficialAccount.objects.get(iden=iden)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest('Invalid IDEN Parameter')

        # 对请求进行校验并预解析数据，并转发数据给控制中心获得响应数据
        wechat_instance = WechatBasic(
            token=official_account.token,
            appid=official_account.appid,
            appsecret=official_account.appsecret
        )
        if not wechat_instance.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('Invalid Verify Parameter')
        try:
            wechat_instance.parse_data(data=xml)
            return ControlCenter(
                official_account=official_account,
                wechat_instance=wechat_instance
            ).response
        except ParseError:
            return HttpResponseBadRequest('Invalid XML Data')
        except WechatException:
            return HttpResponseBadRequest('Internal Error')

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(ListenView, self).dispatch(*args, **kwargs)