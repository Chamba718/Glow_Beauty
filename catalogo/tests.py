from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Categoria, Producto


class CatalogoViewsTests(TestCase):
    def setUp(self):
        categoria = Categoria.objects.create(nombre="Rostro", slug="rostro")
        self.producto = Producto.objects.create(
            categoria=categoria, nombre="Rubor Cereza", slug="rubor-cereza",
            descripcion="Color suave y luminoso.", precio=Decimal("45.00"), destacado=True,
        )

    def test_listado_muestra_producto_disponible(self):
        response = self.client.get(reverse("catalogo:inicio"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rubor Cereza")

    def test_detalle_del_producto(self):
        response = self.client.get(self.producto.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Color suave y luminoso.")

    def test_usuario_puede_guardar_favorito(self):
        usuario = User.objects.create_user(username="ana", password="clave-segura-123")
        self.client.force_login(usuario)
        response = self.client.post(reverse("catalogo:alternar_favorito", args=[self.producto.slug]))
        self.assertRedirects(response, self.producto.get_absolute_url())
        self.assertEqual(usuario.favoritos.count(), 1)
