from _datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views import View

from ressource.forms import AddRessourceForm
from ressource.models import Reservation
from user.models import Profile


class ManageReservations(LoginRequiredMixin, View):
    form_class = AddRessourceForm
    initial = {}
    template_name = "reservations/reservations.html"

    @staticmethod
    def get_cache_reservation(reservation_id):
        return cache.get(f"Reservation*[id={reservation_id}]")

    @staticmethod
    def set_cache_reservation(reservation_id):
        return cache.set(f"Reservation*[id={reservation_id}]", Reservation.objects.filter(id=reservation_id), 500)

    @staticmethod
    def delete_cache_reservation(reservation_id):
        return cache.delete(f"Reservation*[id={reservation_id}]")

    @staticmethod
    def get_profile(user):
        return cache.get_or_set(f"Profile*User[id={user.id}]", Profile.objects.get(user=user), 10000)

    def get(self, request, reservation_id=None):
        profile = self.get_profile(request.user)
        tz = profile.get_timezone()

        if not reservation_id:
            form = self.form_class(initial=self.initial)
            now = timezone.now()
            DEFAULT_TIMEOUT = 1800 #1800s == 30 minutes
            reservations_past = cache.get(f"ReservationPast*Profile[id={profile.id}]")
            if not reservations_past:
                reservations_past = Reservation.objects.filter(end_date__lte=now)
                if not request.user.is_superuser:
                    reservations_past = reservations_past.filter(profile=profile)
                cache.set(f"ReservationPast*Profile[id={profile.id}]", reservations_past, DEFAULT_TIMEOUT)

            reservations_present = cache.get(f"ReservationPresent*Profile[id={profile.id}]")
            if not reservations_present:
                reservations_present = Reservation.objects.filter(start_date__lte=now, end_date__gt=now)
                if not request.user.is_superuser:
                    reservations_present = reservations_present.filter(profile=profile)
                cache.set(f"ReservationPresent*Profile[id={profile.id}]", reservations_present, DEFAULT_TIMEOUT)

            reservations_future = cache.get(f"ReservationFuture*Profile[id={profile.id}]")
            if not reservations_future:
                reservations_future = Reservation.objects.filter(start_date__gte=now)
                if not request.user.is_superuser:
                    reservations_future = reservations_future.filter(profile=profile)
                cache.set(f"ReservationFuture*Profile[id={profile.id}]", reservations_future, DEFAULT_TIMEOUT)

            context = {
                "r_past": reservations_past,
                "r_present": reservations_present,
                "r_future": reservations_future,
                "form": form
            }
            return render(request, self.template_name, context)
        else:
            context = {}
            reservation = self.get_cache_reservation(reservation_id)
            if not reservation:
                reservation = self.set_cache_reservation(reservation_id)
            if reservation.exists():
                values = reservation.values("title", "start_date", "end_date", "ressource__id").first()
                context = {
                    "title": values["title"],
                    "start_date": datetime.strftime(values["start_date"].astimezone(tz), "%Y/%m/%d %H:%M"),
                    "end_date": datetime.strftime(values["end_date"].astimezone(tz), "%Y/%m/%d %H:%M"),
                    "ressource": values["ressource__id"]
                }
            return JsonResponse(context)

    def post(self, request):
        profile = self.get_profile(request.user)

        payload = request.POST.dict()
        payload.pop("csrfmiddlewaretoken")
        if payload.get("start_date"):
            payload["start_date"] = datetime.strptime(payload["start_date"], "%Y/%m/%d %H:%M")
        if payload.get("end_date"):
            payload["end_date"] = datetime.strptime(payload["end_date"], "%Y/%m/%d %H:%M")
        form = self.form_class(payload)
        if form.is_valid() or payload.get("cancel") == "True":
            if payload.get("id"):
                id = payload.pop("id")
                cancel = payload.pop("cancel", False)
                reservation = Reservation.objects.filter(id=id)
                if not request.user.is_superuser and request.user != reservation.first().profile.user:
                    return JsonResponse({"errors": {"title": _("You are not authorized to modify this reservation")}})
                if cancel == "True":
                    self.delete_cache_reservation(id)
                    cache.delete(f"ReservationPresent*Profile[id={profile.id}]")
                    cache.delete(f"ReservationFuture*Profile[id={profile.id}]")
                    reservation.delete()
                else:
                    self.set_cache_reservation(id)
                    reservation.update(**payload)
                return JsonResponse({})

            else:
                new_reservation = form.save(commit=False)
                new_reservation.profile = profile
                new_reservation.save()
                cache.delete(f"ReservationFuture*Profile[id={profile.id}]")
                return JsonResponse(
                    {"id": new_reservation.id, "title": new_reservation.title, "modifyButton": _("Modify"),
                     "cancelButton": _("Cancel")})
        else:
            errors = form.errors
            return JsonResponse({"errors": errors})
