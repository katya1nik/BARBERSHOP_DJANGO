def menu_context(request):
    """
    онтекстный процессор для передачи данных меню во все шаблоны
    """
    menu_items = [
        {'name': 'лавная', 'url': '#home', 'anchor': True},
        {'name': ' нас', 'url': '#about', 'anchor': True},
        {'name': 'астера', 'url': '#masters', 'anchor': True},
        {'name': 'слуги', 'url': '#services', 'anchor': True},
        {'name': 'апись', 'url': '#booking', 'anchor': True},
    ]
    
    # обавляем пункты для персонала
    staff_menu_items = []
    if request.user.is_authenticated and request.user.is_staff:
        staff_menu_items = [
            {'name': 'аявки', 'url': 'orders_list', 'anchor': False},
        ]
    
    return {
        'menu_items': menu_items,
        'staff_menu_items': staff_menu_items,
    }
