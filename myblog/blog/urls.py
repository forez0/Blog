"""URL configuration for the blog application."""

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views
from .views import logout_view

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
