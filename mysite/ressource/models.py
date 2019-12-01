from django.db import models


class RessourceType(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom")

    def __str__(self):
        return self.name


class Ressource(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nom")
    type = models.ForeignKey("ressource.RessourceType", null=True, on_delete=models.SET_NULL)
    localisation = models.CharField(max_length=200, verbose_name="Lieu")
    capacity = models.IntegerField(default=10, verbose_name="Capacité")

    def __str__(self):
        return self.name


class Reservation(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    start_date = models.DateTimeField(verbose_name="Date et heure de début")
    end_date = models.DateTimeField(verbose_name="Date et heure de fin")
    ressource = models.ForeignKey("ressource.Ressource", verbose_name="Ressource", null=True, on_delete=models.SET_NULL)
    profile = models.ForeignKey("user.Profile", verbose_name="Utilisateur", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title