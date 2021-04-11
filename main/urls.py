from django.contrib import admin
from django.urls import path, include
from . import views


app_name='main'
urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('<int:pk>/', views.QuestionDetail.as_view(), name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create,name='answer_create'),
    path('question/create/',views.QuestionCreate.as_view(), name='question_create'),
]
