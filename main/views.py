
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import *
from django.views.generic import ListView, DetailView, View

# Create your views here.


# def index(request):
#     question_list = Question.objects.order_by('-create_date')
#     context = {
#         'page_title': '질문과 답변',
#         'question_list': question_list
#     }
#     return render(request, 'main/index.html', context)
#
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     context = {
#         'page_title': '질문 보기',
#         'question': question
#     }
#     return render(request, 'main/question_detail.html', context)

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


def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('main:detail', pk=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'main/question_detail.html', context)


class QuestionCreate(View):
    def post(self,request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('main:index')
        else:
            context = {'form': form}
            return render(request, 'main/question_form.html',context)

    def get(self, request):
        form = QuestionForm()
        context = {'form': form}
        return render(request, 'main/question_form.html',context)




