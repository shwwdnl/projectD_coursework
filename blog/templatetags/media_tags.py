from django import template

register = template.Library()


@register.simple_tag()
def media_path(path: str):
    """Returns object media url if exists, else photo placeholder"""
    if path:
        return f"/media/{path}"
    return "/static/images/no-photo.jpg"
