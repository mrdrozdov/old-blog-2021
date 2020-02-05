import argparse
import os

from kiss_utils import write_html, get_page_name
from kiss_utils import JinjaRenderer


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--slug', type=str, required=True)
    parser.add_argument('--templates', type=str, required=True)
    parser.add_argument('--template_name', type=str, required=True)
    options = parser.parse_args()

    output_path = options.output
    templates_path = options.templates
    template_name = options.template_name
    slug = options.slug

    jinja_renderer = JinjaRenderer(templates_path)
    html = jinja_renderer.render(template_name)
    target = get_page_name(output_path, dict(slug=slug))
    
    write_html(target, html)
