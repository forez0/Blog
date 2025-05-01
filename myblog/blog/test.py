"""Модуль з тестами для блогу Django."""

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from .models import Post, Comment


class BlogTests(TestCase):
    """Набір модульних тестів для перевірки функціоналу блогу."""

    def setUp(self):
        """Налаштовує початкові дані для тестів."""
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )
        self.client = Client()
        self.post = Post.objects.create(  # pylint: disable=no-member
            title='Test Post',
            content='This is a test post.',
            author=self.user
        )
        self.comment = Comment.objects.create(  # pylint: disable=no-member
            post=self.post,
            author=self.user,
            text='This is a test comment.'
        )

    def test_post_creation(self):
        """Перевірка створення публікації."""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'This is a test post.')
        self.assertEqual(self.post.author.username, 'testuser')

    def test_post_list_view(self):
        """Перевірка перегляду списку публікацій."""
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertTemplateUsed(response, 'blog/post_list.html')


    def test_post_create_view(self):
        """Перевірка створення нової публікації."""
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('post_create'), {
            'title': 'New Test Post',
            'content': 'This is a new test post.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Post.objects.filter(title='New Test Post').exists()  # pylint: disable=no-member
        )

    def test_comment_creation(self):
        """Перевірка створення коментаря."""
        self.assertEqual(self.comment.author.username, 'testuser')
        self.assertEqual(self.comment.text, 'This is a test comment.')
        self.assertEqual(self.comment.post.title, 'Test Post')

    def test_comment_display(self):
        """Перевірка відображення коментаря на сторінці публікації."""
        response = self.client.get(
            reverse('post_detail', args=[self.post.pk])
        )
        self.assertContains(response, 'This is a test comment.')

    def test_pagination(self):
        """Перевірка пагінації для списку публікацій."""
        for i in range(15):
            Post.objects.create(  # pylint: disable=no-member
                title=f'Post {i}',
                content=f'Content {i}',
                author=self.user
            )
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['posts'].has_other_pages())
        self.assertEqual(len(response.context['posts']), 5)

    def test_search_functionality(self):
        """Перевірка функціональності пошуку."""
        response = self.client.get(reverse('post_list') + '?q=Test')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_edit_view(self):
        """Перевірка редагування публікації."""
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('post_edit', args=[self.post.pk]),
            {
                'title': 'Updated Test Post',
                'content': 'This is an updated test post.'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Test Post')

    def test_post_delete_view(self):
        """Перевірка видалення публікації."""
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('post_delete', args=[self.post.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Post.objects.filter(pk=self.post.pk).exists()  # pylint: disable=no-member
        )

    def test_comment_without_text(self):
        """Перевірка створення коментаря без тексту."""
        self.client.login(username='testuser', password='12345')
        self.client.post(
            reverse('add_comment', args=[self.post.pk]),
            {'text': ''}
        )
        self.assertEqual(
            Comment.objects.count(), 1  # pylint: disable=no-member
        )

    def test_anonymous_post_with_name(self):
        """Перевірка створення публікації анонімним користувачем з ім'ям."""
        self.client.logout()
        self.client.post(reverse('post_create'), {
            'title': 'Anon Post',
            'content': 'Anonymous content',
            'author_name': 'AnonUser'
        })
        post = Post.objects.filter(title='Anon Post').first()  # pylint: disable=no-member
        self.assertEqual(post.author_name, 'AnonUser')

    def test_logged_in_post_sets_author_name(self):
        """Перевірка, що у публікації ставиться ім'я автора при авторизації."""
        self.client.login(username='testuser', password='12345')
        self.client.post(reverse('post_create'), {
            'title': 'Logged Post',
            'content': 'With user'
        })
        post = Post.objects.get(title='Logged Post')  # pylint: disable=no-member
        self.assertEqual(post.author_name, 'testuser')

    def test_anonymous_comment_with_name(self):
        """Перевірка створення коментаря анонімним користувачем з ім'ям."""
        self.client.logout()
        self.client.post(
            reverse('add_comment', args=[self.post.pk]),
            {
                'text': 'Anonymous comment',
                'author_name': 'Anon'
            }
        )
        self.assertEqual(
            Comment.objects.last().author_name, 'Anon'  # pylint: disable=no-member
        )

    def test_logged_in_comment_sets_author_name(self):
        """Перевірка, що у коментарі ставиться ім'я автора при авторизації."""
        self.client.login(username='testuser', password='12345')
        self.client.post(
            reverse('add_comment', args=[self.post.pk]),
            {'text': 'User comment'}
        )
        comment = Comment.objects.last()  # pylint: disable=no-member
        self.assertEqual(comment.author_name, 'testuser')

    def test_post_create_page_authenticated(self):
        """Перевірка доступності сторінки створення публікації."""
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 200)

    def test_post_create_page_anonymous_redirect(self):
        """Перевірка редіректу для анонімних користувачів."""
        self.client.logout()
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 302)

    def test_post_edit_page_requires_authentication(self):
        """Перевірка вимоги авторизації для редагування."""
        self.client.logout()
        response = self.client.get(
            reverse('post_edit', args=[self.post.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_post_delete_requires_login(self):
        """Перевірка вимоги авторизації для видалення."""
        self.client.logout()
        response = self.client.post(
            reverse('post_delete', args=[self.post.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Post.objects.filter(pk=self.post.pk).exists()  # pylint: disable=no-member
        )
