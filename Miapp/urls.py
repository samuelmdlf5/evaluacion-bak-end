# reservas/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('',views.DispSal, name='salas'),  
    path("reserva/<int:id>/",views.reservar, name="reserva"),
    path("modoAdmin/", views.modoAdmin, name="modoAdmin"), 
]