from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import *
from django.views.generic import ListView, DetailView, View

LOGIN_URL = 'common:login'


class index(ListView):
    model = Question
    template_name = 'main/index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(index, self).get_context_data()
        context['page_title'] = '질문과 답변'
        return context

    def get_queryset(self):
        return self.model.objects.order_by('-create_date')


class QuestionDetail(DetailView):
    model = Question
    template_name = 'main/question_detail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data()
        context['page_title'] = '질문내용 보기'
        return context


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
            return render(request, 'main/question_form.html', context)

    def get(self, request):
        form = QuestionForm()
        context = {'form': form}
        return render(request, 'main/question_form.html', context)


@login_required(login_url=LOGIN_URL)
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('main:detail', question_id=question_id)

    if request.method == "POST":
        form = Question(request.POST, instance=question)
        if form.is_vaild():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('main:detail', question_id=question_id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
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
