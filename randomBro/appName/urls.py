from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home_page'),     #нейм - переменная для шаблонизатора, желательно указывать
    path('category/<int:category_id>/', get_category, name='category_page'), #можно менять путь
    path('news/<int:news_id>/', get_news, name='news_page'),
    path('add-news/', add_news, name='add_news')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
