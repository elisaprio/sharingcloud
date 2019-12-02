from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils import timezone
from django.utils.translation import gettext as _

from ressource.models import Reservation


class AddRessourceForm(ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    cancel = forms.BooleanField(widget=forms.HiddenInput, initial=False, required=False)

    def clean_start_date(self):
        now = timezone.now()
        start_date = self.cleaned_data.get("start_date")
        if start_date and start_date < now:
            return ValidationError(_('Invalid value'), code="invalid")
        return start_date

    def clean_end_date(self):
        now = timezone.now()
        end_date = self.cleaned_data.get("end_date")
        if end_date and end_date < now:
            return ValidationError(_('Invalid value'), code="invalid")
        return end_date

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        ressource = cleaned_data.get("ressource")
        if end_date <= start_date:
            self.add_error("end_date",(
                ValidationError(_("End date earlier than start date"), code="invalid")
            ))
        else:
            reservations_same_time = Reservation.objects.filter(ressource=ressource, start_date__lte=end_date, end_date__gte=start_date)
            if reservations_same_time.exists():
                self.add_error("start_date", (
                    ValidationError(_("Another reservation exists during this time range in the same room"), code="invalid")
                ))

    class Meta:
        model = Reservation
        fields = ["title",  "ressource", "start_date", "end_date", "id"]

    class Media:
        js = ("js/datetimepicker/jquery.datetimepicker.full.js",)
        css = {"all":("css/datetimepicker/jquery.datetimepicker.css",)}

