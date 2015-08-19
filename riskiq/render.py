import os

from jinja2 import Template, Environment, PackageLoader

def renderer(data, template_file, custom_template=None,
        verbose=False, oneline=False):
    """
    Render the template with supplied context.
    Example template_file: "blacklist/lookup"

    """
    if custom_template:
        with open(custom_template) as f:
            template = Template(f.read())
        return template.render(data=data, verbose=verbose).encode('utf-8')
    if oneline:
        template_file += '_oneline'
    env = Environment(loader=PackageLoader('riskiq', 'templates'))
    template = env.get_template(template_file)
    return template.render(data=data, verbose=verbose).encode('utf-8').rstrip()
