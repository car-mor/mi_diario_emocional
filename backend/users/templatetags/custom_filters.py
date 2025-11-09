# users/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    """
    Reemplaza en el string: value.replace(old, new)
    Uso: {{ "hello world"|replace:"world|there" }}
    """
    if '|' not in arg:
        return value
    
    old, new = arg.split('|', 1)
    return value.replace(old, new)

@register.filter
def multiply(value, arg):
    """
    Multiplica el valor por el argumento
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def get_emotion_class(value):
    """
    Convierte combinaciones de emociones a clases CSS
    """
    if not value:
        return "bar-combinacion"
    
    # Convertir "miedo - sorpresa" a "miedo-sorpresa"
    class_name = value.lower().replace(" - ", "-").replace(" ", "-")
    return f"bar-{class_name}"

@register.filter
def calculate_percentage(value, total):
    """
    Calcula el porcentaje: (value / total) * 100
    """
    try:
        # Si total es un QuerySet, obtener su longitud
        if hasattr(total, 'count'):
            total = total.count()
        elif hasattr(total, '__len__'):
            total = len(total)
        
        total = float(total)
        if total == 0:
            return 0
        return (float(value) / total) * 100
    except (ValueError, TypeError, ZeroDivisionError):
        return 0
    