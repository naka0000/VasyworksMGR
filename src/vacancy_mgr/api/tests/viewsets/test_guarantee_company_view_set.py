"""
System Name: Vasyworks
Project Name: vacancy_mgr
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from unittest import TestCase
from django.test import Client
from django.urls import reverse
import warnings
from api.api_helper import ApiHelper


class GuaranteeCompanyViewSetTest(TestCase):
    """
    保証会社ビューセットのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.client = Client()

    def test_get_guarantee_company_view_set(self):
        url = reverse(
            'api_guarantee_company',
            args=[
                ApiHelper.get_key(),
            ],
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        guarantee_company = response.data[0]
        self.assertEqual(guarantee_company['name'], '全保連')
