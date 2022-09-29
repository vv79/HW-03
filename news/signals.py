from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core import mail
from .models import Post, CategorySubscriber, article
from django.utils.text import Truncator
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import resolve_url


@receiver(post_save, sender=Post)
def send_subscribers_messages(sender, instance, created, **kwargs):
    categories = instance.categories

    category_subscribers = CategorySubscriber.objects.filter(type=instance.type, category__in=categories.all()).all()

    messages = []

    for category_subscriber in category_subscribers:
        user = category_subscriber.user
        if created:
            if instance.type == article:
                subject = f'New article "{instance.title}" published.'
            else:
                subject = f'New news "{instance.title}" published.'
        else:
            if instance.type == article:
                subject = f'Article changed "{instance.title}".'
            else:
                subject = f'News changed "{instance.title}".'

        context = {
            'username': user.username,
            'subject': subject,
            'content': Truncator(instance.content).chars(50),
            'url': resolve_url('article_detail', pk=instance.id) if instance.type == article else
            resolve_url('article_detail', pk=instance.id)
        }

        html_content = render_to_string('news/email/post_save_email.html', context)

        plain_message = strip_tags(html_content)

        message = mail.EmailMultiAlternatives(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email])
        message.attach_alternative(html_content, "text/html")

        messages.append(message)

    connection = mail.get_connection()
    connection.open()
    connection.send_messages(messages)
    connection.close()
