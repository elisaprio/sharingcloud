from django import forms
from django.forms import ModelForm

from ressource.models import Reservation


class AddRessourceForm(ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    cancel = forms.BooleanField(widget=forms.HiddenInput, initial=False, required=False)

    class Meta:
        model = Reservation
        fields = ["title",  "ressource", "start_date", "end_date", "id"]

    class Media:
        js = ("js/datetimepicker/jquery.datetimepicker.full.js",)
        css = {"all":("css/datetimepicker/jquery.datetimepicker.css",)}

