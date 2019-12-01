from django.forms import ModelForm

from ressource.models import Reservation


class AddRessourceForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ["title",  "ressource", "start_date", "end_date"]
