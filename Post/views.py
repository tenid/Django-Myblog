from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView

from Post.forms import PostForm
from Post.models import Post, Category

import os, json, uuid
from blog.settings import LOGIN_URL

from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from martor.utils import LazyEncoder


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
            return render(request, 'Post/post_form.html', context)

    def get(self, request):
        form = PostForm()
        category_list = Category.objects.order_by('-created_at').all()
        context = {
            'form': form,
            'category_list': category_list}
        return render(request, 'Post/post_form.html', context)


@login_required(login_url=LOGIN_URL)
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('QnA:detail', pk=post_id)
    else:
        post.delete()
    return redirect('post:index')


@login_required(login_url=LOGIN_URL)
def post_modify(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author:
        # messages 같이 임의로 발생시킨 오류는 폼 필드와 관련이 없으므로 넌필드 오류에 해당된다
        messages.error(request, '수정권한이 없습니다')
        return redirect('post:post-detail', pk=post_id)

    else:
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.modified_at = timezone.now()
                post.save()
                return redirect('post:post-detail', pk=post_id)
        else:
            form = PostForm(instance=post)
        context = {'form': form}
        return render(request, 'post/post_form.html', context)


def markdown_uploader(request):
    """
    Makdown image upload for locale storage
    and represent as json to markdown editor.
    """
    if request.method == 'POST' and request.is_ajax():
        if 'markdown-image-upload' in request.FILES:
            image = request.FILES['markdown-image-upload']
            image_types = [
                'image/png', 'image/jpg',
                'image/jpeg', 'image/pjpeg', 'image/gif'
            ]
            if image.content_type not in image_types:
                data = json.dumps({
                    'status': 405,
                    'error': _('Bad image format.')
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            if image.size > settings.MAX_IMAGE_UPLOAD_SIZE:
                to_MB = settings.MAX_IMAGE_UPLOAD_SIZE / (1024 * 1024)
                data = json.dumps({
                    'status': 405,
                    'error': _('Maximum image file is %(size) MB.') % {'size': to_MB}
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            img_uuid = "{0}-{1}".format(uuid.uuid4().hex[:10], image.name.replace(' ', '-'))
            tmp_file = os.path.join(settings.MARTOR_UPLOAD_PATH, img_uuid)
            def_path = default_storage.save(tmp_file, ContentFile(image.read()))
            img_url = os.path.join(settings.MEDIA_URL, def_path)

            data = json.dumps({
                'status': 200,
                'link': img_url,
                'name': image.name
            })
            return HttpResponse(data, content_type='application/json')
        return HttpResponse(_('Invalid request!'))
    return HttpResponse(_('Invalid request!'))
