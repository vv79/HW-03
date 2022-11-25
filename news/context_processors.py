import pytz
from django.conf import settings
from django.utils import timezone


def timezone_context(request):
    user_timezone = pytz.timezone(
        request.session.get('django_timezone') or settings.TIME_ZONE
    )

    current_time = timezone.now().astimezone(user_timezone)
    context = {
        'current_time': current_time,
        'timezones': pytz.common_timezones
    }

    return context

