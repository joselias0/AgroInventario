from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
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

        suma_gastos= "{:.2f}".format(suma_gastos)
        ventas1 = ventas.objects.filter(fecha__range=(fecha_inicio, fecha_fin)).aggregate(total=Sum('precio_final'))['total']
        suma_ganancias = 0
        if ventas1 is not None:
            suma_ganancias = float(ventas1)
        else:
            suma_ganancias = 0.0

        suma_ganancias= "{:.2f}".format(suma_ganancias)
        balance = float(suma_ganancias) - float(suma_gastos)
        balance= "{:.2f}".format(balance)
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
def pag_add_tamano(request):
    tam = Tamaño.objects.exclude(producto__isnull=False)
    if tam.exists():
        return render(request, 'add_tamano.html', {'Tamaño': tam}) 
    else:
        error_message = "No es posible agregar una nueva clasificación porque los tamaños ya han sido asignados a los productos."
        return render(request, 'add_tamano.html', {'error_message':error_message})


@login_required
@csrf_protect
def pag_add_inventario(request, id1):
    if request.method == 'POST':
        # Recupera todos los lotes y productos disponibles en la base de datos
        Lot = Lote.objects.all()
        prodi = Producto.objects.all()
        # Obtiene el producto específico según el ID proporcionado en la URL
        produc1 = Producto.objects.get(id=id1)
        # Obtiene los datos ingresados por el usuario desde el formulario
        cantidad1 = int(request.POST['cantidad'])
        fecha1 = request.POST['fecha']
        precio_individual_carton = request.POST['precio_unitario']

        # Validar el precio ingresado a un número flotante
        try:
            precio_individual_carton = float(precio_individual_carton)
        except ValueError:
            # Si el usuario ingresa un valor no numérico como precio, se muestra un mensaje de error
            message = "Error: El precio ingresado no es válido."
            return render(request, 'adm-huevos.html', {"Producto": prodi, 'error_message': message})

        # Calcula la fecha de vencimiento del lote (15 días después de la fecha de creación)
        fecha_objeto = datetime.strptime(fecha1, '%Y-%m-%d')
        fecha_venci = fecha_objeto + timedelta(days=15)

        # Crea un nuevo lote en la base de datos con los datos proporcionados por el usuario
        Lot = Lote.objects.create(
            produc = produc1,
            cantidad = cantidad1,
            fecha_creacion = fecha_objeto,
            fecha_vencimiento = fecha_venci,
            costo_produccion = produc1.costo_produccion,
            precio_individual = precio_individual_carton
        )
        Lot.save()
        # Actualiza la cantidad disponible del producto en la base de datos
        produc1.cantidad = produc1.cantidad + cantidad1
        produc1.save()
        # Muestra un mensaje de éxito y vuelve a renderizar la página de administración de productos
        message = "El lote fue registrado con éxito"
        return render(request, 'adm-huevos.html', {"Producto": prodi, 'message': message})
    
    # Si la solicitud no es de tipo POST, renderiza el formulario para agregar inventario
    return render(request, 'add_inventario.html', {"id": id1})


@login_required
@csrf_protect
def ver_lotes(request, id):
    prodi = Producto.objects.all()
    lotes = Lote.objects.filter(produc_id=id)
    lotes.count()
    if lotes.count()==0:
        error_message="No hay lotes disponibles para este producto"
        return render(request, 'adm-huevos.html', {"Producto": prodi, 'error_message': error_message})
    else:
        return render(request, 'ver_lotes.html', {'Lotes': lotes})

@login_required
@csrf_protect   
def borrar_lote(request, id):
    try:
        message = "El lote fue borrado con exito"
        p_delete = Lote.objects.get(id=id)
        prod = Producto.objects.get(id=p_delete.produc.id)
        lotes = Lote.objects.filter(produc_id=prod.id)
        prod.cantidad -= p_delete.cantidad
        prod.save()
        p_delete.delete()
        prodi = Producto.objects.all()
        
        if prod.cantidad==0:
            message = "El lote fue borrado con exito"
            return render(request, 'adm-huevos.html', {"Producto": prodi, 'message': message})
        else:
            message = "El lote fue borrado con exito"
            
            return render(request, 'ver_lotes.html', {'Lotes': lotes, 'message': message}) 
    except:
        return JsonResponse({'error': 'El registro no ha sido borrado'})
    
@csrf_protect
@login_required
def pag_borrar_prod(request, id):
    Prod = Producto.objects.get(id=id)
    return render(request, 'eliminar_prod_lote.html', {'Producto': Prod})

@csrf_protect
@login_required
def pag_borrar_lot(request, id):
    Lot = Lote.objects.get(id=id)
    return render(request, 'eliminar_prod_lote.html', {'Lote': Lot})

@csrf_protect
@login_required
def edit_lote(request, id):
    lote = Lote.objects.get(id=id)
    
    if request.method == 'POST':
        cantidad = request.POST['cantidad']
        precio = request.POST['precio_unitario']
        
        lote_objeto = Lote.objects.get(id=id)

        lot1 = Lote.objects.get(id=id)
        prod2 = Producto.objects.get(id=lot1.produc.id)
        lotes1 = Lote.objects.filter(produc_id=prod2.id)
        try:
            precio = precio.replace(',', '.')
            precio = float(precio)
        except ValueError:
            message = "Error: El precio ingresado no es válido."
            return render(request, 'ver_lotes.html', {'error_message': message, 'Lotes': lotes1})
       
        
        # Actualizar los campos del lote
        lote_objeto.precio_individual = float(precio)
        prod = Producto.objects.get(id=lote_objeto.produc.id)
        prod.cantidad -=lote_objeto.cantidad
        lote_objeto.cantidad = int(cantidad)
        prod.cantidad += int(cantidad)
        prod.save()
        lote_objeto.save()

        #mostrar datos
        lot = Lote.objects.get(id=id)
        prod1 = Producto.objects.get(id=lot.produc.id)
        lotes = Lote.objects.filter(produc_id=prod1.id)
        
        
        # Mensaje de éxito
        message = "El lote fue editado con éxito."
        return render(request, 'ver_lotes.html', {'message': message, 'Lotes': lotes})
    
    return render(request, 'edit_lote.html', {'lote': lote})


@login_required
@csrf_protect
def add_tamano(request):
    if request.method == 'POST':
        Prod1 = Producto.objects.all()
        precio1 = request.POST['precio']
        tamaño = request.POST['tamaño']
        id_tamaño=Tamaño.objects.get(pk=tamaño)
        message = "La nueva clasificación fue agregada con exito"
        try:
            precio1 = precio1.replace(',', '.')
            precio1 = float(precio1)
        except ValueError:
            message = "Error: El precio ingresado no es válido."
            return render(request, 'adm-huevos.html', {'Producto': Prod1, 'error_message':message})
        

        Prod = Producto.objects.create(
            cantidad=0,
            costo_produccion=precio1,
            tamaño=id_tamaño,
        )

        Prod.save()
        
        return render(request, 'adm-huevos.html', {'Producto': Prod1, 'message':message}) 

@login_required
@csrf_protect   
def borrar_tamano(request, id):
    try:
        Prod = Producto.objects.all()
        message = "La clasificación fue borrada con exito"
        p_delete = Producto.objects.get(id=id)
        p_delete.delete()
        return render(request, 'adm-huevos.html', {'Producto': Prod, 'error_message' : message})
    except:
        return JsonResponse({'error': 'El registro no ha sido borrado'})
    

@csrf_protect
@login_required
def edit_tamano(request, id):
    tam = Producto.objects.get(id=id)
    tamaño = Tamaño.objects.filter(producto__isnull=True)
    if tam.tamaño:
        tamaño = tamaño | Tamaño.objects.filter(pk=tam.tamaño.id)
    if  request.method=='POST':
        precio1 = request.POST['precio']
        tamaño = request.POST['tamaño']
        Produc = Producto.objects.get(id=id)
        tamaño = Tamaño.objects.get(id=tamaño)
        tamaño1 = Tamaño.objects.filter(producto__isnull=True)
        Prod = Producto.objects.all()
        try:
            precio1 = precio1.replace(',', '.')
            precio1 = float(precio1)
        except ValueError:
            message = "Error: El precio ingresado no es válido."
            return render(request,'adm-huevos.html', {'Producto':Prod, 'error_message':message })
        
        Produc.costo_produccion = float(precio1)
        Produc.tamaño = tamaño
        Produc.save()
        message = "El producto fue editado con exito"
        return render(request,'adm-huevos.html', {'Producto':Prod, 'message':message })
    return render(request, 'edit_tamano.html', {'Producto': tam, 'Tamaño': tamaño })
    

@login_required
@csrf_protect
def pag_add_venta(request):
    prod = Producto.objects.all()
    return render(request, 'add_ventas.html', {'Producto': prod}) 
    


@csrf_protect
@login_required
def add_venta(request):
    if request.method == 'POST':
        nombre1 = request.POST['nombre']
        cantidad_solicitada = int(request.POST['cantidad'])
        producto_id = request.POST['producto']
        fecha = request.POST['fecha']
        fecha_objeto = datetime.strptime(fecha, '%Y-%m-%d')
        producto = Producto.objects.get(id=producto_id)
        # Calcular la cantidad total disponible del producto en todos los lotes
        cantidad_total_disponible = Lote.objects.filter(produc=producto_id).aggregate(total=Sum('cantidad'))['total'] or 0
        
        # Validar si la cantidad solicitada es mayor que la cantidad disponible
        if cantidad_solicitada > cantidad_total_disponible:
            # Mostrar mensaje de error al usuario
            error_message= 'La cantidad solicitada es mayor que la cantidad disponible para el producto seleccionado.'
            vent = ventas.objects.all()
            pro = Producto.objects.all()
            return render(request, 'adm-ventas.html', {'ventas':vent, 'Producto':pro, 'error_message':error_message})
        
        # Actualizar la cantidad disponible del producto
        producto.cantidad -= cantidad_solicitada
        # Descuentos de la cantidad solicitada de los lotes disponibles
        cantidad = cantidad_solicitada
        lotes_disponibles = Lote.objects.filter(produc=producto_id, cantidad__gt=0).order_by('fecha_creacion')
        precio_final = 0
        lotes_utilizados = []

        # Iterar sobre los lotes disponibles y descontar la cantidad solicitada
        for lote in lotes_disponibles:
            if cantidad_solicitada > 0:
                cantidad_descontada = min(cantidad_solicitada, lote.cantidad)
                precio_final += (lote.precio_individual - lote.costo_produccion) * cantidad_descontada
                lote.cantidad -= cantidad_descontada
                lote.save()
                lotes_utilizados.append(lote) 
                cantidad_solicitada -= cantidad_descontada

        # Crear un registro de venta y detalle de venta
        venta = ventas.objects.create(nombre=nombre1, cantidad=cantidad, precio_final=precio_final, fecha=fecha_objeto)
        producto.save()
        detalle_venta = DetalleVentas.objects.create(venta=venta)
        detalle_venta.lotes.set(lotes_utilizados)

        # Renderizar la página de administración de ventas con todas las ventas
        return render(request, 'adm-ventas.html', {'ventas': ventas.objects.all()})  


@csrf_protect
@login_required
def r_devolucion(request, id):
    prod = Producto.objects.all()
    ventas_unicas = ventas.objects.get(id=id)
    if request.method == 'POST':
        cantidad_solicitada = int(request.POST['cantidad'])
        producto_id = request.POST['producto']
        cantidad = cantidad_solicitada
        prod = Producto.objects.get(id=producto_id)
        
        cantidad_total_disponible = Lote.objects.filter(produc=producto_id).aggregate(total=Sum('cantidad'))['total'] or 0
        
        if cantidad_solicitada > cantidad_total_disponible:
            error_message= 'La cantidad solicitada es mayor que la cantidad disponible para el producto seleccionado.'
            vent = ventas.objects.all()
            pro = Producto.objects.all()
           
            return render(request, 'adm-ventas.html', {'ventas':vent, 'Producto':pro, 'error_message':error_message})
        if cantidad_solicitada > ventas_unicas.cantidad:
            message1= 'La devolución ha sido realizada con exito'
            prod.cantidad -= cantidad_solicitada
            precio_final = 0
            lotes_disponibles = Lote.objects.filter(produc=producto_id, cantidad__gt=0).order_by('fecha_creacion')

            lotes_utilizados = []

            for lote in lotes_disponibles:
                if cantidad_solicitada > 0:
                    cantidad_descontada = min(cantidad_solicitada, lote.cantidad)
                    precio_final += (lote.precio_individual - lote.costo_produccion) * cantidad_descontada
                    lote.cantidad -= cantidad_descontada
                    lote.save()
                    lotes_utilizados.append(lote) 
                    cantidad_solicitada -= cantidad_descontada
            ventas_unicas.cantidad =  cantidad
            ventas_unicas.precio_final = precio_final
            ventas_unicas.save()
            prod.save()
            detalle_venta = DetalleVentas.objects.get(venta=ventas_unicas)
            detalle_venta.lotes.set(lotes_utilizados)
            detalle_venta.save()
            vent = ventas.objects.all()
            pro = Producto.objects.all()
            return render(request, 'adm-ventas.html', {'ventas':vent, 'Producto':pro, 'message':message1})
        
        prod.cantidad -= cantidad_solicitada
        
        lotes_disponibles = Lote.objects.filter(produc=producto_id, cantidad__gt=0).order_by('fecha_creacion')

        lotes_utilizados = []

        for lote in lotes_disponibles:
            if cantidad_solicitada > 0:
                cantidad_descontada = min(cantidad_solicitada, lote.cantidad)
                lote.cantidad -= cantidad_descontada
                lote.save()
                lotes_utilizados.append(lote) 
                cantidad_solicitada -= cantidad_descontada
        prod.save()
        detalle_venta = DetalleVentas.objects.get(venta=ventas_unicas)
        detalle_venta.lotes.set(lotes_utilizados)
        detalle_venta.save()
        message= 'La devolución ha sido realizada con exito'
        return render(request, 'adm-ventas.html', {'ventas': ventas.objects.all(), 'message':message})
    return render(request, 'devolucion.html', {'Producto': prod, 'ventas': ventas_unicas}) 
