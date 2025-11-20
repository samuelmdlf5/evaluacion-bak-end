from django import forms
from django.core.exceptions import ValidationError
from datetime import timedelta

class mostrar(forms.Form):
    RutE = forms.CharField(max_length=12, label="RUT")
    NombreE = forms.CharField(max_length=50, label="Nombre")
    ApellidoE = forms.CharField(max_length=50, label="Apellido")
    duracion = forms.DurationField(
        label="Duración",
        help_text="Formato HH:MM:SS (máx. 2 h)"
    )

    def clean_duracion(self):
        d = self.cleaned_data['duracion']
        if not timedelta(minutes=10) <= d <= timedelta(hours=2):
            raise ValidationError("Entre 10 min y 2 h.")
        return d