from django import template
from appName.models import Category

register = template.Library()


@register.simple_tag(name='get_list_categories')    #РУДИМЕНТ ЕБАНЫЙ
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('appName/list_categories.html') #шаблон для рендеринга
def show_categories(arg1='Hi'):
    categories = Category.objects.all()
    return {'categories': categories, 'arg1': arg1} #arg1 можно потом вывести

# суть в том, что мы рендерим шаблон 'appName/list_categories.html', отдаем в него данные
