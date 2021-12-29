from django.http import HttpResponse, response, HttpResponseRedirect, Http404
from django.template import loader
# render(requestオブジェクト, テンプレート名, <任意>辞書型)
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # template = loader.get_template('votes/index.html')
#     context  = {'latest_question_list': latest_question_list,}
#     # return HttpResponse(template.render(context, request))
#     return render(request, 'votes/index.html', context)

# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # # return HttpResponse("You're looking at question %s." % question_id)
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'votes/detail.html', {'question': question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'votes/results.html', {'question': question})

class IndexView(generic.ListView):
    template_name = 'votes/index.html'
    context_object_name = 'latest_qustion_list'

    def get_queryset(self):
        """Return the last five published questions."""
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'votes/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'votes/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'votes/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('votes:results', args=(question.id,)))