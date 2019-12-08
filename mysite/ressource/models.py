from django.db import models
from django.utils.translation import gettext_lazy as _


class RessourceType(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class Ressource(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    type = models.ForeignKey("ressource.RessourceType", null=True, on_delete=models.SET_NULL)
    localisation = models.CharField(max_length=200, verbose_name=_("Place"))
    capacity = models.IntegerField(default=10, verbose_name=_("Capacity"))

    def __str__(self):
        return self.localisation + " - " + self.name


class Reservation(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    start_date = models.DateTimeField(verbose_name=_("Start date and time"))
    end_date = models.DateTimeField(verbose_name=_("End date and time"))
    ressource = models.ForeignKey("ressource.Ressource", verbose_name=_("Ressource"), null=True, on_delete=models.SET_NULL)
    profile = models.ForeignKey("user.Profile", verbose_name=_("User"), on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title