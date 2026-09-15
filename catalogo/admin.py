from django.contrib import admin
from .models import Categoria, Favorito, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    prepopulated_fields = {"slug": ("nombre",)}
    search_fields = ("nombre",)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "precio", "disponible", "destacado")
    list_filter = ("categoria", "disponible", "destacado")
    list_editable = ("disponible", "destacado")
    search_fields = ("nombre", "descripcion")
    prepopulated_fields = {"slug": ("nombre",)}
    readonly_fields = ("creado_en", "actualizado_en")


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "producto", "creado_en")
    list_filter = ("creado_en",)
    search_fields = ("usuario__username", "producto__nombre")
    readonly_fields = ("creado_en",)
