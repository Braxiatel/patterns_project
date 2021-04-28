def add_closing_slash(path):
    # добавление закрывающего слеша
    if not path.endswith('/'):
        path = f'{path}/'
    return path
