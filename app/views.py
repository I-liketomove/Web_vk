from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *

def paginate(objects, page, per_page=5):
    otn = int(len(objects) + per_page - 1) // per_page
    if int(page) > otn:
        page = str(otn)
    if int(page) < 1:
        page = str(1)
    # Явно упорядочиваем QuerySet по умолчанию по полю 'id'
    paginator = Paginator(objects, per_page)
    page_obj = paginator.get_page(page)
    return paginator.page(page), page_obj

def find_top_tags(objects, count_top=7):
    # топ 7 тегов из базы данных (самых популярных)
    popular_tags = objects.top_tags(count_top)
    return popular_tags

def find_best_members(objects, count_top=5):
    # топ 5 людей из базы данных (с самым большим количеством правильных ответов)
    best_members = objects.best_users(count_top)
    return best_members

def index(request):
    page = request.GET.get('page', 1)
    paginate_res, page_obj = paginate(Question.objects.all().order_by('id'), page)
    return render(request, 'index.html', {'page_obj': page_obj, 'questions': paginate_res,
                                           'popular_tags': find_top_tags(Tag.objects), 'best_members': find_best_members(User.objects)})

def question(request, question_id):
    page = request.GET.get('page', 1)
    question_item = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(what_question=question_item)
    paginate_res, page_obj = paginate(answers.order_by('id'), page, 3)
    return render(request, 'question.html', {'question': question_item, 'page_obj': page_obj, 'answers': paginate_res,
                                              'popular_tags': find_top_tags(Tag.objects), 'best_members': find_best_members(User.objects)})

def hot(request):
    page = request.GET.get('page', 1)
    hot_questions = Question.objects.hot_questions(amount=10)
    paginate_res, page_obj = paginate(hot_questions, page)
    return render(request, 'hot.html', {'page_obj': page_obj, 'questions': paginate_res,
                                         'popular_tags': find_top_tags(Tag.objects), 'best_members': find_best_members(User.objects)})

def new(request):
    page = request.GET.get('page', 1)
    new_questions = Question.objects.newest_questions(amount=10)
    paginate_res, page_obj = paginate(new_questions, page)
    return render(request, 'new.html', {'page_obj': page_obj, 'questions': paginate_res,
                                         'popular_tags': find_top_tags(Tag.objects), 'best_members': find_best_members(User.objects)})

def settings(request):
    return render(request, 'settings.html', {'popular_tags': find_top_tags(Tag.objects), 'best_members': find_best_members(User.objects)})

def tag(request, tag_name):
    page = request.GET.get('page', 1)
    questions_with_tag = Question.objects.filter(tags__name=tag_name)
    paginate_res, page_obj = paginate(questions_with_tag.order_by('id'), page)
    return render(request, 'tag.html', {'page_obj': page_obj, 'questions': paginate_res,
                                          'tag_name': tag_name, 'popular_tags': find_top_tags(Tag.objects), 'best_members': find_best_members(User.objects)})

#def signup(request):
#    return render(request, 'signup.html', {'popular_tags': find_top_tags(Tag.objects), 'best_members': find_best_members(User.objects)})

def ask(request):
    return render(request, 'ask.html', {'popular_tags': find_top_tags(Tag.objects), 'best_members': find_best_members(User.objects)})

#def login(request):
#    return render(request, 'login.html', {'popular_tags': find_top_tags(Tag.objects), 'best_members': find_best_members(User.objects)})

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Sign up")

        # Добавляем данные в контекст
        context['popular_tags'] = find_top_tags(Tag.objects)
        context['best_members'] = find_best_members(User.objects)

        # Объединяем контексты
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Login")

        # Добавляем данные в контекст
        context['popular_tags'] = find_top_tags(Tag.objects)
        context['best_members'] = find_best_members(User.objects)

        # Объединяем контексты
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('index')


def logout_user(request):
    logout(request)
    return redirect('login')