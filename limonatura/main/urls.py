from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página de inicio
    path('catalogo/', views.catalogo, name='catalogo'),  # Página de catálogo
    path('login/', views.login_view, name='login'),  # Página de login
    path('contacto/', views.contacto, name='contacto'),  # Página de contacto
    path('enviar-mensaje/', views.enviar_mensaje, name='enviar_mensaje'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/actualizar/<int:producto_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('checkout/', views.checkout, name='checkout'),
    path('procesar_pago/', views.procesar_pago, name='procesar_pago'),
    path("reporte/usuarios/", views.generar_reporte_usuarios, name="reporte_usuarios"),
    path("reporte/productos/", views.generar_reporte_productos, name="reporte_productos"),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/productos/', views.gestionar_productos, name='gestionar_productos'),  # Gestión de productos
    path('dashboard/usuarios/', views.gestionar_usuarios, name='gestionar_usuarios'),  # Gestión de usuarios
    path('dashboard/ventas/', views.gestionar_ventas, name='gestionar_ventas'),
    path('dashboard/reportes/', views.generar_reportes, name='generar_reportes'),
]
