from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



class News(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок епта:')
    content = models.TextField(verbose_name='Текст новости:')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать?')
    news_category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория:') #внешний ключ
    views = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('news_page', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title    #то что будет напсано в возвращаемом объекте

    # описательный класс
    class Meta:     #подкласс для того чтобы изменить написание в админке лоол
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['created_at', 'title']  #порядок сортировки, работает везде, нетолько в админке


class Category(models.Model):
    title = models.CharField(max_length=50, db_index=True)  #дб индекс - ускоряет поиск по этому полю хз

    def get_absolute_url(self): # конфенция приписывает называть так этот метод, а нужен он для ссылок красивых
        return reverse('category_page', kwargs={'category_id': self.pk})
    # первый параметр берем из юрлс название маршрута, второй параметр берем оттуда же

    def __str__(self):
        return self.title   #   а называется эта хуета строковое представление объекта


class Comment(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    news = models.ForeignKey('News', on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-created_at']
