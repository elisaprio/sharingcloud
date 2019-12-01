from _datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
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

    def get(self, request):
        form = self.form_class(initial=self.initial)
        now = timezone.now()
        reservations_past = Reservation.objects.filter(end_date__lte=now, profile__user=request.user)
        reservations_present = Reservation.objects.filter(start_date__lte=now, end_date__gt=now, profile__user=request.user)
        reservations_future = Reservation.objects.filter(start_date__gte=now, profile__user=request.user)

        context = {
            "r_past": reservations_past,
            "r_present": reservations_present,
            "r_future": reservations_future,
            "form": form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        payload = request.POST.dict()
        if payload.get("start_date"):
            payload["start_date"] = datetime.strptime(payload["start_date"], '%Y/%m/%d %H:%M')
        if payload.get("end_date"):
            payload["end_date"] = datetime.strptime(payload["end_date"], '%Y/%m/%d %H:%M')
        form = self.form_class(payload)
        print(payload)
        if form.is_valid() or payload.get("cancel") == "True":
            if payload.get("id"):
                print("MODIFICATION")
                id = payload.pop("id")
                cancel = payload.pop("cancel", False)
                reservation = Reservation.objects.filter(id=id)
                if cancel == "True":
                    print("CANCEL")
                    reservation.delete()
                else:
                    reservation.update(**payload)
            else:
                print("CREATION")
                new_reservation = form.save(commit=False)
                new_reservation.profile = Profile.objects.get(user=request.user)
                new_reservation.save()
            return HttpResponse(status=200)
        else:
            print("INVALID FORM")
            print(form.errors)
            errors = form.errors
            return JsonResponse({"errors": errors})
