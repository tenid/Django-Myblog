from django.contrib import admin
from django.urls import path
from .views import base_views, question_views, answer_views, comment_views, vote_views
from django.contrib.auth.decorators import login_required

app_name='QnA'
urlpatterns = [
    # base_views.py
    path('', base_views.index.as_view(), name='index'),
    path('<int:pk>/', base_views.QuestionDetail.as_view(), name='detail'),

    # question_views.py
    path('question/create/',login_required(question_views.QuestionCreate.as_view(), login_url='common:login'), name='question_create'),
    path('question/modify/<int:question_id>/', question_views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', question_views.question_delete, name='question_delete'),

    # answer_views.py
    path('answer/create/<int:question_id>/', login_required(answer_views.answer_create, login_url='common:login'), name='answer_create'),
    path('answer/modify/<int:answer_id>', answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>', answer_views.answer_delete, name='answer_delete'),

    # comment_views.py
    path('comment/create/question/<int:question_id>/', comment_views.comment_create_question, name='comment_create_question'),
    path('comment/modify/question/<int:comment_id>/', comment_views.comment_modify_question, name='comment_modify_question'),
    path('comment/delete/question/<int:comment_id>/', comment_views.comment_delete_question, name='comment_delete_question'),
    path('comment/create/answer/<int:answer_id>/',comment_views.comment_create_answer, name='comment_create_answer'),
    path('comment/modify/answer/<int:comment_id>/',comment_views.comment_modify_answer, name='comment_modify_answer'),
    path('comment/delete/answer/<int:comment_id>/',comment_views.comment_delete_answer, name='comment_delete_answer'),

    # vote_views.py
    path('vote/question/<int:question_id>/', vote_views.vote_question, name='vote_question'),
    path('vote/answer/<int:answer_id>/', vote_views.vote_answer, name='vote_answer'),

]
