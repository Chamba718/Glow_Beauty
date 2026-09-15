from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegistroForm
from .models import Categoria, Favorito, Producto, Carrito, ItemCarrito, PerfilUsuario


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

@login_required
def checkout_whatsapp(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    perfil, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)
    
    if carrito.items.count() == 0:
        messages.error(request, "Tu carrito está vacío. Agrega productos antes de comprar.")
        return redirect("catalogo:ver_carrito")
        
    if request.method == "POST":
        # Guardar datos del usuario
        request.user.first_name = request.POST.get("nombre", "")
        request.user.last_name = request.POST.get("apellido", "")
        request.user.save()
        
        perfil.telefono = request.POST.get("telefono", "")
        perfil.direccion = request.POST.get("direccion", "")
        perfil.save()
        
        # Construir mensaje de WhatsApp premium
        import urllib.parse
        
        def cop(valor):
            """Formato Peso Colombiano: 10000 → $10.000"""
            try:
                return f"${int(round(float(valor))):,.0f}".replace(",", ".")
            except Exception:
                return f"${valor}"
        
        numero_whatsapp = "573152814129"
        
        nombre_completo = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
        
        linea = "━━━━━━━━━━━━━━━━━━━━━━━━"
        
        mensaje  = f"✨ *NUEVO PEDIDO — GLOW BEAUTY* ✨\n"
        mensaje += f"{linea}\n\n"
        
        mensaje += f"👤 *Cliente*\n"
        mensaje += f"   Nombre: *{nombre_completo}*\n"
        mensaje += f"   📞 Tel: {perfil.telefono}\n"
        mensaje += f"   📍 Dirección: {perfil.direccion}\n\n"
        
        mensaje += f"{linea}\n"
        mensaje += f"🛍️ *Detalle del Pedido*\n"
        mensaje += f"{linea}\n"
        for item in carrito.items.all():
            subtotal = cop(item.get_subtotal)
            precio_unit = cop(item.producto.precio)
            mensaje += f"\n▸ *{item.producto.nombre}*\n"
            mensaje += f"   {item.cantidad} ud. × {precio_unit} = *{subtotal}*\n"
        
        total = cop(carrito.get_total)
        mensaje += f"\n{linea}\n"
        mensaje += f"💰 *TOTAL A PAGAR: {total}*\n"
        mensaje += f"{linea}\n\n"
        mensaje += f"_Pago contra entrega / transferencia._\n"
        mensaje += f"¡Gracias por tu compra! 🌸"
        
        # Vaciar el carrito
        carrito.items.all().delete()
        
        # Codificar mensaje para URL
        mensaje_codificado = urllib.parse.quote(mensaje)
        url_whatsapp = f"https://wa.me/{numero_whatsapp}?text={mensaje_codificado}"
        
        return redirect(url_whatsapp)
        
    return render(request, "catalogo/checkout.html", {"carrito": carrito, "perfil": perfil})
