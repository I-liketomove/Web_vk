from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator


# Create your views here.

QUESTIONS = [
        {
            'id': i,
            'title': f'Questions {i}',
            'content': f'Long Lorem Ipsum {i}'
        } for i in range (100)
    ]

def paginate(objects, page, per_page=15):
    otn=int(len(objects))//per_page
    if int(page) > otn:
        page = str(otn)
    if int(page) <1 :
        page=str(1)
    #добавить проверку на большее количество страниц
    paginator = Paginator(objects, per_page)
    return paginator.page(page)

def index(request):
    page=request.GET.get('page',1) #http://127.0.0.1:8000/?page=2
    return render(request,'index.html', {'questions' : paginate(QUESTIONS,page) })
#HttpResponse("Hello, world!"))

def question(request, question_id):
    item = QUESTIONS [question_id]
    return render(request, 'question.html', {'question' : item})

def hot(request):
    page=request.GET.get('page',1) #http://127.0.0.1:8000/?page=2
    return render(request, 'hot.html', {'questions' : paginate(QUESTIONS,page) })

def settings(request):
    return render(request, 'settings.html')

def tag(request):
    return render(request, 'tag.html')

def signup(request):
    return render(request, 'registration.html')

def ask(request):
    return render(request, 'ask.html')

def login(request):
    return render(request, 'login.html')
