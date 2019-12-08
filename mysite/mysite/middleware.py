import pytz

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from user.models import Profile


class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_anonymous:
            profile = Profile.objects.filter(user=request.user)

            if profile.exists():
                timezone.activate(profile.first().get_timezone())
