"""instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_views
from webapp import views as webapp_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accounts_views.LoginView.as_view(), name="login"),
    path('create/', accounts_views.RegisterView.as_view(), name="register"),
    path('profile/<int:pk>/', accounts_views.UserDetailView.as_view(), name="profile"),
    path('profile/<int:pk>/followers/add', accounts_views.AddFollower.as_view(), name="add-follower"),
    path('posts/', webapp_views.IndexView.as_view(), name="index"),
    path("posts/new/", webapp_views.PostCreateView.as_view(), name="create_post"),
    path("posts/<int:pk>", webapp_views.PostDetailView.as_view(), name="detail_post"),
    path('likes_gateway/<int:pk>', webapp_views.LikeGateway.as_view(), name='like_gateway')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
