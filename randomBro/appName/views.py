from .models import News, Category, Comment
from .forms import NewsForm, RegistationForm, LoginForm, ContactForm, CommentForm
from .tokens import account_activation_token

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.core.mail import send_mail
from django.http import HttpResponseRedirect


from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.urls import reverse


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
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            email_confirmation(request, user, form.cleaned_data.get('email'))
            return redirect('home_page')

        else:
            messages.error(request, 'Ошибка регистрации')

    else:
        form = RegistationForm()
    return render(request, 'appName/register.html', context={'form': form})


def email_confirmation(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('appName/email_confirmation.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(mail_subject, message, to=[to_email])

    if email.send():
        messages.success(request, f'Бро {user}, заходи в {to_email} и подтверждай почту')

    else:
        messages.error(request, '-')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')

    return redirect('home_page')

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

class ViewNews(DetailView, FormMixin):
    model = News
    template_name = 'appName/news.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()  # Добавьте форму в контекст
        comments = Comment.objects.filter(news=self.object)
        context['comments'] = comments
        return context

    def form_valid(self, form):
        # Действия после успешной отправки формы
        # return super().form_valid(form)
        return redirect('news/<int:pk>/')

    def form_invalid(self, form):
        # Действия в случае недопустимых данных формы
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('news_page', kwargs={'pk': self.object.pk})

    def get(self, request, *args, **kwargs):
        # Получите объект новости
        news = self.get_object()

        # Увеличьте значение views на 1
        news.views = F('views') + 1

        # Сохраните объект новости обратно в базу данных
        news.save()

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comm = form.save(commit=False)
            comm.author = request.user
            comm.news = self.object
            comm.save()
            return HttpResponseRedirect(self.get_success_url())



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





