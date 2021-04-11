from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import ListView,DetailView
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(index, self).get_context_data()
        context['page_title'] = '질문과 답변'
        return context

    def get_queryset(self):
        return Question.objects.order_by('-create_date')


class QuestionDetail(DetailView):
    model = Question
    template_name = 'main/question_detail.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data()
        context['page_title'] = '질문내용 보기'
        return context

