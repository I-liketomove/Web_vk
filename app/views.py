from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.core.paginator import Paginator
from django.db.models import Count
from app.models import Question, Answer, Tag, User

# Create your views here.

QUESTIONS = [
        {
            'id': i,
            'title': f'Questions {i}',
            'content': f'№{i} Lorem ipsum dolor sit amet, consectetur adipiscing elit,'
                       f' sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. '
                       f'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
                       f' Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.'
                       f' Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id'
                       f' est laborum.'
        } for i in range(100)
    ]

def paginate(objects, page, per_page=5):
    otn = int(len(objects) + per_page - 1)//per_page
    if int(page) > otn:
        page = str(otn)
    if int(page) < 1:
        page = str(1)
    paginator = Paginator(objects, per_page)
    page_obj = paginator.get_page(page)
    return paginator.page(page), page_obj

def find_top_tags(objects, count_top = 7):
    # топ 7 тегов из базы данных (самых популярных)
    popular_tags = objects.annotate(num_questions=Count('questions')).order_by('-num_questions')[:count_top]
    return popular_tags

def find_best_members(objects, count_top = 5):
    # топ 5 людей из базы данных (с самым большим количеством правильных ответов)
    best_members = objects.best_users(amount=count_top)
    return best_members

def index(request):
    page = request.GET.get('page', 1) #http://127.0.0.1:8000/?page=2
    paginate_res, page_obj = paginate(Question.objects.all(), page)
    return render(request,'index.html', {'page_obj': page_obj, 'questions': paginate_res,\
                                         'popular_tags': find_top_tags(Tag.objects), 'best_members': find_best_members(User.objects)})


def question(request, question_id):
    page = request.GET.get('page', 1)
    question_item = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(what_question=question_item)
    paginate_res, page_obj = paginate(answers, page, 3)
    return render(request, 'question.html', {'question': question_item, 'page_obj': page_obj, 'answers': paginate_res,
                                             'popular_tags': find_top_tags(Tag.objects), 'best_members': find_best_members(User.objects)})


def hot(request):
    page = request.GET.get('page', 1)
    hot_questions = Question.objects.order_by('-like')[:10]
    paginate_res, page_obj = paginate(hot_questions, page)
    return render(request, 'hot.html', {'page_obj': page_obj, 'questions': paginate_res,\
                                        'popular_tags': find_top_tags(Tag.objects), 'best_members': find_best_members(User.objects)})

def settings(request):
    return render(request, 'settings.html', {'popular_tags': find_top_tags(Tag.objects), 'best_members': find_best_members(User.objects)})

def tag(request, tag_name):
    page = request.GET.get('page', 1)
    questions_with_tag = Question.objects.filter(tags__name=tag_name)
    paginate_res, page_obj = paginate(questions_with_tag, page)
    return render(request, 'tag.html', {'page_obj': page_obj, 'questions': paginate_res,\
                                        'tag_name': tag_name, 'popular_tags': find_top_tags(Tag.objects), 'best_members': find_best_members(User.objects)})

def signup(request):
    return render(request, 'signup.html', {'popular_tags': find_top_tags(Tag.objects), 'best_members': find_best_members(User.objects)})

def ask(request):
    return render(request, 'ask.html', {'popular_tags': find_top_tags(Tag.objects), 'best_members': find_best_members(User.objects)})

def login(request):
    return render(request, 'login.html', {'popular_tags': find_top_tags(Tag.objects), 'best_members': find_best_members(User.objects)})

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')