from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

app_name='main'
urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('<int:pk>/', views.QuestionDetail.as_view(), name='detail'),
    path('answer/create/<int:question_id>/', login_required(views.answer_create, login_url='common:login'),name='answer_create'),
    path('question/create/',login_required(views.QuestionCreate.as_view(), login_url='common:login'), name='question_create'),
]
