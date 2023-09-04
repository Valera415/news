from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Category
from .forms import NewsForm
from django.views.generic import ListView


class HomeNews(ListView):
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
        context['title'] = 'Новости'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).order_by('-pk')
#     переопределяем метод получаения данных из бд


class NewsByCategory(ListView):
    model = News




# def index(request):
#     news = News.objects.order_by('-created_at')
#     context = {'news': news, 'title': 'Новости'} #переменные в шаблон
#     return render(request, 'appName/index.html', context=context)


def get_category(request, category_id):
    news = News.objects.filter(news_category_id=category_id)
    category = Category.objects.get(pk=category_id)
    context = {'news': news, 'category': category, 'title': 'Новости'}
    return render(request, 'appName/category.html', context=context)


def get_news(request, news_id):
    # news = News.objects.get(pk=news_id)
    news = get_object_or_404(News, pk=news_id)
    # чтобы при отсутствии pk получать не 5xx ошибку, а 404
    return render(request, 'appName/news.html', context={'news': news})


def add_news(request):
    # один и тот же реквест и на отправку формы и на получение страницы
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            # news = News.objects.create(**form.cleaned_data)
            # штуку сверху применяем для несвязанных с бд форм
            # распаковали словарь (**) и добавили в бдху данные из формы (form.cleaned_data)
            news = form.save()
            # сохраняем епта
            return redirect(news)
    #     redirect перенаправляет нас,
    else:
        form = NewsForm()
    return render(request, 'appName/add_news.html', context={'form': form})





