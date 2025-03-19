from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key, "-")
    return "-"

@register.filter
def get_input(form, field_name):
    """Returns a specific form field dynamically."""
    return form[field_name] if field_name in form.fields else ""


@register.filter
def add_prefix(value, prefix):
    """Adds a prefix to a given string."""
    return f"{prefix}{value}"


@register.filter
def dict_key(dictionary, key):
    """Retrieve a dictionary value by key in Django templates."""
    return dictionary.get(key, None)