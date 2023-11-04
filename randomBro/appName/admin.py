from django.contrib import admin
from .models import News, Category, Comment


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'news_category', 'created_at', 'is_published']
    # крч класс для того чтобы изменить вид в админке
    list_display_links = ['title']  # что будет ссылкой кликабельной для открытия элемента таблиц
    search_fields = ['title', 'content', 'id']  # поля по которым можно будет делать поиск
    list_editable = ('is_published',)  # возможность тыкать и редактировать сразу в админке, не открывая
    list_filter = ('is_published', 'news_category')  # фильтр в админке


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['title']


# class CommentAdmin(admin.ModelAdmin):
#     list_display = ['id', 'author', 'news']

admin.site.register(News, NewsAdmin)  # чтобы в админке было мое приложение
admin.site.register(Category)
admin.site.register(Comment)

# порядок в скобках выше важен!
