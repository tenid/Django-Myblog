from django.contrib import admin
from django.urls import path, include
from . import views


app_name='main'
urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('<int:pk>/', views.QuestionDetail.as_view(), name='detail'),
]
