from django.db import models
from django.urls import reverse



class News(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок епта:')
    content = models.TextField(verbose_name='Текст новости:')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать?')
    news_category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория:') #внешний ключ

    def get_absolute_url(self):
        return reverse('news_page', kwargs={'news_id': self.pk})

    def __str__(self):
        return self.title    #то что будет напсано в возвращаемом объекте

    class Meta:     #подкласс для того чтобы изменить написание в админке лоол
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['created_at', 'title']  #сортировка, работает везде, нетолько в админке


class Category(models.Model):
    title = models.CharField(max_length=50, db_index=True)  #дб индекс - ускоряет поиск по этому полю хз

    def get_absolute_url(self): # конфенция приписывает называть так этот метод, а нужен он для ссылок красивых
        return reverse('category_page', kwargs={'category_id': self.pk})
    # первый параметр берем из юрлс название маршрута, второй параметр берем оттуда же

    def __str__(self):
        return self.title   #   а называется эта хуета строковое представление объекта
