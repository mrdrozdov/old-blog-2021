import os
import json
import shutil
import yaml

from jinja2 import Environment, PackageLoader, select_autoescape

import mistune


# --- Utility Methods --- #

def mkdirp(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        pass


def rmdir(dir):
    try:
        shutil.rmtree(dir)
    except:
        pass


# --- Render --- #

class Renderer(object):
    def __init__(self, name, templates):
        super(Renderer, self).__init__()
        env = Environment(
            loader=PackageLoader(name, templates)
        )
        self.env = env
        self.cache = {}
        self.verbose = True

    def __cache(self, name, page, config):
        _config = dict(
            url=os.path.join(page['slug'], config['slug']),
            title=config.get('title', None),
            date=config.get('date', None),
            )
        _config.update(config)
        self.cache.setdefault(name, []).append(_config)

    def __group(self, name):
        return self.cache[name]

    def __parse_md_config(self, fn):
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

    def __parse_md_data(self, fn):
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

    def __render_jinja(self, path, template, **kwargs):
        if self.verbose:
            print("Rendering Jinja\n\tpath={}\n\ttemplate={}".format(
                path, template))
        template = self.env.get_template(template)
        post = template.render(**kwargs)
        with open(path, 'w') as f:
            f.write(post)

    def __render_markdown(self, path, template, fn, **kwargs):
        if self.verbose:
            print("Rendering Markdown\n\tpath={}\n\ttemplate={}\n\tfile={}".format(
                path, template, fn))
        config = self.__parse_md_config(fn)

        slug = config.get('slug', None)
        if not slug:
            raise ValueError('Error: Must include `slug` for each post (post: {}).'.format(fn))
        if not slug.endswith('.html'):
            config['slug'] = slug = slug + '.html'
        path = os.path.join(path, slug)

        if config.get('draft', False):
            return config

        if not config.get('norender', False):
            template = self.env.get_template(template)
            data = self.__parse_md_data(fn)
            body = mistune.markdown(data, escape=False)
            post = template.render(body=body, **config)
            with open(path, 'w') as f:
                f.write(post)

        return config

    def render(self, skeleton, page):
        if page['type'] == 'standalone':
            return self.render_standalone(skeleton, page)
        elif page['type'] == 'group':
            return self.render_group(skeleton, page)
        elif page['type'] == 'resource':
            return self.render_resource(skeleton, page)
        else:
            return False

    def render_standalone(self, skeleton, page):
        public_path = os.path.join(skeleton['public'], page['public'])
        public_dir = os.path.dirname(public_path)
        mkdirp(public_dir)

        kwargs = {}

        if 'group' in page:
            kwargs['group'] = self.__group(page['group'])

        style = page.get('style', 'jinja')

        if style == 'jinja':
            self.__render_jinja(public_path, page['template'], **kwargs)
        elif style == 'markdown':
            raise NotImplementedError("Standalone pages only support jinja style.")

        return True

    def __render_group(self, skeleton, page, fn):
        public_dir = os.path.join(skeleton['public'], page['public'])

        style = page.get('style', 'jinja')

        fn = os.path.join(page['source'], fn)

        if style == 'jinja':
            raise NotImplementedError("Groups only support markdown style.")
        elif style == 'markdown':
            config = self.__render_markdown(public_dir, page['template'], fn)

        if config.get('draft', False):
            return

        name = page.get('name', None)
        if name is not None:
            self.__cache(name, page, config)

    def render_group(self, skeleton, page):
        public_dir = os.path.join(skeleton['public'], page['public'])
        mkdirp(public_dir)

        source_dir = page['source']

        fns = [fn for fn in os.listdir(source_dir) 
               if os.path.isfile(os.path.join(source_dir, fn))]

        for fn in fns:
            self.__render_group(skeleton, page, fn)

        return True

    def render_resource(self, skeleton, page):
        public_dir = os.path.join(skeleton['public'], page['public'])

        shutil.copytree(page['source'], public_dir)
        return True


# --- Config --- #

def read_config(file):
    return json.load(open(file))


# --- Main --- #

def args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='skeleton.json',
                        help='Path to skeleton config file.')
    _args = parser.parse_args()
    return _args


def run(options):
    config = read_config(options.config)

    skeleton = config['skeleton']
    pages = skeleton['pages']

    rmdir(skeleton['public'])
    mkdirp(skeleton['public'])

    renderer = Renderer(skeleton['name'], skeleton['templates'])

    for _page in pages:
        renderer.render(skeleton, _page)


if __name__ == '__main__':
    options = args()
    run(options)
