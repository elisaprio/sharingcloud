from django.contrib import admin

# Register your models here.
from ressource.models import Ressource, RessourceType, Reservation


class ReservationAdmin(admin.ModelAdmin):
    model = Reservation
    list_display = ("title", "start_date", "end_date", "ressource")
    list_filter = ("ressource",)


class RessourceAdmin(admin.ModelAdmin):
    model = Ressource
    list_display = ("name", "type")
    list_filter = ("type",)


admin.site.register(Ressource, RessourceAdmin)
admin.site.register(RessourceType)
admin.site.register(Reservation, ReservationAdmin)
