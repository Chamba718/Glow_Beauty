from .models import Carrito

def cart_count(request):
    if request.user.is_authenticated:
        try:
            carrito = Carrito.objects.get(usuario=request.user)
            # Sumar las cantidades de todos los items
            total_items = sum(item.cantidad for item in carrito.items.all())
            return {"cart_count": total_items}
        except Carrito.DoesNotExist:
            return {"cart_count": 0}
    return {"cart_count": 0}
