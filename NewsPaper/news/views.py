from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import *
from .filters import NewsFilter
from .forms import NewsForm, ArticleForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ValidationError
from .tasks import send_mail_category
from django.core.cache import cache


@login_required
def subscribe(request, category_id):
    user = request.user
    # Проверяем, подписан ли пользователь уже на данную категорию
    if not UserCategory.objects.filter(user=user.id).exists():
        category = Category.objects.get(id=category_id)
        category.subscribers.add(user.id)
    return redirect('/search/')


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
        Author.objects.create(user_auth=user)
    return redirect('/')


class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'post_dt'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class NewsDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'news_one.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'news_one'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
            return obj


@method_decorator(login_required, name='dispatch')
class NewsSearch(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'post_dt'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news_search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


@method_decorator(login_required, name='dispatch')
class NewCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'new_create.html'

    def form_valid(self, form):
        try:
            post = form.save(commit=False)
            post.post_select = 1
            post.author = self.request.user.author
            v = super().form_valid(form)
            send_mail_category.delay(post.id)
            return v
        except ValidationError as e:
            # Обработка ValidationError
            # Здесь вы можете показать сообщение об ошибке пользователю
            return self.form_invalid(form)  # возвращаем невалидную форму


@method_decorator(login_required, name='dispatch')
class NewUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'new_edit.html'


@method_decorator(login_required, name='dispatch')
class NewDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_Post',)
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('news_list')


@method_decorator(login_required, name='dispatch')
class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = ArticleForm
    model = Post
    template_name = 'article_create.html'
    context_object_name = 'article_create'

    def form_valid(self, form):
        try:
            post = form.save(commit=False)
            post.post_select = 1
            post.author = self.request.user.author
            v = super().form_valid(form)
            send_mail_category.delay(post.id)
            return v
        except ValidationError as e:
            # Обработка ValidationError
            # Здесь вы можете показать сообщение об ошибке пользователю
            return self.form_invalid(form)  # возвращаем невалидную форму


@method_decorator(login_required, name='dispatch')
class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = ArticleForm
    model = Post
    template_name = 'article_edit.html'


@method_decorator(login_required, name='dispatch')
class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news_list')
