from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.core.paginator import Paginator


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
    otn = int(len(objects))//per_page
    if int(page) > otn:
        page = str(otn)
    if int(page) < 1:
        page = str(1)
    paginator = Paginator(objects, per_page)
    page_obj = paginator.get_page(page)
    return paginator.page(page), page_obj

def index(request):
    page = request.GET.get('page', 1) #http://127.0.0.1:8000/?page=2
    paginate_res, page_obj = paginate(QUESTIONS, page)
    return render(request,'index.html', {'page_obj': page_obj, 'questions': paginate_res})

def question(request, question_id):
    item = QUESTIONS [question_id]
    return render(request, 'question.html', {'question' : item})

def hot(request):
    page = request.GET.get('page', 1) #http://127.0.0.1:8000/?page=2
    paginate_res, page_obj = paginate(QUESTIONS, page)
    return render(request, 'hot.html', {'page_obj': page_obj, 'questions': paginate_res})

def settings(request):
    return render(request, 'settings.html')

def tag(request):
    page=request.GET.get('page', 1)
    paginate_res, page_obj = paginate(QUESTIONS, page)
    return render(request,'tag.html', {'page_obj': page_obj, 'questions': paginate_res})

def signup(request):
    return render(request, 'signup.html')

def ask(request):
    return render(request, 'ask.html')

def login(request):
    return render(request, 'login.html')

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')