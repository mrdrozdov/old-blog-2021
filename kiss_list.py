import argparse
import os

from kiss_utils import write_html, get_page_name
from kiss_utils import BlogPostReader, JinjaRenderer


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--posts', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--templates', type=str, required=True)
    parser.add_argument('--template_name', type=str, required=True)
    parser.add_argument('--slug', type=str, required=True)
    parser.add_argument('--group_slug', type=str, required=True)
    options = parser.parse_args()

    posts_path = options.posts
    output_path = options.output
    templates_path = options.templates
    template_name = options.template_name
    slug = options.slug
    group_slug = options.group_slug

    jinja_renderer = JinjaRenderer(templates_path)
    blogpost_reader = BlogPostReader()

    group = []

    for filename in os.listdir(posts_path):
        input_path = os.path.join(posts_path, filename)
        config = blogpost_reader.get_config(input_path)

        if config.get('draft', False):
            continue

        config['url'] = get_page_name(group_slug, config)

        group.append(config)

    # Use the markdown body and any other configuration to generate the html with jinja.
    html = jinja_renderer.render(template_name, group=group, **config)

    target = get_page_name(output_path, dict(slug=slug))
    
    write_html(target, html)
