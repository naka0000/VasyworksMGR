"""
System Name: Vasyworks
Project Name: vacancy_mgr
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
"""
from unittest import TestCase
from django.test import Client
from django.urls import reverse
from django.db import transaction
import warnings


class UserViewTest(TestCase):
    """
    ユーザービューのテスト
    """
    def setUp(self):
        warnings.simplefilter('ignore')
        self.client = Client()
        if transaction.get_autocommit():
            transaction.set_autocommit(False)

        response = self.client.post(
            reverse('login'),
            {'username': 't-kanri', 'password': 'guest1234', },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        transaction.rollback()

    def test_get_user_view(self):
        url = reverse(
            'users_user',
            args=['Mw'],  # 管理 太郎
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        target_user = response.context['target_user']
        self.assertEqual(target_user.full_name, '管理 太郎')

    def test_post_user_view(self):
        url = reverse(
            'users_user',
            args=['Mw'],  # 管理 太郎
        )
        response = self.client.post(
            url,
            {
                'username': 'test-user',
                'last_name': 'テスト',
                'first_name': 'ユーザ編集',
                'is_active': 'on',
                'is_company_admin': 'on',
                'staff': '0',
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), '保存しました。')
