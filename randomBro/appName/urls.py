from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import *

urlpatterns = [
    # path('', index, name='home_page'),     #нейм - переменная для шаблонизатора, желательно указывать
    path('', HomeNews.as_view(), name='home_page'),
    # path('category/<int:category_id>/', get_category, name='category_page'), #можно менять путь
    path('category/<int:category_id>/', NewsByCategory.as_view(), name='category_page'),
    # path('news/<int:news_id>/', get_news, name='news_page'),
    path('news/<int:pk>/', ViewNews.as_view(), name='news_page'),
    # path('add-news/', add_news, name='add_news')
    path('add-news/', CreateNews.as_view(), name='add_news'),
    path("debug/", include("debug_toolbar.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
