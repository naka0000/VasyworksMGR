"""
System Name: Vasyworks
Project Name: vacancy_mgr
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
import urllib.parse
import django_filters
from django.shortcuts import render
from rest_framework import viewsets, filters
from django.db.models import Q
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text, escape_uri_path
from lib.convert import *
from company.models import Company
from api.api_helper import ApiHelper
from property.models import RoomPicture, Room
from api.serializers import RoomPictureSerializer


class RoomPictureViewSet(viewsets.ModelViewSet):
    """
    部屋画像
    """
    def list(self, request, *args, **kwargs):
        key = kwargs.get('key')
        if not ApiHelper.check_key(key):
            raise Exception

        id = kwargs.get('id')
        room = Room.objects.get(pk=id)

        self.queryset = RoomPicture.objects.filter(
            room=room,
            is_deleted=False,
        ).order_by('priority', 'picture_type__priority', 'id').all()
        self.serializer_class = RoomPictureSerializer

        return super().list(request, args, kwargs)
