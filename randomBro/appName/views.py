from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Category
from .forms import NewsForm


def index(request):
    news = News.objects.order_by('-created_at')
    context = {'news': news, 'title': 'Новости'} #переменные в шаблон
    return render(request, 'appName/index.html', context=context)


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





