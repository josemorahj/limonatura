from django.contrib import admin
from .models import Usuario, Producto, Venta, DetalleVenta
from django.contrib.auth.admin import UserAdmin

admin.site.register(Usuario, UserAdmin)
admin.site.register(Producto)
admin.site.register(Venta)
admin.site.register(DetalleVenta)




