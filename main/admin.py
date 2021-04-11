from django.contrib import admin
from .models import *


# 검색 기능
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']


# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Category)
admin.site.register(Post)


