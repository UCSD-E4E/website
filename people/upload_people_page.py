'''Uploads the people and alumni page
'''
import argparse
import base64
import json
import os
from pathlib import Path

import requests
import yaml
from create_people_page import create_html


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
    parser.add_argument('yml', type=Path)
    args = parser.parse_args()
    people_data_path: Path = args.yml

    cred_file = Path('credentials.json')
    if cred_file.is_file():
        with open(cred_file, 'r', encoding='ascii') as handle:
            creds = json.load(handle)
    else:
        value = os.environ['WP_CREDS']
        creds = json.loads(value)

    with open(people_data_path, 'r', encoding='ascii') as handle:
        data = yaml.safe_load(handle)

    people_html, alumni_html = create_html(data)

    update_page_content(
        wp_domain='https://e4e.ucsd.edu',
        username=creds['username'],
        password=creds['password'],
        page_id=5303,
        html_content=people_html
    )
    update_page_content(
        wp_domain='https://e4e.ucsd.edu',
        username=creds['username'],
        password=creds['password'],
        page_id=5354,
        html_content=alumni_html
    )

if __name__ == '__main__':
    main()
