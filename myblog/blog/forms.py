"""Форми для блогу: реєстрація користувача, створення постів і коментарів."""

from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment


class BaseModelForm(forms.ModelForm):
    """Базова форма з методом збереження для авторизованих користувачів."""

    def __init__(self, *args, **kwargs):
        """Ініціалізація форми з урахуванням запиту.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """Збереження об'єкта з автоматичним встановленням автора.

        Args:
            commit (bool): Чи потрібно зберігати об'єкт у базу даних.

        Returns:
            Model instance: Збережений об'єкт моделі.
        """
        instance = super().save(commit=False)
        if self.request and self.request.user.is_authenticated:
            instance.author = self.request.user
        if commit:
            instance.save()
        return instance


class RegistrationForm(forms.ModelForm):
    """Форма для реєстрації нового користувача з підтвердженням паролю."""

    password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Пароль",
        help_text="Пароль має містити мінімум 8 символів"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        label="Підтвердження паролю",
    )

    class Meta:
        """Мета-клас для конфігурації форми реєстрації."""
        model = User
        fields = ['username', 'email']
        help_texts = {
            'username': "Логін має бути унікальним",
            'email': "Введіть дійсну email-адресу"
        }

    def clean_password_confirm(self):
        """Перевірка, що паролі збігаються.

        Returns:
            str: Підтверджений пароль.

        Raises:
            ValidationError: Якщо паролі не збігаються.
        """
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Паролі не збігаються')

        return password_confirm

    def save(self, commit=True):
        """Збереження користувача з хешуванням пароля.

        Args:
            commit (bool): Чи потрібно зберігати користувача у базу даних.

        Returns:
            User: Створений користувач.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class PostForm(BaseModelForm):
    """Форма для створення або редагування поста."""

    author_name = forms.CharField(
        max_length=100,
        required=False,
        label="Ім'я автора",
        widget=forms.TextInput(attrs={
            'placeholder': "Залиште пустим для анонімного поста",
            'class': 'form-control'
        }),
        help_text="Використовується, якщо ви не увійшли в систему"
    )

    class Meta:
        """Мета-клас для конфігурації форми поста."""
        model = Post
        fields = ['title', 'content', 'image', 'author_name']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'title': 'Заголовок поста',
            'content': 'Текст поста',
        }

    def __init__(self, *args, **kwargs):
        """Приховати поле author_name для авторизованих користувачів.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        if self.request and self.request.user.is_authenticated:
            self.fields.pop('author_name')

    def save(self, commit=True):
        """Збереження поста з обробкою анонімного автора.

        Args:
            commit (bool): Чи потрібно зберігати пост у базу даних.

        Returns:
            Post: Збережений пост.
        """
        instance = super().save(commit=False)
        if not instance.author and 'author_name' in self.cleaned_data:
            instance.author_name = self.cleaned_data['author_name']
        if commit:
            instance.save()
        return instance

    def clean(self):
        """Додаткова валідація даних форми."""
        cleaned_data = super().clean()
        # Тут можна додати додаткову валідацію
        return cleaned_data


class CommentForm(BaseModelForm):
    """Форма для додавання коментарів до постів."""

    author_name = forms.CharField(
        max_length=100,
        required=False,
        label="Ваше ім'я",
        widget=forms.TextInput(attrs={
            'placeholder': "Залиште пустим для анонімного коментаря",
            'class': 'form-control'
        }),
        help_text="Вкажіть, якщо бажаєте залишити коментар анонімно"
    )

    class Meta:
        """Мета-клас для конфігурації форми коментаря."""
        model = Comment
        fields = ['text', 'author_name']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ваш коментар...'
            }),
        }
        labels = {
            'text': 'Текст коментаря',
        }

    def __init__(self, *args, **kwargs):
        """Приховати поле author_name для авторизованих користувачів.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        if self.request and self.request.user.is_authenticated:
            self.fields.pop('author_name')

    def save(self, commit=True):
        """Збереження коментаря з обробкою анонімного автора.

        Args:
            commit (bool): Чи потрібно зберігати коментар у базу даних.

        Returns:
            Comment: Збережений коментар.
        """
        instance = super().save(commit=False)
        if not instance.author and 'author_name' in self.cleaned_data:
            instance.author_name = self.cleaned_data['author_name']
        if commit:
            instance.save()
        return instance

    def clean(self):
        """Додаткова валідація даних форми."""
        cleaned_data = super().clean()
        text = cleaned_data.get('text')

        if not text:
            raise forms.ValidationError({'text': 'Це поле обов\'язкове для заповнення'})

        # For anonymous users, require author_name
        if not self.request.user.is_authenticated and not cleaned_data.get('author_name'):
            raise forms.ValidationError({'author_name': 'Будь ласка, вкажіть ваше ім\'я'})

        return cleaned_data
