from django.urls import path

from ressource.views import ManageReservations

urlpatterns = [
    path("reservations/", ManageReservations.as_view(), name="reservations"),
    path("reservations/<int:reservation_id>/", ManageReservations.as_view(), name="reservations_with_id"),
]