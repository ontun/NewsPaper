import logging
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from ...models import *
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from datetime import date, timedelta
from django.template import loader
from django.db.models import Q
from django.urls import reverse_lazy
'''
logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
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
            print(full_list)
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


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="mon", hour="04", minute="20"),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не
            # надо.
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
'''