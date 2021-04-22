
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    hit_count = models.PositiveIntegerField(default=0)
    create_date = models.DateTimeField()
    # null = True: null 값 허용
    # blank = True: form.is_vaild()에서 공백 값 허용
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')

    def __str__(self):
        return self.subject

    class Meta:
        db_table = 'question'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='author_answer')
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'answer'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)


class HitCount(models.Model):
    ip = models.CharField(max_length=15, default=None, null=True)
    question = models.ForeignKey(Question,default=None,null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, blank=True)



