from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Categoria(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="productos")
    nombre = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to="productos/", blank=True, null=True)
    disponible = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "productos"
        ordering = ["-destacado", "nombre"]

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("catalogo:detalle_producto", kwargs={"slug": self.slug})


class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favoritos")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="marcado_como_favorito")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "favorito"
        verbose_name_plural = "favoritos"
        constraints = [models.UniqueConstraint(fields=["usuario", "producto"], name="favorito_unico_por_usuario")]

    def __str__(self):
        return f"{self.usuario.username} · {self.producto.nombre}"

class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="carrito")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "carrito"
        verbose_name_plural = "carritos"

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

    @property
    def get_total(self):
        return sum(item.get_subtotal for item in self.items.all())


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "ítem del carrito"
        verbose_name_plural = "ítems del carrito"

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre}"

    @property
    def get_subtotal(self):
        return self.producto.precio * self.cantidad
