import argparse
import os

from kiss_utils import write_html, get_page_name
from kiss_utils import BlogPostReader, JinjaRenderer, MarkdownRender


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
        html = jinja_renderer.render(template_name, body=markdown, **config)

        target = get_page_name(output_path, config)
        
        write_html(target, html)
