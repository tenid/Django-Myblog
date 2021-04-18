from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.views import View

from blog.settings import LOGIN_URL
from main.forms import QuestionForm
from main.models import Question


class QuestionCreate(View):
    def post(self, request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.author = request.user
            question.save()
            return redirect('main:index')
        else:
            context = {'form': form}
            print("QuestionCreate by post")
            return render(request, 'main/question_form.html', context)

    def get(self, request):
        form = QuestionForm()
        context = {'form': form}
        print("QuestionCreate by get")
        return render(request, 'main/question_form.html', context)


@login_required(login_url=LOGIN_URL)
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        # messages 같이 임의로 발생시킨 오류는 폼 필드와 관련이 없으므로 넌필드 오류에 해당된다
        messages.error(request, '수정권한이 없습니다')
        return redirect('main:detail', pk=question_id)

    else:
        if request.method == "POST":
            form = QuestionForm(request.POST, instance=question)
            if form.is_valid():
                question = form.save(commit=False)
                question.modify_date = timezone.now()
                question.save()
                return redirect('main:detail', pk=question_id)
        else:
            form = QuestionForm(instance=question)
        context = {'form': form}
        print("QuestionModify by get")
        return render(request, 'main/question_form.html', context)


@login_required(login_url=LOGIN_URL)
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('main:detail', pk=question_id)
    else:
        question.delete()
    return redirect('main:index')




