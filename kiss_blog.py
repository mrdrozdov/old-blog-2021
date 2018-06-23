import argparse
import os

import mistune
import yaml

from jinja2 import Environment, PackageLoader, select_autoescape


def touch_file(path):
    os.system('touch {}'.format(path))


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--posts', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--templates', type=str, required=True)
    parser.add_argument('--template_name', type=str, default='post.html')
    options = parser.parse_args()

    posts_path = options.posts
    output_path = options.output
    templates_path = options.templates
    template_name = options.template_name

    jinja_renderer = JinjaRenderer(templates_path)
    markdown_renderer = MarkdownRender()
    blogpost_reader = BlogPostReader()

    for filename in os.listdir(posts_path):
        input_path = os.path.join(posts_path, filename)
        config = blogpost_reader.get_config(input_path)

        if config.get('draft', False):
            continue

        # Extract the text body from the post file.
        body = blogpost_reader.get_body(input_path)

        # Convert the text body into rendered markdown.
        markdown = markdown_renderer.render(body)

        # Use the markdown body and any other configuration to generate the html with jinja.
        html = jinja_renderer.render(template_name, body=body, **config)

        target = get_page_name(output_path, config)
        
        write_html(target, html)
