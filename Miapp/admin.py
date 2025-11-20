from django.contrib import admin
from .models import Sala, Reserva , Estudiante


class SalAdmin(admin.ModelAdmin):
    list_display = ['NombreS', 'CapacidadM', 'Disponibilidad']

class EstAdmin(admin.ModelAdmin):
    list_display = ['Rut', 'NombreE', 'ApellidoE']

class ResAdmin(admin.ModelAdmin):
    list_display = ['Estudiante', 'Sala']

admin.site.register(Sala,SalAdmin)
admin.site.register(Reserva,ResAdmin)
admin.site.register(Estudiante,EstAdmin)