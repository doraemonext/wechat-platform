# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, mixins
from rest_framework import status, parsers

from .serializer import MemberSerializer, GroupSerializer


class MemberListAPI(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    model = get_user_model()
    serializer_class = MemberSerializer

    def get(self, request, *args, **kwargs):
        return super(MemberListAPI, self).list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)
        groups = request.POST.getlist('groups[]')

        if serializer.is_valid():
            object = serializer.save()
            for group in groups:
                object.groups.add(Group.objects.get(pk=group))
            serializer = self.get_serializer(instance=object)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberDetailAPI(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    model = get_user_model()
    serializer_class = MemberSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.object = self.get_object_or_none()

        # Clear password
        data = request.DATA.copy()
        if data.get('password'):
            self.object.set_password(data.get('password'))
        del data['password']

        # Update user groups
        origin_groups = self.object.groups.all()
        for group in origin_groups:
            self.object.groups.remove(group)
        groups = data.getlist('groups[]')
        for group in groups:
            self.object.groups.add(Group.objects.get(pk=group))

        # Update user settings
        serializer = self.get_serializer(self.object, data=data, files=request.FILES, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.pre_save(serializer.object)
        except ValidationError as err:
            return Response(err.message_dict, status=status.HTTP_400_BAD_REQUEST)

        if self.object is None:
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        self.object = serializer.save(force_update=True)
        self.post_save(self.object, created=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class GroupListAPI(mixins.ListModelMixin, GenericAPIView):
    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    model = Group
    serializer_class = GroupSerializer

    def get(self, request, *args, **kwargs):
        return super(GroupListAPI, self).list(request, *args, **kwargs)