from django.shortcuts import render
from django.views.generic import DetailView, ListView
from Post.models import Category
from QnA.models import Question

# Django model ORM로 Where절에 or문을 사용할 경우
from django.db.models import Q


class Index(ListView):
    model = Question
    template_name = 'QnA/index.html'
    paginate_by = 10

    # get 요청으로 보낸 데이터 처리
    def get(self, request, *args, **kwargs):
        self.kw = request.GET.get('kw')   # 검색 텍스트
        self.page = request.GET.get('page')  # 페이지 번호
        return super(Index, self).get(request, *args, **kwargs)

    # 추가로 필요한 데이터 처리
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data()
        category_list = Category.objects.order_by('-created_at').all()
        context['category_list'] = category_list
        context['page_title'] = '질문과 답변'
        return context

    # 쿼리 명령 처리
    def get_queryset(self):
        question_list = self.model.objects.order_by('-create_date')
        if self.kw:
            question_list = question_list.filter(
                Q(subject__icontains=self.kw) |  # 제목검색
                Q(content__icontains=self.kw) |  # 내용검색
                Q(author__username__icontains=self.kw) |  # 질문 글쓴이검색
                Q(answer__author__username__icontains=self.kw)  # 답변 글쓴이검색
            ).distinct()
        return question_list


class QuestionDetail(DetailView):
    model = Question
    template_name = 'QnA/question_detail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data()
        context['page_title'] = '질문내용 보기'
        return context
