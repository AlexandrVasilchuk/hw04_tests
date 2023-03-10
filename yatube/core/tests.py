from django.test import TestCase


class ViewTestClass(TestCase):
    def test_error_page(self):
        """Проверка недоступности страницы с кодом 404"""
        self.assertEqual(self.client.get('/nonexist-page/').status_code, 404)

    def test_error_template(self):
        """Проверка использования верного шаблона"""
        self.assertTemplateUsed(
            self.client.get('/nonexists-page/'),
            'core/404.html',
        )
