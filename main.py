import yaml

from jinja2 import Environment, PackageLoader, select_autoescape

import sys
import os
from os import listdir
from os.path import isfile, join


def parse_config(fn):
    start_match = '---'
    end_match = '---'

    started = False

    lines = []

    with open(fn) as f:
        for line in f:
            if not started and line.strip() == start_match:
                started = True
                continue
            elif started and line.strip() == end_match:
                break
            elif started:
                lines.append(line)

    outp = ''.join(lines)
    config = yaml.load(outp)

    return config


def parse_data(fn):
    start_match = '---'
    end_match = '---'

    started = False
    finished = False

    lines = []

    with open(fn) as f:
        for line in f:
            if not finished and not started and line.strip() == start_match:
                started = True
                continue
            elif not finished and started and line.strip() == end_match:
                finished = True
                continue
            elif finished:
                lines.append(line)

    outp = ''.join(lines)

    return outp

blog_config = 'blog.yaml'
if len(sys.argv) > 1:
    blog_config = sys.argv[1]
settings = yaml.load(open(blog_config))

env = Environment(
    loader=PackageLoader(settings['package_name'], settings['package_templates']),
    # autoescape=select_autoescape(['html', 'xml'])
)

post_template = env.get_template(settings['post_template'])
blog_template = env.get_template(settings['blog_template'])
home_template = env.get_template(settings['home_template'])
papers_template = env.get_template(settings['papers_template'])
about_template = env.get_template(settings['about_template'])

path_to_posts = settings['path_to_posts']

path_to_public_posts = settings['path_to_public_posts']
path_to_public_blog = settings['path_to_public_blog']
path_to_public_home = settings['path_to_public_home']
path_to_public_papers = settings['path_to_public_papers']
path_to_public_about = settings['path_to_public_about']

slug_prefix = settings['slug_prefix']

# Render Posts
# ------------

fns = [fn for fn in listdir(path_to_posts) if isfile(join(path_to_posts, fn))]

posts = []

for i, fn in enumerate(fns):
    fn = os.path.join(path_to_posts, fn)
    config = parse_config(fn)
    data = parse_data(fn)

    post = post_template.render(body=data, **config)

    slug = config.get('slug', None)
    if not slug:
        raise ValueError('Error: Must include `slug` for each post (post: {}).'.format(fn))

    if not slug.endswith('.html'):
        slug = slug + '.html'
    fn_out = os.path.join(path_to_public_posts, slug)

    with open(fn_out, 'w') as f:
        f.write(post)

    posts.append(dict(
        url=os.path.join(slug_prefix, slug),
        title=config['title'],
        ))

# Render Blog
# -----------

blog = blog_template.render(posts=posts)
with open(path_to_public_blog, 'w') as f:
    f.write(blog)

# Render Home
# -----------
home = home_template.render()
with open(path_to_public_home, 'w') as f:
    f.write(home)

# Render Papers
# -------------
papers = papers_template.render()
with open(path_to_public_papers, 'w') as f:
    f.write(papers)

# Render About
# ------------
about = about_template.render()
with open(path_to_public_about, 'w') as f:
    f.write(about)
