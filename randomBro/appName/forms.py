from django import forms
from .models import Category, News


# class NewsForm(forms.Form):
    # lable - заголовок, required - обязательный ли пункт в форме, initial - начальное значение
    # ПРОЧИТАТЬ ПРО ФОРМЫ И АТРИБУТЫ
    #
    # title = forms.CharField(max_length=150, label='Заголовок',
    #                         widget=forms.TextInput(attrs={"class": 'form-control'}))
    #
    # content = forms.CharField(label='Контент', required=False, widget=forms.Textarea(attrs={
    #     "class": 'form-control',
    #     "rows": 10
    # }))
    #
    # is_published = forms.BooleanField(label='Опубликовать?', required=False, initial=True)
    # news_category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='', widget=forms.Select(attrs={"class": "form-control"}))


# вариант выше ручной, ниже - автоматический

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        # fields = '__all__'
# все поля, но это не рекомендуемный вариант
        fields = ['title', 'content', 'is_published', 'news_category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }