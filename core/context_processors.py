def menu_context(request):
    """����������� ��������� ��� �������� ������ ���� �� ��� �������"""
    return {
        'menu_items': [
            {'name': '�������', 'url': 'landing', 'anchor': '#home'},
            {'name': '� ���', 'url': 'landing', 'anchor': '#about'},
            {'name': '������', 'url': 'landing', 'anchor': '#services'},
            {'name': '�������', 'url': 'landing', 'anchor': '#masters'},
            {'name': '������', 'url': 'landing', 'anchor': '#booking'},
        ]
    }
