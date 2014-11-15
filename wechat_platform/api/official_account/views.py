# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, mixins
from rest_framework import status, parsers

from system.official_account.models import OfficialAccount
from .serializer import OfficialAccountSerializer


class OfficialAccountListAPI(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    model = OfficialAccount
    serializer_class = OfficialAccountSerializer
    paginate_by = None

    def get(self, request, *args, **kwargs):
        return super(OfficialAccountListAPI, self).list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(OfficialAccountListAPI, self).create(request, *args, **kwargs)


class OfficialAccountDetailAPI(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    model = OfficialAccount
    serializer_class = OfficialAccountSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class OfficialAccountSwitchAPI(APIView):
    """
    当前公众号切换 API
    """
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        official_account_id = request.POST.get('official_account')
        if not official_account_id:
            return Response(data={'official_account': [u'切换公众号不能为空', ]}, status=status.HTTP_400_BAD_REQUEST)

        if official_account_id == '0':  # 当 official_account_id 为 0 时代表进入管理模式
            request.session['current_official_account'] = 0
        else:
            try:
                official_account = OfficialAccount.objects.get(pk=official_account_id)
            except Exception:
                return Response(data={'official_account': [u'切换公众号非法', ]}, status=status.HTTP_400_BAD_REQUEST)
            request.session['current_official_account'] = official_account.pk
        return Response(data={'redirect_url': reverse('admin:dashboard:dashboard')})