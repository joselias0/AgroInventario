from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import *
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus import SimpleDocTemplate, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.db.models import Sum

@login_required
@csrf_protect
def generar_pdf_vp(request):
    if request.method == 'POST': 
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        btn = request.POST.get('action')
        gastos = gastos_recursos.objects.all() 
        ventas1 = ventas.objects.all()  

        if fecha_inicio > fecha_fin:
            error_message = "La fecha de inicio no puede ser mayor que la fecha final."
            return render(request, 'adm-contabilidad.html', {'error_message': error_message})

        gastos = gastos_recursos.objects.filter(fecha__range=(fecha_inicio, fecha_fin)).aggregate(total=Sum('precio'))['total']
        suma_gastos = 0
        if gastos is not None:
            suma_gastos = float(gastos)
        else:
            suma_gastos = 0.0

        ventas1 = ventas.objects.filter(fecha__range=(fecha_inicio, fecha_fin)).aggregate(total=Sum('precio_final'))['total']
        suma_ganancias = 0
        if ventas1 is not None:
            suma_ganancias = float(ventas1)
        else:
            suma_ganancias = 0.0
        balance = suma_ganancias - suma_gastos

        if btn == 'vista_previa':
            return render(request, 'adm-contabilidad.html', {'suma_ganancias': suma_ganancias, 'suma_gastos': suma_gastos, 'fecha_inicio':fecha_inicio, 'fecha_fin':fecha_fin, 'balance':balance})
        elif btn == 'generar_informe':
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="resultado_balance.pdf"'

            doc = SimpleDocTemplate(response, pagesize=letter)
            elements = []

            styles = getSampleStyleSheet()
            style = styles["Normal"]
            
            image_path = "static/multimedia/logo - agro.png"
            img = Image(image_path)
            img.drawHeight = 100
            img.drawWidth = 100
            elements.append(img)
            

            centered_style = ParagraphStyle(name='CenteredStyle', alignment=1)

            centered_text = f"Granja Ramírez<br/>"
            centered_para = Paragraph(centered_text, centered_style)
            elements.append(centered_para)

            if fecha_inicio:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            else:
                fecha_inicio = None

            if fecha_fin:
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
            else:
                fecha_fin = None
            
            text = f"<br/><b>Fecha inicio:</b> {fecha_inicio.strftime('%d/%m/%Y')}<br/>"
            text += f"<br/><b>Fecha fin:</b> {fecha_fin.strftime('%d/%m/%Y')}<br/>"
            text += f"<br/><b>Gastos:</b> {suma_gastos} <br/>"
            text += f"<br/><b>Ganancias:</b> {suma_ganancias} <br/>"
            text += f"<br/><b>Balance:</b> {balance} <br/>"
            para = Paragraph(text, style)
            elements.append(para)
            doc.build(elements)

            return response

    return HttpResponse("Error: No se pudo generar el PDF")

@login_required
@csrf_protect
def pag_add_tamaño(request):
    tam = Tamaño.objects.all()
    return render(request, 'add_tamano.html', {'Tamaño': tam})

@login_required
@csrf_protect
def pag_add_inventario(request, id1):
    if request.method == 'POST':
        Prod = productividad.objects.all()
        prodi = Producto.objects.all()
        produc = Producto.objects.get(id=id1)
        cantidad1 = int(request.POST['cantidad'])
        fecha1 = request.POST['fecha']

        fecha_objeto = datetime.strptime(fecha1, '%Y-%m-%d')

        Prod = productividad.objects.create(
            cantidad_agregada = cantidad1,
            fecha = fecha_objeto,
            id_producto = produc
        )
        Prod.save()
        
        produc.cantidad = produc.cantidad + cantidad1
        produc.save()
        return render(request, 'adm-huevos.html', {"Producto": prodi})
    return render(request, 'add_inventario.html', {"id": id1})

@login_required
@csrf_protect
def add_tamano(request):
    Prod = Producto.objects.all()
    if request.method == 'POST':
        cantidad1 = request.POST['cantidad']
        precio1 = request.POST['precio']
        tamaño = request.POST['tamaño']
        id_tamaño=Tamaño.objects.get(pk=tamaño)
        message = "La nueva clasificación fue agregada con exito"
        

        Prod = Producto.objects.create(
            cantidad=cantidad1,
            precio=precio1,
            tamaño=id_tamaño,
        )

        Prod.save()
        

        return render(request, 'adm-huevos.html', {'Producto': Prod, 'message':message}) 

@login_required
@csrf_protect   
def borrar_tamano(request, id):
    try:
        Prod = Producto.objects.all()
        p_delete = Producto.objects.get(id=id)
        p_delete.delete()
        return render(request, 'adm-huevos.html', {'Producto': Prod})
    except:
        return JsonResponse({'error': 'El registro no ha sido borrado'})
    

@csrf_protect
@login_required
def edit_tamano(request, id):
    tam = Producto.objects.get(id=id)
    tamaño = Tamaño.objects.all()
    if  request.method=='POST':
        cantidad1 = request.POST['cantidad']
        precio1 = request.POST['precio']
        tamaño = request.POST['tamaño']
        Produc = Producto.objects.get(id=id)
        tamaño = Tamaño.objects.get(id=tamaño)
        Prod = Producto.objects.all()
        precio1 = precio1.replace(',', '.')
        Produc.cantidad = cantidad1
        Produc.precio = float(precio1)
        Produc.tamaño = tamaño
        Produc.save()
        
        return render(request,'adm-huevos.html', {'Producto':Prod})
    return render(request, 'edit_tamano.html', {'Producto': tam, 'Tamaño': tamaño })
    
 