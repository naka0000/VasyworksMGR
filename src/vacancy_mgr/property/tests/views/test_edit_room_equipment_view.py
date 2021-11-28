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


class EditRoomEquipmentViewTest(TestCase):
    """
    部屋設備編集ビューのテスト
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

    def test_get_edit_room_equipment_view(self):
        url = reverse(
            'property_edit_room_equipment',
            args=[
                '5073ab83b3204160a947d1ab470a0b2b',     # 表示項目確認用マンション DEMO1号室
                6,           # 2口コンロ付
            ],
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        equipment = response.context['data']
        self.assertEqual(equipment.equipment.name, '2口コンロ付')

    def test_post_edit_room_equipment_view(self):
        url = reverse(
            'property_edit_room_equipment',
            args=[
                '5073ab83b3204160a947d1ab470a0b2b',     # 表示項目確認用マンション DEMO1号室
                6,           # 2口コンロ付
            ],
        )
        response = self.client.post(
            url,
            {
                'is_remained': 'off',
                'priority': '10',
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), '保存しました。')
