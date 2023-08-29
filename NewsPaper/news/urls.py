from django.urls import path
# Импортируем созданное нами представление
from .views import (NewCreate, NewUpdate, NewDelete, ArticleCreate, ArticleUpdate, ArticleDelete,
                    NewsList, NewsDetail, NewsSearch, upgrade_me)

urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('', NewsList.as_view(), name='news_list'),
    path('search/', NewsSearch.as_view()),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    path('<int:pk>', NewsDetail.as_view(), name='news_one'),
    path('news/create/', NewCreate.as_view(), name='new_create'),
    path('news/<int:pk>/update/', NewUpdate.as_view(), name='new_update'),
    path('news/<int:pk>/delete/', NewDelete.as_view(), name='new_delete'),
    path('articles/create/', ArticleCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/update/', ArticleUpdate.as_view(), name='articles_update'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='articles_delete'),
    path('upgrade/', upgrade_me, name='upgrade')
]
