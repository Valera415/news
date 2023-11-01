from .models import News, Category
from .forms import NewsForm, RegistationForm, LoginForm, ContactForm

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'test.3228@yandex.ru',
                            ['yazenuk@gmail.com', ], fail_silently=True)
            if mail:
                messages.success(request, 'дурак!')
                return redirect('contact')
            else:
                messages.error(request,'Тупица')
        else:
            messages.error(request, 'мудила!')
    else:
        form = ContactForm()
    return render(request, 'appName/contact.html', context={'form': form})



def register(request):
    if request.method == 'POST':
        form = RegistationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Успешная регистрация')
            return redirect('email_confirmation')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = RegistationForm()
    return render(request, 'appName/register.html', context={'form': form})


def email_confirmation(request):
    return render(request, 'appName/email_confirmation.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home_page')
    else:
        form = LoginForm()

    return render(request, 'appName/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home_page')


class HomeNews(ListView):
    paginate_by = 2
    # добавим пагинатор, разбивка по 10 элементов на страничке,
    # в контекст все добавляется автоматически

    model = News
    template_name = 'appName/home_news_list.html'
#     переопределение базового шаблона, по дефолту ищется news_list (название модели_лист)

    context_object_name = 'news'
#     чтобы работать не с дефолтным объектом object_list

#     extra_context = {'title': 'Главная'}
#     доп данные, не рекомендуется использовать для динамических данных

    def get_context_data(self, *, object_list=None, **kwargs):
        # обращаемся к родителю и записываем контекст, чтобы добавить в него свою переменную с данными
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'

        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).order_by('-pk').select_related('news_category')
#     переопределяем метод получаения данных из бд


class NewsByCategory(ListView):
    paginate_by = 2
    model = News
    template_name = 'appName/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    # когда мы ищем новость, которой нет, мы ее не будем показывать, т.е. получил 404 ошибку, а не ошибку БД


    def get_queryset(self):
        return News.objects.filter(news_category_id=self.kwargs['category_id'], is_published=True).order_by('-pk').select_related('news_category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context




# def index(request):
#     news = News.objects.order_by('-created_at')
#     context = {'news': news, 'title': 'Новости'} #переменные в шаблон
#     return render(request, 'appName/index.html', context=context)


# def get_category(request, category_id):
#     news = News.objects.filter(news_category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     context = {'news': news, 'category': category, 'title': 'Новости'}
#     return render(request, 'appName/category.html', context=context)


# def get_news(request, news_id):
#     # news = News.objects.get(pk=news_id)
#     news = get_object_or_404(News, pk=news_id)
#     # чтобы при отсутствии pk получать не 5xx ошибку, а 404
#     return render(request, 'appName/news.html', context={'news': news})

class ViewNews(DetailView):
    model = News
    template_name = 'appName/news.html'

    def get(self, request, *args, **kwargs):
        # Получите объект новости
        news = self.get_object()

        # Увеличьте значение views на 1
        news.views = F('views') + 1

        # Сохраните объект новости обратно в базу данных
        news.save()

        return super().get(request, *args, **kwargs)

    # pk_url_kwarg = 'news_id'
#     можно крч так сделать, а можно и согласно конвенциям джанго


class CreateNews(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = NewsForm
    template_name = 'appName/add_news.html'
#     почему после заполнения формы происходит редирект на новость?
# потому что в модели определен get_absolute_url, он и редиректит (лучше его так и называть)


# def add_news(request):
#     # один и тот же реквест и на отправку формы и на получение страницы
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # news = News.objects.create(**form.cleaned_data)
#             # штуку сверху применяем для несвязанных с бд форм
#             # распаковали словарь (**) и добавили в бдху данные из формы (form.cleaned_data)
#             news = form.save()
#             # сохраняем епта
#             return redirect(news)
#     #     redirect перенаправляет нас,
#     else:
#         form = NewsForm()
#     return render(request, 'appName/add_news.html', context={'form': form})





