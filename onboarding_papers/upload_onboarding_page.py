'''Uploads the people and alumni page
'''
import argparse
import base64
import json
import os
from pathlib import Path
from typing import Dict, List

import requests
import yaml

from create_onboarding_page import create_bib_html, create_html_page


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
    parser.add_argument('config', type=Path)
    args = parser.parse_args()
    config_file: Path = args.config

    cred_file = Path('credentials.json')
    if cred_file.is_file():
        with open(cred_file, 'r', encoding='ascii') as handle:
            creds = json.load(handle)
    else:
        value = os.environ['WP_CREDS']
        creds = json.loads(value)

    with open(config_file, 'r', encoding='ascii') as handle:
        config: List[Dict[str, str]] = yaml.safe_load(handle)

    create_bib_html(config)

    html = create_html_page(config)

    update_page_content(
        wp_domain='https://e4e.ucsd.edu',
        username=creds['username'],
        password=creds['password'],
        page_id=6162,
        html_content=html
    )

if __name__ == '__main__':
    main()
