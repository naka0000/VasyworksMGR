"""
System Name: Vasyworks
Project Name: vacancy_mgr
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
import os
import datetime
from abc import ABCMeta, abstractmethod
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text, escape_uri_path
from django.utils.translation import gettext_lazy as _
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import views, login as auth_login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from dateutil.relativedelta import relativedelta
from PIL import Image
from lib.convert import *
from users.forms import CreateVacancyUserForm
from enums.models import VacancyLevel


class CreateVacancyUserView(views.FormView):
    """
    空室情報閲覧ユーザー作成
    """
    form_class = CreateVacancyUserForm
    template_name = 'users/create_vacancy_user.html'
    success_url = reverse_lazy('users_vacancy_user_list')
    user = None
    back_url = None
    target_user = None

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.user = self.request.user
        if not self.user:
            raise Http404
        if not self.user.is_company_admin:
            raise Http404

        self.back_url = self.request.GET.get('back_url', None)
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        url = super().get_success_url()
        if self.target_user:
            url = reverse_lazy('users_vacancy_user', kwargs={'idb64': self.target_user.idb64})
            back_url = xstr(reverse_lazy('users_vacancy_user_list'))
            url += '?back_url=' + back_url

        return url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        if self.back_url:
            context['back_url'] = self.back_url
            context['escaped_back_url'] = escape_uri_path(self.back_url)
        return context

    def form_valid(self, form):
        if settings.DEMO:
            messages.error(self.request, 'DEMOモードのため追加できません。')
        else:
            target_user = form.save(commit=False)
            target_user.display_name = '未入力'
            target_user.is_active = True
            target_user.is_staff = False
            target_user.level = VacancyLevel.objects.get(pk=3)  # 標準レベル3
            target_user.allow_org_image = False
            target_user.save()

            self.target_user = target_user
            messages.success(self.request, '追加しました。')

        return super().form_valid(form)
