from django.test import TestCase, Client
from django.urls import reverse
from .models import Post, Comment
from django.contrib.auth.models import User

class BlogTests(TestCase):
    def setUp(self):
        # Створюємо тестового користувача
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()

        # Створюємо тестовий пост
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.user  # Додано автора
        )

        # Створюємо тестовий коментар
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,  # Передаємо User-об'єкт
            text='This is a test comment.'
        )

    # Тест 1: Перевірка створення посту
    def test_post_creation(self):
        """
        Перевіряє, чи правильно створюється пост.
        Перевіряє, чи збігаються заголовок, вміст та автор посту.
        """
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'This is a test post.')
        self.assertEqual(self.post.author.username, 'testuser')

    # Тест 2: Перевірка відображення головної сторінки
    def test_post_list_view(self):
        """
        Перевіряє, чи головна сторінка відображається коректно.
        Перевіряє, чи статус відповіді 200, чи містить сторінка тестовий пост
        та чи використовується правильний шаблон.
        """
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertTemplateUsed(response, 'blog/post_list.html')

    # Тест 3: Перевірка відображення деталей посту
    def test_post_detail_view(self):
        """
        Перевіряє, чи сторінка деталей посту відображається коректно.
        Перевіряє, чи статус відповіді 200, чи містить сторінка заголовок
        та вміст посту, і чи використовується правильний шаблон.
        """
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'This is a test post.')
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    # Тест 4: Перевірка створення посту через форму
    def test_post_create_view(self):
        """
        Перевіряє, чи форма створення посту працює коректно.
        Перевіряє, чи після відправки форми відбувається редирект (статус 302)
        та чи новий пост з'являється в базі даних.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('post_create'), {
            'title': 'New Test Post',
            'content': 'This is a new test post.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='New Test Post').exists())

    # Тест 5: Перевірка додавання коментаря
    def test_comment_creation(self):
        """
        Перевіряє, чи правильно створюється коментар.
        Перевіряє, чи збігаються автор, текст коментаря та пост, до якого він належить.
        """
        self.assertEqual(self.comment.author.username, 'testuser')
        self.assertEqual(self.comment.text, 'This is a test comment.')
        self.assertEqual(self.comment.post.title, 'Test Post')

    # Тест 6: Перевірка відображення коментарів на сторінці посту
    def test_comment_display(self):
        """
        Перевіряє, чи коментар відображається на сторінці деталей посту.
        """
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertContains(response, 'This is a test comment.')

    # Тест 7: Перевірка пагінації
    def test_pagination(self):
        """
        Перевіряє, чи працює пагінація на головній сторінці.
        Створює 15 постів, перевіряє, чи сторінка містить пагінацію
        та чи на одній сторінці відображається 5 постів.
        """
        for i in range(15):
            Post.objects.create(
                title=f'Post {i}',
                content=f'Content {i}',
                author=self.user
            )
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['posts'].has_other_pages())  # Перевіряємо наявність пагінації
        self.assertEqual(len(response.context['posts']), 5)  # Перевіряємо кількість постів на сторінці

    # Тест 8: Перевірка пошуку
    def test_search_functionality(self):
        """
        Перевіряє, чи працює пошук постів.
        Перевіряє, чи сторінка пошуку містить тестовий пост.
        """
        response = self.client.get(reverse('post_list') + '?q=Test')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    # Тест 9: Перевірка редагування посту
    def test_post_edit_view(self):
        """
        Перевіряє, чи форма редагування посту працює коректно.
        Перевіряє, чи після відправки форми відбувається редирект (статус 302)
        та чи оновлюються дані посту в базі даних.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('post_edit', args=[self.post.pk]), {
            'title': 'Updated Test Post',
            'content': 'This is an updated test post.',
        })
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Test Post')

    # Тест 10: Перевірка видалення посту
    def test_post_delete_view(self):
        """
        Перевіряє, чи форма видалення посту працює коректно.
        Перевіряє, чи після видалення посту відбувається редирект (статус 302)
        та чи пост більше не існує в базі даних.
        """
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('post_delete', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

