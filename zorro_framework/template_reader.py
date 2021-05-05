from jinja2 import FileSystemLoader, select_autoescape
from jinja2 import Environment


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон
    :param kwargs: параметры
    :return:
    """

    env = Environment(
        loader=FileSystemLoader(folder),
        autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template(template_name)
    return template.render(**kwargs)
