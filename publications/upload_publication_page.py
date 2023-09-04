'''Uploads the people and alumni page
'''
import argparse
import base64
import json
import os
import subprocess
from pathlib import Path

import requests
import yaml


def update_page_content(wp_domain: str,
                        username: str,
                        password: str,
                        page_id: int,
                        html_content: str) -> None:
    url = f'{wp_domain}/wp-json/wp/v2/pages/{page_id}'
    token = base64.b64encode(f'{username}:{password}'.encode()).decode()
    header = {
        'Authorization': f'Basic {token}'
    }
    body = {
        'content': html_content
    }
    response = requests.post(
        url=url,
        headers=header,
        json=body,
        timeout=60
    )
    if response.status_code != 200:
        raise RuntimeError

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('bib_file', type=Path)
    args = parser.parse_args()
    bib_file: Path = args.bib_file

    cred_file = Path('credentials.json')
    if cred_file.is_file():
        with open(cred_file, 'r', encoding='ascii') as handle:
            creds = json.load(handle)
    else:
        value = os.environ['WP_CREDS']
        creds = json.loads(value)

    subprocess.run(['bibtex2html',
                        '--warn-error',
                        '--sort-by-date',
                        '--reverse-sort',
                        '--nobibsource',
                        '-nofooter',
                        '--nodoc',
                        '--dl',
                        '--style', 'ieeetr',
                        '--no-header',
                        '--html-entities',
                        '--quiet',
                        bib_file.as_posix()], check=True)
    with open(bib_file.with_suffix('.html'), 'r', encoding='utf-8') as handle:
        html = ''
        for line in handle:
            html += line

    update_page_content(
        wp_domain='https://e4e.ucsd.edu',
        username=creds['username'],
        password=creds['password'],
        page_id=5522,
        html_content=html
    )

if __name__ == '__main__':
    main()
