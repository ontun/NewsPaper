from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from .models import *
from datetime import date, timedelta
from django.template import loader
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.template.loader import render_to_string


@shared_task
def weekly_category_send_mail():
    date_today = date.today()
    one_week_ago = date_today - timedelta(days=7)
    date_today = date_today.strftime('%Y-%m-%d')
    one_week_ago = one_week_ago.strftime('%Y-%m-%d')
    post_week = Post.objects.filter(post_dt__date__lte=date_today, post_dt__date__gt=one_week_ago)
    category = PostCategory.objects.filter(Q(post__in=post_week.values('id')))
    subscribers = UserCategory.objects.filter(Q(category__in=category.values('category')))
    article_url = []
    full_list = []
    for i in subscribers:
        user = i.user
        category_user = i.category
        new_articles = Post.objects.filter(
            post_dt__date__gte=one_week_ago,
            post_dt__date__lte=date_today,
            category=category_user
        )
        if new_articles:
            for j in new_articles:
                article_url.append(j)
                article_url.append('http://127.0.0.1:8000/' + reverse_lazy('news_one', args=[j.id]))
                full_list.append(article_url)
                article_url = []
            html_content = loader.render_to_string('account/email/weekly_articles.html', {
                'user': user,
                'category': category_user,
                'articles': full_list,
            })

            msg = EmailMultiAlternatives(
                subject=f'Посты недели любимой категорий',
                body=f'',  # это то же, что и message
                from_email='anton.alexandrovsky@yandex.ru',
                to=[user.email],  # это то же, что и recipients_list
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            msg.send()  # отсылаем


@shared_task
def send_mail_category(p_id):
    post = Post.objects.get(id=p_id)
    article_url = 'http://127.0.0.1:8000/' + reverse_lazy('news_one', args=[post.id])
    html_content = render_to_string(
        'appointment_created.html',
        {
            'post': post,
            'article_url': article_url,
        }
    )

    categor = PostCategory.objects.filter(post=post.id).values('category')
    mail_list = []
    for i in categor:
        mails = User.objects.filter(category=i['category']).values('email')
        for j in mails:
            mail_list.append(j['email'])
    msg = EmailMultiAlternatives(
        subject=f'{post.post_tittle}',
        body=post.post_text,  # это то же, что и message
        from_email='anton.alexandrovsky@yandex.ru',
        to=mail_list,  # это то же, что и recipients_list
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()  # отсылаем
