from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('category/<str:category_name>/',views.CategoryDetail.as_view(), name='category-detail')
]
