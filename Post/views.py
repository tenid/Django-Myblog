from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView

from Post.forms import PostForm
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


class CategoryList(ListView):
    model = Post

    def get(self, request, category_name):
        post_list = Post.objects.filter(category__ca_name=category_name)
        category_list = Category.objects.order_by('-created_at').all()
        context = {
            'category_list': category_list,
            'post_list': post_list
        }
        return render(request, 'Post/category.html', context)


class PostDetail(DetailView):
    model = Post
    template_name = 'Post/post_detail.html'
    context_object_name = 'post'


class PostCreate(View):
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_at = timezone.now()
            post.author = request.user
            post.save()
            return redirect('post:index')
        else:
            context = {'form': form}
            return render(request, 'Post/post_form.html.html', context)

    def get(self, request):
        form = PostForm()
        context = {'form': form}
        return render(request, 'Post/post_form.html', context)
