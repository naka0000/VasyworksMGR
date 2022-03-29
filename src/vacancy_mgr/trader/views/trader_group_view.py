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
from django.views.generic import TemplateView, FormView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from dateutil.relativedelta import relativedelta
from PIL import Image
from lib.convert import *
from lib.functions import *
from trader.models import TraderGroup
from trader.forms import TraderGroupForm


class TraderGroupView(UpdateView):
    """
    賃貸管理業者グループ
    """
    model = TraderGroup
    form_class = TraderGroupForm
    template_name = 'trader/trader_group.html'

    def __init__(self, **kwargs):
        self.user = None
        self.trader_group = None
        self.back_url = None

        super().__init__(**kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.user = self.request.user
        if not self.user:
            raise Http404

        self.back_url = self.request.GET.get('back_url')

        trader_group_id = 0
        try:
            idb64 = force_text(urlsafe_base64_decode(kwargs.get('idb64')))
            if idb64.isdecimal():
                trader_group_id = xint(idb64)
        except ValueError:
            raise Http404

        self.trader_group = get_object_or_404(TraderGroup, pk=trader_group_id)

        self.kwargs['pk'] = trader_group_id

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        if self.back_url:
            context['back_url'] = self.back_url
            context['escaped_back_url'] = escape_uri_path(self.back_url)
        context['trader_group'] = self.trader_group
        return context

    def form_valid(self, form):
        if settings.DEMO:
            messages.error(self.request, 'DEMOモードのため保存できません。')
            return redirect(self.get_success_url())
        else:
            form.save(commit=False)
            form.instance.updated_at = timezone.now()
            form.instance.updated_user = self.user
            form.instance.save()
            messages.success(self.request, '保存しました。')
            return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '保存に失敗しました。')
        return super().form_invalid(form)

    def get_success_url(self):
        url = reverse_lazy('trader_trader_group', kwargs={'idb64': self.trader_group.idb64})

        if self.back_url:
            url += '?back_url=' + escape_uri_path(self.back_url)

        return url
