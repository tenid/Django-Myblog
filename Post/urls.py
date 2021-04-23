from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('Category/<str:category_name>/', views.CategoryList.as_view(), name='category-list'),
    path('<int:pk>/',views.PostDetail.as_view(), name='post-detail'),
    path('create/',views.PostCreate.as_view(), name='post-create'),

]
