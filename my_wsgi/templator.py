"""Connecting templates with wsgi."""

from os.path import join

from jinja2 import Template


def render(template_name, folder='templates', **kwargs):
    """
    Open and read templates context
    and render template with context-parameters.
    """
    template_path = join(folder, template_name)

    with open(template_path, 'r', encoding='utf-8') as f:
        template = Template(f.read())

    return template.render(**kwargs)


