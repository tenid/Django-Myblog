from django.shortcuts import render
from django.views.generic import DetailView, ListView
from Post.models import Category
from QnA.models import Question, HitCount

# Django model ORM로 Where절에 or문을 사용할 경우, 총 갯수 파악
from django.db.models import Q, Count


class Index(ListView):
    model = Question
    template_name = 'QnA/index.html'
    paginate_by = 10

    # get 요청으로 보낸 데이터 처리
    def get(self, request, *args, **kwargs):
        self.kw = request.GET.get('kw', '')   # 검색 텍스트
        self.page = request.GET.get('page','1')  # 페이지 번호
        self.so = request.GET.get('so', 'recent')
        return super(Index, self).get(request, *args, **kwargs)

    # 추가로 필요한 데이터 처리
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data()
        category_list = Category.objects.order_by('-created_at').all()
        context['category_list'] = category_list
        context['page_title'] = '질문과 답변'
        context['so'] = self.so
        return context

    # 쿼리 명령 처리
    def get_queryset(self):
        # 추천순 정렬
        if self.so == 'recommend':
            question_list = self.model.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
        # 인기순 정렬(답글 수)
        elif self.so == 'popular':
            question_list = self.model.objects.annotate(num_answer=Count('answer')).order_by('-num_answer','-create_date')
        # 최근순 정렬
        else:
            question_list = self.model.objects.order_by('-create_date')
        # 검색어 필터
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

    # 사용자 ip 주소 식별
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def update_hitcount(self, ip, question):
        try:
            hits = HitCount.objects.get(ip=ip, question=question)
        except Exception as e:
            # 처음 질문을 조회한 경우
            print(e)
            hits = HitCount(ip=ip, question=question)
            question.hit_count = question.hit_count +1
            question.save()
            hits.save()
        else:
            # 조회한 기록이 있을 경우
            print(str(ip) + ' has already hit\n\n')

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data()
        context['page_title'] = '질문내용 보기'
        self.update_hitcount(self.get_client_ip(self.request),self.get_object())
        return context


