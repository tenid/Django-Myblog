
from django.views.generic import DetailView, ListView

from Post.models import Category
from QnA.models import Question


class index(ListView):
    model = Question
    template_name = 'QnA/index.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(index, self).get_context_data()
        category_list = Category.objects.order_by('-created_at').all()
        context['category_list'] = category_list
        context['page_title'] = '질문과 답변'
        return context

    def get_queryset(self):
        return self.model.objects.order_by('-create_date')


class QuestionDetail(DetailView):
    model = Question
    template_name = 'QnA/question_detail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data()
        context['page_title'] = '질문내용 보기'
        return context
