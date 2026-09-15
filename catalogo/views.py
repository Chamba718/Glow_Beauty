from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegistroForm
from .models import Categoria, Favorito, Producto, Carrito, ItemCarrito


def inicio(request):
    categorias = Categoria.objects.all()
    productos = Producto.objects.filter(disponible=True).select_related("categoria")
    categoria_actual = request.GET.get("categoria", "")
    if categoria_actual:
        productos = productos.filter(categoria__slug=categoria_actual)
    return render(request, "catalogo/inicio.html", {
        "categorias": categorias,
        "productos": productos,
        "destacados": Producto.objects.filter(disponible=True, destacado=True).select_related("categoria")[:3],
        "categoria_actual": categoria_actual,
    })


def detalle_producto(request, slug):
    producto = get_object_or_404(Producto.objects.select_related("categoria"), slug=slug, disponible=True)
    es_favorito = request.user.is_authenticated and Favorito.objects.filter(usuario=request.user, producto=producto).exists()
    return render(request, "catalogo/detalle_producto.html", {"producto": producto, "es_favorito": es_favorito})


def registro(request):
    if request.user.is_authenticated:
        return redirect("catalogo:inicio")
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, "Tu cuenta fue creada. ¡Bienvenida a Glow Beauty!")
            return redirect("catalogo:inicio")
    else:
        form = RegistroForm()
    return render(request, "registration/registro.html", {"form": form})


@login_required
def favoritos(request):
    favoritos_usuario = Favorito.objects.filter(usuario=request.user).select_related("producto__categoria")
    return render(request, "catalogo/favoritos.html", {"favoritos": favoritos_usuario})


@login_required
def alternar_favorito(request, slug):
    if request.method != "POST":
        return redirect("catalogo:detalle_producto", slug=slug)
    producto = get_object_or_404(Producto, slug=slug, disponible=True)
    favorito, creado = Favorito.objects.get_or_create(usuario=request.user, producto=producto)
    if creado:
        messages.success(request, f"{producto.nombre} se añadió a tus favoritos.")
    else:
        favorito.delete()
        messages.info(request, f"{producto.nombre} se eliminó de tus favoritos.")
    return redirect(request.POST.get("next") or "catalogo:detalle_producto", slug=slug)

@login_required
def ver_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    return render(request, "catalogo/carrito.html", {"carrito": carrito})

@login_required
def agregar_al_carrito(request, slug):
    if request.method == "POST":
        producto = get_object_or_404(Producto, slug=slug, disponible=True)
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
        item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
        
        if not creado:
            item.cantidad += 1
            item.save()
            messages.success(request, f"Se agregó otra unidad de {producto.nombre} a tu carrito.")
        else:
            messages.success(request, f"{producto.nombre} se agregó a tu carrito.")
            
    return redirect("catalogo:ver_carrito")

@login_required
def eliminar_del_carrito(request, item_id):
    if request.method == "POST":
        carrito = get_object_or_404(Carrito, usuario=request.user)
        item = get_object_or_404(ItemCarrito, id=item_id, carrito=carrito)
        nombre = item.producto.nombre
        item.delete()
        messages.info(request, f"{nombre} fue eliminado de tu carrito.")
    return redirect("catalogo:ver_carrito")
