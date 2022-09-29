import logging
from ...models import Post, CategorySubscriber, article
from datetime import date, timedelta
from django.core import mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

logger = logging.getLogger(__name__)


def send_subscribers_messages():
    messages = []
    end_date = date.today()
    start_date = end_date - timedelta(days=7)

    for category_subscriber in CategorySubscriber.objects.all():
        user = category_subscriber.user
        category = category_subscriber.category
        posts = Post.objects.filter(
            type=category_subscriber.type,
            categories__in=[category.id],
            date_created__range=[start_date, end_date]
        )

        if len(posts) > 0:
            if category_subscriber.type == article:
                subject = f'Last week articles in "{category.name}"'
            else:
                subject = f'Last week news in "{category.name}"'

            context = {
                'username': user.username,
                'subject': subject,
                'posts': posts,
                'route': 'article_detail' if category_subscriber.type == article else 'news_detail'
            }

            html_content = render_to_string('news/email/apscheduler_email.html', context)
            plain_message = strip_tags(html_content)

            message = mail.EmailMultiAlternatives(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email])
            message.attach_alternative(html_content, "text/html")

            messages.append(message)

    connection = mail.get_connection()
    connection.open()
    connection.send_messages(messages)
    connection.close()


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added hourly job: 'delete_old_job_executions'."
        )

        scheduler.add_job(
            send_subscribers_messages,
            trigger=CronTrigger(day_of_week="sat", hour="00", minute="00"),
            id="send_subscribers_messages",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'send_subscribers_messages'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
