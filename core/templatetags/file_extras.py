# core/templatetags/file_extras.py
import os
from django import template

register = template.Library()

@register.filter
def filename(value):
    """
    "/media/foo/bar.pdf" → "bar.pdf"
    """
    return os.path.basename(value)
