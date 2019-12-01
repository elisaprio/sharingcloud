from django.contrib.auth.models import User
from django.db import models
import pytz

ALL_TIMEZONES = sorted((item, item) for item in pytz.all_timezones)


class MytimezoneTable(models.Model):
    tz_name = models.CharField(choices=ALL_TIMEZONES, max_length=64)

    def __str__(self):
        return self.tz_name


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    tz = models.ForeignKey("user.MytimezoneTable", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
