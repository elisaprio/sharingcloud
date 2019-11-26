from django.contrib import admin

# Register your models here.
from ressource.models import Ressource, RessourceType, Reservation

admin.site.register(Ressource)
admin.site.register(RessourceType)
admin.site.register(Reservation)
