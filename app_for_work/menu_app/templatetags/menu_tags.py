from django import template
from django.utils.datastructures import MultiValueDictKeyError

from menu_app.models import MenuItem


register = template.Library()


@register.inclusion_tag('menu_app/draw_menu.html', takes_context=True)
def draw_menu(context, menu_name):
    # Получаем все элементы для указанного меню
    items = MenuItem.objects.filter(menu__name=menu_name)
    # Находим корневые элементы (без родителя)
    super_parents = list(items.filter(parent=None))

    # Пытаемся найти выбранный пункт по GET-параметру или по текущему URL
    selected_item_id = context['request'].GET.get(menu_name)
    
    if not selected_item_id:
        # Определяем текущий URL
        current_path = context['request'].path
        
        # Ищем пункт меню с таким URL или named_url
        for item in items:
            if item.url == current_path or (item.named_url and _get_url_for_named_url(context, item.named_url) == current_path):
                selected_item_id = item.id
                break
    
    if selected_item_id:
        try:
            selected_item = items.get(id=selected_item_id)
            expanded_items_id_list = get_expanded_items_id_list(selected_item)
            for parent in super_parents:
                if parent.id in expanded_items_id_list:
                    parent.child_items = get_child_items(items, parent.id, expanded_items_id_list)
        except MenuItem.DoesNotExist:
            pass

    return {'items': super_parents}


def _get_url_for_named_url(context, named_url):
    """Получает URL по именованному URL."""
    from django.urls import reverse
    try:
        return reverse(named_url)
    except Exception:
        return ''


def get_expanded_items_id_list(parent):
    """
    Формирует список всех развернутых пунктов меню.
    """
    expanded_items_id_list = []
    while parent:
        expanded_items_id_list.append(parent.id)
        parent = parent.parent
    return expanded_items_id_list


def get_child_items(item_values, current_parent_id, expanded_items_id_list):
    """
    Для переданного в аргументе текущего родителя рекурсивно
    формирует список дочерних элементов.
    """
    current_parent_child_list = list(item_values.filter(parent_id=current_parent_id))
    for child in current_parent_child_list:
        if child.id in expanded_items_id_list:
            child.child_items = get_child_items(item_values, child.id, expanded_items_id_list)
    return current_parent_child_list