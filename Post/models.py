from django.contrib.auth.models import User
from django.db import models


# 카테고리 테이블(카테고리명)
from martor.models import MartorField


class Category(models.Model):
    ca_name = models.CharField(max_length=45)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.ca_name

    class Meta:
        # 테이블 이름
        db_table = 'category'


# 게시물 테이블(작성자, 제목, 작성일, 수정일, 카테고리명)
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=45)
    content = MartorField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField(null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        # 테이블 이름
        db_table = 'post'