#!/usr/bin/env python3
"""
Builds the notebook and checks out the relevant files into gh-pages
"""

import logging

import os
import shutil
import subprocess

import click

try:
    import ruamel.yaml as yaml
except ImportError:
    import yaml


def get_current_git_ref():
    # Gets the current branch_name for HEAD (or HEAD)
    branch_name = subprocess.check_output(
        ['git', 'rev-parse', '--symbolic-full-name', '--verify',
         '--abbrev-ref', 'HEAD'])
    branch_name = branch_name.decode().strip()

    if branch_name == 'HEAD':
        # Instead use the current commit if we're in detached head mode
        branch_name = subprocess.check_output(
            ['git', 'rev-parse', '--verify', 'HEAD']
        ).decode.strip()

    return branch_name


def make_slides(nb_path, template_path=None, reveal_prefix='reveal.js'):
    convert_cmd = [
        'jupyter', 'nbconvert',
        '--to=slides',
        '--reveal-prefix={}'.format(reveal_prefix)
    ]

    if template_path is not None:
        convert_cmd.append('--template={}'.format(template_path))

    convert_cmd.append(nb_path)

    return subprocess.check_call(convert_cmd)


@click.command()
@click.option('-c', '--config', type=click.Path(exists=True),
              default='build_config.yml')
def main(config):
    logging.getLogger().setLevel(logging.INFO)

    with open(config, 'r') as yf:
        conf_dict = yaml.safe_load(yf)

    # Build the slides
    nb_path = conf_dict.get('notebook', 'notebook.ipynb')
    template_path = conf_dict.get('template', None)
    reveal_prefix = conf_dict.get('reveal_prefix', None)

    kwargs = {}
    if template_path is not None:
        kwargs['template_path'] = template_path

    if reveal_prefix is not None:
        kwargs['reveal_prefix'] = reveal_prefix

    make_slides(nb_path, **kwargs)

    # Find the output location of the slides
    # TODO: Just set this in make_slides
    _, nb_fname = os.path.split(nb_path)
    assert nb_fname.endswith('.ipynb')
    slides_loc = nb_fname[0:-len('.ipynb')] + '.slides.html'

    if not os.path.exists(slides_loc):
        raise ValueError('Could not find {}'.format(slides_loc))

    cur_git_ref = get_current_git_ref()   # So we can check stuff out from here
    logging.info('Checking out gh-pages, leaving {}'.format(cur_git_ref))

    # Check out the gh-pages branch
    subprocess.check_call(['git', 'checkout', 'gh-pages'])

    # Move the slides to index.html to update them
    logging.info('Moving slides from {} to index.html'.format(slides_loc))

    shutil.move('index.html', 'index.html.bak')
    try:
        shutil.move(slides_loc, 'index.html')

        # Update the remaining files
        logging.info('Checking out specified data from {}'.format(cur_git_ref))
        subprocess.check_call(
            ['git', 'checkout', cur_git_ref] +
            conf_dict.get('files', []) +            # Standalone files
            conf_dict.get('dirs', [])               # Directories
        )
    except:
        shutil.move('index.html.bak', 'index.html')
        raise
    finally:
        if os.path.exists('index.html.bak'):
            os.remove('index.html.bak')

if __name__ == "__main__":
    main()
