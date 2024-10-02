from django import template
from django.utils.datastructures import MultiValueDictKeyError

from menu_app.models import MenuItem


register = template.Library()


@register.inclusion_tag('menu_app/draw_menu.html', takes_context=True)
def draw_menu(context, menu_name):
    # Получаем все элементы для указанного меню
    items = MenuItem.objects.filter(menu__name=menu_name)
    # Находим корневые элементы (без родителя)
    super_parents = items.filter(parent=None)

    # Если есть параметр выбора элемента
    selected_item = context['request'].GET.get(menu_name)
    if selected_item:
        try:
            selected_item = items.get(id=selected_item)
            expanded_items_id_list = get_expanded_items_id_list(selected_item)
            for parent in super_parents:
                if parent.id in expanded_items_id_list:
                    parent.children = get_child_items(items, parent.id, expanded_items_id_list)
            result_dict = {'items': super_parents}
        except MenuItem.DoesNotExist:
            result_dict = {'items': super_parents}
    else:
        result_dict = {'items': super_parents}

    return result_dict


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
    current_parent_child_list = [
        item for item in item_values.filter(parent_id=current_parent_id)
    ]
    for child in current_parent_child_list:
        if child['id'] in expanded_items_id_list:
            child['child_items'] = get_child_items(
                item_values, child['id'], expanded_items_id_list
            )
    return current_parent_child_list