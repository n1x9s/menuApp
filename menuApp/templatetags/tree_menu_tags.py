from django import template
from menuApp.models import MenuItem
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag
def menu_draw(menu_name):
    menu_items = MenuItem.objects.filter(name=menu_name).select_related('parent')
    return mark_safe(menu_render(menu_items))


def menu_render(menu_items):
    menu_html = '<ul>'
    for item in menu_items:
        menu_html += '<li>'
        if item.url:
            menu_html += f'<a href="{item.url}">{item.name}</a>'
        elif item.named_url:
            menu_html += f'<a href="{item.named_url}">{item.name}</a>'
        else:
            menu_html += item.name
        if item.children.exists():
            menu_html += menu_render(item.children.all())
        menu_html += '</li>'
    menu_html += '</ul>'  
    return menu_html 


