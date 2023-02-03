from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        for txt in range(1, 14):
            Post.objects.create(
                author=PaginatorViewsTest.user,
                group=PaginatorViewsTest.group,
                text=f'Тестовый пост номер {txt}',
            )

    def setUp(self) -> None:
        self.authorized_client = Client()
        self.authorized_client.force_login(PaginatorViewsTest.user)

    def test_paginator_separator(self) -> None:
        """Проверка корректного разделения постов паджинатором"""
        response_values = {
            reverse('posts:index'): 10,
            reverse('posts:index') + '?page=2': 3,
            reverse('posts:group_list', kwargs={'slug': 'test_slug'}): 10,
            reverse('posts:group_list', kwargs={'slug': 'test_slug'})
            + '?page=2': 3,
            reverse('posts:profile', kwargs={'username': 'auth'}): 10,
            reverse('posts:profile', kwargs={'username': 'auth'})
            + '?page=2': 3,
        }
        for response, value in response_values.items():
            with self.subTest(value=value):
                self.assertEqual(
                    len(
                        (self.authorized_client.get(response)).context[
                            'page_obj'
                        ]
                    ),
                    value,
                )
