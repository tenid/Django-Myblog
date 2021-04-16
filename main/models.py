from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    # null = True: null 값 허용
    # blank = True: form.is_vaild()에서 공백 값 허용
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject

    class Meta:
        db_table = 'question'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'answer'

# class Category(models.Model):
#     ca_id = models.AutoField(primary_key=True)
#     ca_name = models.CharField(max_length=45)
#
#     def __str__(self):
#         return self.ca_name
#
#     class Meta:
#         db_table = 'category'
#
#
#
#
# class Post(models.Model):
#     post_id = models.AutoField(primary_key=True)
#     post_title = models.CharField(max_length=45)
#     post_content = models.CharField(max_length=45)
#     created_at = models.DateTimeField()
#     post_img = models.CharField(max_length=45, blank=True, null=True)
#     category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
#
#     class Meta:
#         db_table = 'post'
