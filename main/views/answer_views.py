from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from blog.settings import LOGIN_URL
from main.forms import AnswerForm
from main.models import Question, Answer



@login_required(login_url=LOGIN_URL)
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.author = request.user
            answer.save()
            return redirect('main:detail', pk=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'main/question_detail.html', context)



@login_required(login_url=LOGIN_URL)
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('main:detail', pk=answer.question.id)

    else:
        if request.method == "POST":
            form = AnswerForm(request.POST, instance=answer)
            if form.is_valid():
                answer = form.save(commit=False)
                answer.modify_date = timezone.now()
                answer.save()
                return redirect('main:detail', pk=answer.question.id)
        else:
            form = AnswerForm(instance=answer)
        context = {'form': form}
        return render(request, 'main/answer_form.html', context)


@login_required(login_url=LOGIN_URL)
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정 권한이 없습니다.')
    else:
        answer.delete()
    return redirect('main:detail', pk=answer.question.id)
