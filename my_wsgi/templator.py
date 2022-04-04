"""Connecting templates with wsgi."""

from os.path import join

from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    """
    Open and read templates context
    and render template with context-parameters.
    """
    environment = Environment()
    environment.loader = FileSystemLoader(folder)
    template = environment.get_template(template_name)
    return template.render(**kwargs)


