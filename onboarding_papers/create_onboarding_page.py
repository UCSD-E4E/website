'''Creates the onboarding references page
'''
import argparse
import datetime as dt
import logging
import subprocess
from pathlib import Path
from typing import Dict, List

import yaml

def main():
    """Main application logic
    """
    logger = logging.getLogger('create_onboarding_page')
    logger.info('Starting')
    parser = argparse.ArgumentParser()
    parser.add_argument('config', action='store', type=Path)

    args = parser.parse_args()
    config_file = Path(args.config)
    with open(config_file, 'r', encoding='ascii') as handle:
        config: List[Dict[str, str]] = yaml.safe_load(handle)

    create_bib_html(config)

    html = create_html_page(config)

    with open('projects.html', 'w', encoding='utf-8') as handle:
        handle.write(html)

def create_html_page(config: List[Dict[str, str]]) -> str:
    """Creates the HTML WP Page

    Args:
        config (List[Dict[str, str]]): Config

    Returns:
        str: HTML wordpress body
    """
    config_entries = {entry['name']:entry for entry in config}
    html_files = {entry['name']:Path(entry['bib_file'] + '.html') for entry in config}
    html = ''

    with open('preamble.txt', 'r', encoding='utf-8') as handle:
        html += '<!-- wp:paragraph -->\n'
        html += '<p>'
        for line in handle:
            html += line
        html += '</p>\n'
        html += '<!-- /wp:paragraph -->\n\n'

    for name, html_file in html_files.items():
        config_entry = config_entries[name]
        html += '<!-- wp:heading -->\n'
        if 'url' in config_entry:
            heading_text = (f'<a href="{config_entry["url"]}" data-type="link" '
                           f'data-id="{config_entry["url"]}">{name}</a>')
        else:
            heading_text = f'{name}'
        html += f'<h2 class="wp-block-heading">{heading_text}</h2>\n'
        html += '<!-- /wp:heading -->\n'
        html += '\n'

        html += '<!-- wp:html -->\n'
        with open(html_file, 'r', encoding='UTF-8') as handle:
            for line in handle:
                html += line
        html += '\n<!-- /wp:html -->\n'
        html += '\n'

    html += '<!-- wp:paragraph -->\n'
    html += f'<p>Updated {dt.datetime.now().isoformat(timespec="seconds")}</p>\n'
    html += '<!-- /wp:paragraph -->\n'
    html += '\n'
    return html

def create_bib_html(config: List[Dict[str, str]]):
    """Creates the bibtex HTML

    Args:
        config (List[Dict[str, str]]): Configuration list
    """
    bib_files = [Path(entry['bib_file'] + '.bib') for entry in config]

    for bib_file in bib_files:
        subprocess.run(['bibtex2html',
                        '--warn-error',
                        '--sort-by-date',
                        '--nobibsource',
                        '-nofooter',
                        '--nodoc',
                        '--dl',
                        '--style', 'ieeetr',
                        '--no-header',
                        '--html-entities',
                        '--no-abstract',
                        '--no-keywords',
                        '--no-keys',
                        '--quiet',
                        bib_file], check=True)

if __name__ == '__main__':
    main()
