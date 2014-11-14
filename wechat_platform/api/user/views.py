# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status, parsers

from .serializer import LoginSerializer


class LoginAPI(APIView):
    permission_classes = (permissions.AllowAny, )
    parser_classes = (parsers.FormParser, )

    def get_redirect_url(self, next):
        if next:
            return next
        else:
            return reverse('admin:dashboard:dashboard')

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.DATA)
        if serializer.is_valid():
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            redirect_url = serializer.data.get('next')

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                response = {
                    'redirect_url': self.get_redirect_url(redirect_url),
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    'non_field_errors': [u'用户名或密码不正确'],
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPI(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        logout(request)
        response = {
            'redirect_url': reverse('admin:user:login'),
        }
        return Response(response, status=status.HTTP_200_OK)