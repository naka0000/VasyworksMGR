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


class ChangeUserPasswordViewTest(TestCase):
    """
    ユーザーパスワード変更ビューのテスト
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

    def test_get_change_user_password_view(self):
        url = reverse(
            'users_user_change_password',
            args=['Mw'],  # 管理 太郎
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        target_user = response.context['target_user']
        self.assertEqual(target_user.full_name, '管理 太郎')

    def test_post_change_user_password_view(self):
        url = reverse(
            'users_user_change_password',
            args=['Mw'],  # 管理 太郎
        )
        response = self.client.post(
            url,
            {
                'new_password1': 'vasyworks1234',
                'new_password2': 'vasyworks1234',
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'パスワードを変更しました。')
