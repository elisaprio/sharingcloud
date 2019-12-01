from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from ressource.forms import AddRessourceForm


class ManageReservations(LoginRequiredMixin, View):
    form_class = AddRessourceForm
    initial = {}
    template_name = "reservations.html"

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_reservation = form.save(commit=False)
            new_reservation.user = request.user
            new_reservation.save()
        else:
            errors = form.errors
            return JsonResponse({"errors": errors})
