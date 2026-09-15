from django import template

register = template.Library()


@register.filter(name="cop")
def formato_cop(valor):
    """
    Formatea un número como precio en Peso Colombiano (COP).
    Ejemplo: 10000 → $10.000  |  1500000 → $1.500.000
    """
    try:
        valor = int(round(float(valor)))
        # Usar punto como separador de miles (formato colombiano)
        formateado = f"{valor:,.0f}".replace(",", ".")
        return f"${formateado}"
    except (TypeError, ValueError):
        return f"${valor}"
