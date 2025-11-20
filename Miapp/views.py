from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Sala, Estudiante, Reserva
from .forms import mostrar

def DispSal(request):
    lista = Sala.objects.all()
    for s in lista:
        s.actualizar_disponibilidad()
    return render(request, 'paginaP.html', {'salas': lista})

def modoAdmin(request):
    if request.method == "POST":
        acc = request.POST.get("action")

        if acc == "crear_sala":
            Sala.objects.create(NombreS=request.POST.get("nombre_sala"),
                                CapacidadM=request.POST.get("capacidad"))
        elif acc == "editar_sala":
            obj = Sala.objects.get(id=request.POST.get("sala_id"))
            obj.NombreS = request.POST.get("nombre_sala_edit")
            obj.CapacidadM = request.POST.get("capacidad_edit")
            obj.save()
        elif acc == "eliminar_sala":
            Sala.objects.filter(id=request.POST.get("sala_id")).delete()

        elif acc == "crear_estudiante":
            Estudiante.objects.create(Rut=request.POST.get("rut"),
                                      NombreE=request.POST.get("nombre"),
                                      ApellidoE=request.POST.get("apellido"))
        elif acc == "editar_estudiante":
            obj = Estudiante.objects.get(id=request.POST.get("estudiante_id"))
            obj.Rut = request.POST.get("rut_edit")
            obj.NombreE = request.POST.get("nombre_edit")
            obj.ApellidoE = request.POST.get("apellido_edit")
            obj.save()
        elif acc == "eliminar_estudiante":
            Estudiante.objects.filter(id=request.POST.get("estudiante_id")).delete()

        elif acc == "crear_reserva":
            Reserva.objects.create(
                Estudiante=Estudiante.objects.get(id=request.POST.get("estudiante")),
                Sala=Sala.objects.get(id=request.POST.get("sala")),
                FechaHI=request.POST.get("fecha_hi"),
                FechaHT=request.POST.get("fecha_ht"))
        elif acc == "editar_reserva":
            obj = Reserva.objects.get(id=request.POST.get("reserva_id"))
            obj.Estudiante = Estudiante.objects.get(id=request.POST.get("estudiante_edit"))
            obj.Sala = Sala.objects.get(id=request.POST.get("sala_edit"))
            obj.FechaHI = request.POST.get("fecha_hi_edit")
            obj.FechaHT = request.POST.get("fecha_ht_edit")
            obj.save()
        elif acc == "eliminar_reserva":
            Reserva.objects.filter(id=request.POST.get("reserva_id")).delete()

        return redirect("modoAdmin")

    return render(request, "modoAdmin.html", {
        "salas": Sala.objects.all(),
        "estudiantes": Estudiante.objects.all(),
        "reservas": Reserva.objects.all(),
    })

def reservar(request, id):
    sala = Sala.objects.get(id=id)
    ahora = timezone.now()
    sala.actualizar_disponibilidad(ahora)

    ocupados = sala.cupos_ocupados(ahora)
    libres = sala.CapacidadM - ocupados

    if request.method == "POST":
        form = mostrar(request.POST)
        if form.is_valid():
            if libres <= 0:                      
                messages.error(request, 'Sala llena.')
                return redirect('salas')

            rut = form.cleaned_data['RutE']
            nombre = form.cleaned_data['NombreE']
            apellido = form.cleaned_data['ApellidoE']
            duracion = form.cleaned_data['duracion']

            alumno, _ = Estudiante.objects.get_or_create(
                Rut=rut,
                defaults={'NombreE': nombre, 'ApellidoE': apellido}
            )
            alumno.NombreE = nombre
            alumno.ApellidoE = apellido
            alumno.save()

            inicio = ahora
            fin = inicio + duracion

            Reserva.objects.create(
                Estudiante=alumno,
                Sala=sala,
                FechaHI=inicio,
                FechaHT=fin
            )
            sala.actualizar_disponibilidad()
            return redirect('salas')
    else:
        form = mostrar()

    return render(request, 'reserva.html',
                  {'sala': sala, 'form': form,
                   'ocupados': ocupados, 'libres': libres})