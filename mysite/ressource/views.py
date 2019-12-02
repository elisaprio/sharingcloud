from _datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from ressource.forms import AddRessourceForm
from ressource.models import Reservation
from user.models import Profile


class ManageReservations(LoginRequiredMixin, View):
    form_class = AddRessourceForm
    initial = {}
    template_name = "reservations/reservations.html"

    def get(self, request, reservation_id=None):
        if not reservation_id:
            form = self.form_class(initial=self.initial)
            now = timezone.now()
            reservations_past = Reservation.objects.filter(end_date__lte=now)
            reservations_present = Reservation.objects.filter(start_date__lte=now, end_date__gt=now)
            reservations_future = Reservation.objects.filter(start_date__gte=now)

            if not request.user.is_superuser:
                reservations_past = reservations_past.filter(profile__user=request.user)
                reservations_present = reservations_present.filter(profile__user=request.user)
                reservations_future = reservations_future.filter(profile__user=request.user)

            context = {
                "r_past": reservations_past,
                "r_present": reservations_present,
                "r_future": reservations_future,
                "form": form
            }
            return render(request, self.template_name, context)
        else:
            context = {}
            reservation = Reservation.objects.filter(id=reservation_id)
            if reservation.exists():
                values = reservation.values("title", "start_date", "end_date", "ressource__id").first()
                context = {
                    "title": values["title"],
                    "start_date": datetime.strftime(values["start_date"], "%Y/%m/%d %H:%M"),
                    "end_date": datetime.strftime(values["end_date"], "%Y/%m/%d %H:%M"),
                    "ressource": values["ressource__id"]
                }
            return JsonResponse(context)

    def post(self, request):
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
                if cancel == "True":
                    reservation.delete()
                else:
                    reservation.update(**payload)
            else:
                new_reservation = form.save(commit=False)
                new_reservation.profile = Profile.objects.get(user=request.user)
                new_reservation.save()
            return JsonResponse({"id": new_reservation.id, "title": new_reservation.title})
        else:
            errors = form.errors
            return JsonResponse({"errors": errors})
