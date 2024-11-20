from django.shortcuts import render, redirect,  get_object_or_404
from .models import Producto, Usuario, Venta
from django.http import HttpResponse
from django.contrib import messages
import openpyxl
from django.contrib.auth import logout



# Página de inicio
def index(request):
    return render(request, 'main/index.html')

def catalogo(request):
    productos = Producto.objects.all()  # Obtiene todos los productos
    return render(request, 'main/catalogo.html', {'productos': productos})

# Página de login
def login_view(request):
    return render(request, 'main/login.html')

# Página de contacto
def contacto(request):
    return render(request, 'main/contacto.html')


def dashboard(request):
    return render(request, 'main/dashboard.html')

# Procesar mensaje desde el formulario de contacto
def enviar_mensaje(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        mensaje = request.POST.get("mensaje")
        
        # Procesar el mensaje (opcional: guardar en BD o enviar correo)
        return HttpResponse(f"Gracias {nombre}, hemos recibido tu mensaje.")
    
    # Redirigir a la página principal si no se accede mediante POST
    return redirect('index')


def agregar_al_carrito(request, producto_id):
    # Obtener el producto seleccionado
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Verificar si existe un carrito en la sesión, si no, inicializar uno
    carrito = request.session.get('carrito', {})
    
    # Agregar el producto al carrito o actualizar la cantidad
    if str(producto_id) in carrito:
        carrito[str(producto_id)]['cantidad'] += 1
    else:
        carrito[str(producto_id)] = {
            'nombre': producto.nombre,
            'precio': str(producto.precio),
            'cantidad': 1,
        }
    
    # Guardar el carrito en la sesión
    request.session['carrito'] = carrito
    return redirect('catalogo')



def ver_carrito(request):
    carrito = {
        1: {'nombre': 'Collar Artesanal', 'precio': 1499.00, 'cantidad': 2},
        2: {'nombre': 'Cartera de Cuero Vegano', 'precio': 25000.00, 'cantidad': 1},
    }
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    return render(request, 'main/carrito.html', {'carrito': carrito, 'total': total})


def agregar_al_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    producto = get_object_or_404(Producto, id=producto_id)

    if str(producto_id) in carrito:
        carrito[str(producto_id)]['cantidad'] += 1
    else:
        carrito[str(producto_id)] = {
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'cantidad': 1,
        }

    request.session['carrito'] = carrito
    return redirect('catalogo')

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = 0
    for item in carrito.values():
        item['subtotal'] = item['precio'] * item['cantidad']
        total += item['subtotal']
    return render(request, 'main/carrito.html', {'carrito': carrito, 'total': total})

def actualizar_carrito(request, producto_id):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        carrito = request.session.get('carrito', {})

        if str(producto_id) in carrito:
            if cantidad > 0:
                carrito[str(producto_id)]['cantidad'] = cantidad
            else:
                del carrito[str(producto_id)]

            request.session['carrito'] = carrito

    return redirect('ver_carrito')

def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito

    return redirect('ver_carrito')


def checkout(request):
    carrito = request.session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    # agregar lógica adicional para el proceso de pago
    return render(request, 'main/checkout.html', {'carrito': carrito, 'total': total})


def procesar_pago(request):
    if request.method == 'POST':
        metodo_pago = request.POST.get('metodo_pago')
        carrito = request.session.get('carrito', {})
        total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
        
        #  agregar la logica para procesar el pago según el método seleccionado
        
        # Simulación de procesamiento de pago
        messages.success(request, f'Pago realizado con éxito mediante {metodo_pago}. Total pagado: ${total:.2f}')
        
        # Limpiar el carrito después de la compra
        request.session['carrito'] = {}
        
        return redirect('catalogo')
    else:
        return redirect('ver_carrito')


def generar_reporte_productos(request):
    # Crear un archivo Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Stock de Productos"

    # Encabezados
    ws.append(["ID", "Nombre", "Descripción", "Precio", "Stock"])

    # Datos
    productos = Producto.objects.all()
    for producto in productos:
        ws.append([
            producto.id,
            producto.nombre,
            producto.descripcion,
            producto.precio,
            producto.stock
        ])

    # Configurar la respuesta HTTP
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="stock_productos.xlsx"'
    wb.save(response)

    return response


def generar_reporte_usuarios(request):
    # Implementar la logica
    return HttpResponse("Reporte de usuarios generado exitosamente.")

def logout_view(request):
    logout(request)
    return redirect('index')  # Redirige al inicio después de cerrar sesión



def gestionar_productos(request):
    productos = Producto.objects.all()  
    return render(request, 'main/gestionar_productos.html', {'productos': productos})

def gestionar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'main/gestionar_usuarios.html', {'usuarios': usuarios})

def gestionar_ventas(request):
    ventas = Venta.objects.all()
    return render(request, 'main/gestionar_ventas.html', {'ventas': ventas})


def generar_reportes(request):
    if request.method == 'POST':
        tipo_reporte = request.POST.get('tipo-reporte')

        # Lógica para generar reportes según el tipo seleccionado
        if tipo_reporte == 'usuarios':
            # Lógica para el reporte de usuarios
            pass
        elif tipo_reporte == 'productos':
            # Lógica para el reporte de productos
            pass
        elif tipo_reporte == 'ventas':
            # Lógica para el reporte de ventas
            pass

        return render(request, 'main/reporte_generado.html', {'tipo_reporte': tipo_reporte})
    return render(request, 'main/generar_reportes.html')
