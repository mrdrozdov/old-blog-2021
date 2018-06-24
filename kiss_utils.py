import argparse
import os

import mistune
import yaml

from jinja2 import Environment, PackageLoader, select_autoescape


def write_html(path, html):
    with open(path, 'w') as f:
        f.write(html)


def get_page_name(path, config):
    try:
        slug = config['slug']
    except ValueError as e:
        # Slug must be included.
        raise e

    # Slug should end in html.
    if not slug.endswith('.html'):
        slug = slug + '.html'

    return os.path.join(path, slug)


class JinjaRenderer(object):
    def __init__(self, templates, name='blog'):
        loader = PackageLoader(name, templates)
        env = Environment(loader=loader)

        self.env = env

    def render(self, template_name, **kwargs):
        template = self.env.get_template(template_name)
        post = template.render(**kwargs)
        return post


class MarkdownRender(object):
    def render(self, body):
        data = mistune.markdown(body, escape=False)
        return data


class BlogPostReader(object):
    def get_config(self, path):
        start_match = '---'
        end_match = '---'

        started = False

        lines = []

        with open(path) as f:
            for line in f:
                if not started and line.strip() == start_match:
                    started = True
                    continue
                elif started and line.strip() == end_match:
                    break
                elif started:
                    lines.append(line)

        output = ''.join(lines)
        config = yaml.load(output)

        return config

    def get_body(self, path):
        start_match = '---'
        end_match = '---'

        started = False
        finished = False

        lines = []

        with open(path) as f:
            for line in f:
                if not finished and not started and line.strip() == start_match:
                    started = True
                    continue
                elif not finished and started and line.strip() == end_match:
                    finished = True
                    continue
                elif finished:
                    lines.append(line)

        output = ''.join(lines)

        return output
