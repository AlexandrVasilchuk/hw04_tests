from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class TestViewsPosts(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_name')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=TestViewsPosts.user,
            group=TestViewsPosts.group,
            text='Тестовый пост более 15 символов',
        )
        cls.extra_group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug_extra',
            description='Тестовое описание',
        )

    def setUp(self) -> None:
        self.authorized_client = Client()
        self.authorized_client.force_login(TestViewsPosts.user)

    def test_correct_templates(self) -> None:
        """Обращение по namespace:name возвращают правильный шаблон"""
        response_expected = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse(
                'posts:group_list', kwargs={'slug': 'test_slug'}
            ): 'posts/group_list.html',
            reverse(
                'posts:post_detail', kwargs={'pk': TestViewsPosts.post.pk}
            ): 'posts/post_detail.html',
            reverse(
                'posts:post_edit', kwargs={'pk': TestViewsPosts.post.pk}
            ): 'posts/create_post.html',
            reverse(
                'posts:profile', kwargs={'username': 'test_name'}
            ): 'posts/profile.html',
        }
        for response, value in response_expected.items():
            with self.subTest(value=value):
                self.assertTemplateUsed(
                    self.authorized_client.get(response),
                    value,
                    msg_prefix='Вызывается не тот шаблон!',
                )

    def correct_page_obj_first_obj(self, context) -> None:
        """Проверка соотвествия поста на странице"""
        fields_to_check = {
            context.author.username: TestViewsPosts.user.username,
            context.group.title: TestViewsPosts.group.title,
            context.text: TestViewsPosts.post.text,
        }
        for field, expected in fields_to_check.items():
            with self.subTest(expected=expected):
                self.assertEqual(field, expected)

    def test_index_context(self) -> None:
        """Шаблон index сформирован с правильным контекстом."""
        first_object = self.authorized_client.get(
            reverse('posts:index')
        ).context['page_obj'][0]

        self.correct_page_obj_first_obj(first_object)

    def test_group_list_context(self) -> None:
        """Проверка правильности контекста для group_list"""
        first_object = self.authorized_client.get(
            reverse(
                'posts:group_list', kwargs={'slug': TestViewsPosts.group.slug}
            )
        ).context['page_obj'][0]
        self.correct_page_obj_first_obj(first_object)
        self.assertEqual(
            self.authorized_client.get(
                reverse(
                    'posts:group_list',
                    kwargs={'slug': TestViewsPosts.group.slug},
                )
            ).context['group'],
            TestViewsPosts.group,
        )

    def test_profile_context(self) -> None:
        """Проверка правильности контекста для profile"""
        first_object = self.authorized_client.get(
            reverse(
                'posts:profile',
                kwargs={'username': TestViewsPosts.user.username},
            )
        ).context['page_obj'][0]
        self.correct_page_obj_first_obj(first_object)
        self.assertEqual(
            self.authorized_client.get(
                reverse(
                    'posts:profile',
                    kwargs={'username': TestViewsPosts.user.username},
                )
            ).context['author'],
            TestViewsPosts.user,
        )

    def test_post_detail(self) -> None:
        """Проверка правильности контекста для post_detail"""
        object = self.authorized_client.get(
            reverse(
                'posts:post_detail',
                kwargs={'pk': TestViewsPosts.post.pk},
            )
        ).context['post']
        self.assertEqual(object, TestViewsPosts.post)

    def correct_fields_post_form(self, form) -> None:
        """Проверка соответствия полей для формы"""
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = form.fields[value]
                self.assertIsInstance(form_field, expected)

    def test_create_post(self) -> None:
        """Проверка правильности контекста для create_post"""
        form = self.authorized_client.get(
            reverse('posts:post_create')
        ).context['form']
        self.correct_fields_post_form(form)

    def test_post_edit(self) -> None:
        """Проверка правильности контекста для post_edit"""
        form = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'pk': TestViewsPosts.post.pk})
        ).context['form']
        self.correct_fields_post_form(form)
        self.assertEqual(
            self.authorized_client.get(
                reverse(
                    'posts:post_edit', kwargs={'pk': TestViewsPosts.post.pk}
                )
            ).context['is_edit'],
            True,
        )

    def test_extra_check(self) -> None:
        """Проверка, что уникальный пост попадает на нужные страницы"""
        self.assertEqual(
            Post.objects.filter(pk=TestViewsPosts.post.pk).exists(), True
        )
        response = {
            'index': reverse('posts:index'),
            'profile': reverse(
                'posts:profile',
                kwargs={'username': TestViewsPosts.user.username},
            ),
            'group_list': reverse(
                'posts:group_list', kwargs={'slug': TestViewsPosts.group.slug}
            ),
        }
        for value in response.values():
            with self.subTest(value=value):
                self.assertEqual(
                    self.authorized_client.get(value).context['page_obj'][0],
                    TestViewsPosts.post,
                    msg=f'{value}',
                )

        self.assertEqual(
            len(
                (
                    self.authorized_client.get(
                        reverse(
                            'posts:group_list',
                            kwargs={'slug': TestViewsPosts.extra_group.slug},
                        ),
                    )
                ).context['page_obj']
            ),
            0,
        )
