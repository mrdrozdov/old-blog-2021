import yaml
import mistune

from jinja2 import Environment, PackageLoader, select_autoescape

import sys
import os
from os import listdir
from os.path import isfile, join
import shutil


def mkdirp(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        pass


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


class TemplateManager(object):
    def __init__(self, env, settings):
        super(TemplateManager, self).__init__()
        self.env = env
        self.settings = settings

    def add_page(self, template_name, public_name, **kwargs):
        public_path = self.settings[public_name]
        template = self.env.get_template(self.settings[template_name])
        data = template.render(**kwargs)
        with open(public_path, 'w') as f:
            f.write(data)


template_manager = TemplateManager(env, settings)


post_template = env.get_template(settings['post_template'])
path_to_posts = settings['path_to_posts']
path_to_public_posts = settings['path_to_public_posts']
post_slug_prefix = settings['post_slug_prefix']

paper_summary_template = env.get_template(settings['paper_summary_template'])
path_to_paper_summaries = settings['path_to_paper_summaries']
path_to_public_paper_summaries = settings['path_to_public_paper_summaries']
paper_summary_slug_prefix = settings['paper_summary_slug_prefix']

path_to_static = settings['path_to_static']
path_to_public_static = settings['path_to_public_static']


# Render Posts
# ------------

fns = [fn for fn in listdir(path_to_posts) if isfile(join(path_to_posts, fn))]

posts = []

for i, fn in enumerate(fns):
    fn = os.path.join(path_to_posts, fn)
    config = parse_config(fn)
    data = parse_data(fn)
    body = mistune.markdown(data, escape=False)

    post = post_template.render(body=body, **config)

    slug = config.get('slug', None)
    if not slug:
        raise ValueError('Error: Must include `slug` for each post (post: {}).'.format(fn))

    if not slug.endswith('.html'):
        slug = slug + '.html'
    fn_out = os.path.join(path_to_public_posts, slug)

    mkdirp(os.path.dirname(fn_out))
    with open(fn_out, 'w') as f:
        f.write(post)

    posts.append(dict(
        url=os.path.join(post_slug_prefix, slug),
        title=config['title'],
        ))

# Render Paper Summaries
# ----------------------

fns = [fn for fn in listdir(path_to_paper_summaries) if isfile(join(path_to_paper_summaries, fn))]

paper_summaries = []

for i, fn in enumerate(fns):
    fn = os.path.join(path_to_paper_summaries, fn)
    config = parse_config(fn)
    data = parse_data(fn)
    body = mistune.markdown(data, escape=False)

    post = paper_summary_template.render(body=body, **config)

    slug = config.get('slug', None)
    if not slug:
        raise ValueError('Error: Must include `slug` for each post (post: {}).'.format(fn))

    if not slug.endswith('.html'):
        slug = slug + '.html'
    fn_out = os.path.join(path_to_public_paper_summaries, slug)

    mkdirp(os.path.dirname(fn_out))
    with open(fn_out, 'w') as f:
        f.write(post)

    paper_summaries.append(dict(
        url=os.path.join(paper_summary_slug_prefix, slug),
        title=config['title'],
        ))

# Render Standalone Pages
# -----------------------

template_manager.add_page('blog_template', 'path_to_public_blog', posts=posts)
template_manager.add_page('summaries_template', 'path_to_public_summaries', paper_summaries=paper_summaries)
template_manager.add_page('home_template', 'path_to_public_home')
template_manager.add_page('papers_template', 'path_to_public_papers')
template_manager.add_page('about_template', 'path_to_public_about')

# Copy Static Data
# ----------------

for dir in os.listdir(path_to_static):
    source = os.path.join(path_to_static, dir)
    target = os.path.join(path_to_public_static, dir)
    mkdirp(os.path.dirname(target))
    shutil.rmtree(target)
    shutil.copytree(source, target)
