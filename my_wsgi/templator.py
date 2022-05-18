"""Connecting templates with wsgi."""

from os.path import join

from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', static_url = '/static/', **kwargs):
    """
    Open and read templates context
    and render template with context-parameters.
    """
    environment = Environment()  # определяет среду окружения шаблонизатора jinja2
    environment.loader = FileSystemLoader(folder)
    environment.globals['static'] = static_url   # подключаем статику
    template = environment.get_template(template_name)
    return template.render(**kwargs)


