def menu_context(request):
    """Контекстный процессор для передачи данных меню во все шаблоны"""
    return {
        'menu_items': [
            {'name': 'Главная', 'url': 'landing', 'anchor': '#home'},
            {'name': 'О нас', 'url': 'landing', 'anchor': '#about'},
            {'name': 'Услуги', 'url': 'landing', 'anchor': '#services'},
            {'name': 'Мастера', 'url': 'landing', 'anchor': '#masters'},
            {'name': 'Запись', 'url': 'landing', 'anchor': '#booking'},
        ]
    }
