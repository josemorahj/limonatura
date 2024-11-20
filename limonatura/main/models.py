from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Producto(models.Model):
    CATEGORIA_CHOICES = [
        ('Joyería', 'Joyería'),
        ('Carteras', 'Carteras'),
        ('Vestimenta', 'Vestimenta'),
        ('Calzado', 'Calzado'),
    ]
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    imagen = models.ImageField(upload_to='productos/')

    def __str__(self):
        return self.nombre
    

class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Vendedor', 'Vendedor'),
        ('Cliente', 'Cliente'),
    ]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)
    rut = models.CharField(max_length=12, unique=True)  # Ej: 12.345.678-9

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  
        blank=True,
    )

    def __str__(self):
        return f"{self.username} ({self.rol})"



class Venta(models.Model):
    METODO_PAGO_CHOICES = [
        ('PayPal', 'PayPal'),
        ('Transferencia', 'Transferencia'),
        ('Efectivo', 'Efectivo'),
    ]
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'Cliente'})
    productos = models.ManyToManyField(Producto, through='DetalleVenta')
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)

    def __str__(self):
        return f"Venta #{self.id} - Cliente: {self.cliente.username}"
    

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta #{self.venta.id} - Producto: {self.producto.nombre} (x{self.cantidad})"
