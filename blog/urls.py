"""blog URL Configuration

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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from Post import views as mainView
from Post.views import markdown_uploader
from django.conf import settings

urlpatterns = [
    path('', mainView.Index.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('QnA/', include('QnA.urls')),
    # 로그인,로그아웃,회원가입
    path('common/',include('common.urls')),
    path('post/', include('Post.urls')),

    # martor
    path('martor/', include('martor.urls')),
    path('api/uploader/', markdown_uploader, name='markdown_uploader_page'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
