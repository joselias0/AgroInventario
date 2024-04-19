from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .models import recursos, gastos_recursos ,salud_gallinas
from .formularios import RecursoForm , GastoForm, SaludForm
from .models import *


@login_required
@csrf_protect
def salir(request):
    logout(request)
    return redirect('/')

@csrf_protect
@login_required
def index(request):
    return render(request, 'index.html')

@csrf_protect
@login_required
def huevos(request):
    pro = Producto.objects.all()
    return render(request, 'adm-huevos.html', {'Producto':pro})

@csrf_protect
@login_required
def venta(request):
    return render(request, 'adm-ventas.html')

@csrf_protect
@login_required
def recurso(request):
    recursos_list = recursos.objects.all()
    return render(request, 'adm-recursos.html',{'recursos_list': recursos_list})

@csrf_protect
@login_required
def contabilidad(request):
    return render(request, 'adm-contabilidad.html')

@csrf_protect
@login_required
def agregarGasto(request, id_recurso):
    recurso = recursos.objects.get(id=id_recurso)
    if request.method == 'POST':
        formulario = GastoForm(request.POST)
        if formulario.is_valid():
            gasto = formulario.save(commit=False)
            gasto.id_recurso = recurso
            gasto.save()
            recurso.cantidad_disponible += gasto.cantidad_agregada
            recurso.save()
            messages.success(request, '¡Gasto Agregado con Exito!')   
            return redirect('recurso')
    else:
        formulario = GastoForm()
    return render(request, 'adm-agregarGasto.html', {'formulario': formulario , 'recurso' : recurso} )

@csrf_protect
@login_required
def adicion(request):
    formulario = RecursoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        messages.success(request, '¡Recurso Agregado con Exito!')   
        return redirect('recurso')
    return render(request, 'adm-adicion.html', {'formulario': formulario})



@csrf_protect
@login_required
def editarRecurso(request, id):
    recurso = recursos.objects.get(id=id)
    formulario = RecursoForm(request.POST or None, request.FILES or None, instance=recurso)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('recurso')
    return render(request, 'adm-editarRecurso.html', {'formulario': formulario , 'recurso' : recurso})



@csrf_protect
@login_required
def eliminarRecurso(request, id):
    recurso_delete = get_object_or_404(recursos, id=id)
    recurso_delete.delete(using=None, keep_parents=False)
    messages.error(request,"¡Recurso Eliminado!")
    return redirect('recurso')



@csrf_protect
@login_required
def cuidado(request):
    salud_list = salud_gallinas.objects.all()
    recursos_disponibles = recursos.objects.all()
    if request.method == 'POST':
        formulario = SaludForm(request.POST)
        if formulario.is_valid():
            tipo_accion = formulario.cleaned_data['tipo_accion']
            fecha = formulario.cleaned_data['fecha']
            comentarios = formulario.cleaned_data['comentarios']
            cantidad_recurso_usado = formulario.cleaned_data['cantidad_recurso_usado']
            id_recurso_id = request.POST['id_recurso'] 
            
            recurso = get_object_or_404(recursos, pk=id_recurso_id)
            
            if cantidad_recurso_usado > recurso.cantidad_disponible:
                messages.error(request, 'No hay suficiente cantidad disponible de este recurso.')
                return redirect('cuidado')
            
            cuidado_gallinas = salud_gallinas.objects.create(
                tipo_accion=tipo_accion,
                fecha=fecha,
                comentarios=comentarios,
                cantidad_recurso_usado=cantidad_recurso_usado,
                id_recurso_id=id_recurso_id 
            )
            
            recurso.cantidad_disponible -= cantidad_recurso_usado
            recurso.save()

            messages.success(request, 'Se registro el cuidado con exito.')
            return redirect('cuidado') 
            
    else:
        formulario = SaludForm()

    return render(request, 'adm-cuidado.html', {'formulario': formulario, 'recursos_disponibles': recursos_disponibles, 'salud_list': salud_list})


