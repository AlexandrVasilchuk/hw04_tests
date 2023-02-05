from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Group, Post

User = get_user_model()


class TestPostForm(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.form = PostForm()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.text = 'Пост №1'
        cls.post = Post.objects.create(
            author=TestPostForm.user,
            text=TestPostForm.text,
        )

    def setUp(self) -> None:
        self.authorized_client = Client()
        self.authorized_client.force_login(TestPostForm.user)

    def test_newpost_form(self) -> None:
        """Проверка добавления записи в БД при отправке валидной формы"""
        amount_posts = Post.objects.count()
        self.assertEqual(Post.objects.count(), amount_posts)
        self.text = 'Тестовый пост'
        form_data = {
            'text': 'Тестовый пост',
            'group': TestPostForm.group.pk,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'), data=form_data, follow=True
        )
        self.assertEqual(Post.objects.filter(pk=response.context['post'].pk).exists(), True)
        self.assertRedirects(
            response,
            reverse(
                'posts:profile',
                kwargs={'username': TestPostForm.user.username},
            ),
        )
        self.assertEqual(Post.objects.count(), amount_posts + 1)

    def test_not_valid_form(self) -> None:
        """Проверка доступности страницы при отправке невалидной формы"""
        amount_posts = Post.objects.count()
        self.assertEqual(Post.objects.count(), amount_posts)
        form_data = {
            'text': '',
            'group': TestPostForm.group.pk,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'), data=form_data, follow=True
        )
        self.assertFormError(response, 'form', 'text', 'Обязательное поле.')
        self.assertEqual(Post.objects.filter(text='').exists(), False)
        self.assertEqual(Post.objects.count(), amount_posts)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_post(self) -> None:
        """Проверка работы формы при изменении поста"""
        form_data = {
            'text': 'Измененный пост',
            'group': '',
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'pk': TestPostForm.post.pk}),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'pk': TestPostForm.post.pk}),
        )
        self.assertEqual(
            Post.objects.get(pk=TestPostForm.post.pk).text, form_data['text']
        )
        self.assertNotEqual(
            Post.objects.get(pk=TestPostForm.post.pk).text, TestPostForm.text
        )
