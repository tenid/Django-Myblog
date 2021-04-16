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
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),
    path('answer/modify/<int:answer_id>', views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>', views.answer_delete, name='answer_delete'),

]
