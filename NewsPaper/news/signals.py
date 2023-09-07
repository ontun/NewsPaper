from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives
from .models import *
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy


@receiver(pre_save, sender=Post)
def count_publication(instance, **kwargs):
    date_today = date.today().strftime('%Y-%m-%d')
    post = instance
    if Post.objects.filter(author=post.author, post_dt__date=date_today).count() >= 3:
        raise ValidationError('')


'''
@receiver(m2m_changed, sender=Post.category.through)
def send_mail_category(sender, instance, action, **kwargs):
    if action == 'post_add':
        post = instance
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
            subject=f'{instance.post_tittle}',
            body=instance.post_text,  # это то же, что и message
            from_email='anton.alexandrovsky@yandex.ru',
            to=mail_list,  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()  # отсылае '''
