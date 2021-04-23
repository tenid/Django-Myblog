from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView

from Post.models import Post, Category


# 전체 게시글 보기
class Index(ListView):
    model = Post
    template_name = 'Post/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data()
        category_list = Category.objects.order_by('-created_at').all()
        post_list = Post.objects.all()
        context['category_list'] = category_list
        context['post_list'] = post_list
        context['page_title'] = '전체 글보기'
        return context

    def get_queryset(self):
        return self.model.objects.order_by('-created_at')


class CategoryDetail(ListView):
    model = Post

    def get(self, request, category_name):
        post_list = Post.objects.filter(category__ca_name=category_name)
        category_list = Category.objects.order_by('-created_at').all()
        context = {
            'category_list': category_list,
            'post_list': post_list
        }
        return render(request,'Post/test.html',context)





