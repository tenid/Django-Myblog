from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'post'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('Category/<str:category_name>/', views.CategoryList.as_view(), name='category-list'),
    path('<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
    path('create/', login_required(views.PostCreate.as_view(), login_url='common:login'), name='post-create'),
    path('delete/<int:post_id>', views.post_delete, name='post-delete'),
    path('modify/<int:post_id>', views.post_modify, name='post-modify'),
]
