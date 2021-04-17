from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

app_name='main'
urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('<int:pk>/', views.QuestionDetail.as_view(), name='detail'),

    path('question/create/',login_required(views.QuestionCreate.as_view(), login_url='common:login'), name='question_create'),
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),

    path('answer/create/<int:question_id>/', login_required(views.answer_create, login_url='common:login'), name='answer_create'),
    path('answer/modify/<int:answer_id>', views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>', views.answer_delete, name='answer_delete'),


    path('comment/create/question/<int:question_id>/', views.comment_create_question, name='comment_create_question'),
    path('comment/modify/question/<int:comment_id>/', views.comment_modify_question, name='comment_modify_question'),
    path('comment/delete/question/<int:comment_id>/', views.comment_delete_question, name='comment_delete_question'),

]
