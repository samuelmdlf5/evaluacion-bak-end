from django.db import models
from django.utils import timezone

class Sala(models.Model):
    NombreS = models.CharField(max_length=50)
    CapacidadM = models.PositiveIntegerField()
    Disponibilidad = models.BooleanField(default=True)

    def __str__(self):
        return self.NombreS

    def cupos_ocupados(self, momento=None):
        """Reservas activas en este instante."""
        if momento is None:
            momento = timezone.now()
        return Reserva.objects.filter(
            Sala=self,
            FechaHI__lte=momento,
            FechaHT__gte=momento
        ).count()

    def actualizar_disponibilidad(self, momento=None):
        """Actualiza el flag según cupos."""
        if momento is None:
            momento = timezone.now()
        self.Disponibilidad = self.cupos_ocupados(momento) < self.CapacidadM
        self.save(update_fields=['Disponibilidad'])
            
class Estudiante(models.Model):
    Rut = models.CharField(max_length=12, unique=True)
    NombreE = models.CharField(max_length=50)
    ApellidoE = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.NombreE} {self.ApellidoE} ({self.Rut})"

class Reserva(models.Model):
    Estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    Sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    FechaHI = models.DateTimeField(auto_now_add=True)  # Fecha y hora de inicio automática
    FechaHT = models.DateTimeField()  # Fecha y hora de término

    def __str__(self):
        return f"Reserva de {self.Estudiante} en {self.Sala}"
