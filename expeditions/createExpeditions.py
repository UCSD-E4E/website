'''Creates the expeditions page
'''
import argparse
import datetime as dt
from pathlib import Path
from typing import List, Dict
import pandas as pd
import yaml
from schema import Optional, Schema


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('yml', type=Path)
    args = parser.parse_args()
    with open(args.yml, 'r', encoding='ascii') as handle:
        data = yaml.safe_load(handle)
    schema = Schema(
        [
            {
                "project": str,
                'location': str,
                'year': int,
                'month': str,
                Optional('link', default=''): str,
                Optional('media', default=[]): [str],
                Optional('lead', default=[]): [str],
                Optional('people', default=[]): [str],
                Optional('data', default=[]): [str],
                Optional('properties'): dict
            }
        ]
    )
    valid_data: List[Dict] = schema.validate(data)
    for entry in valid_data:
        entry['date'] = dt.datetime.strptime(f'{entry["year"]} {entry["month"]}', "%Y %B").date()
    sorted_entries = sorted(valid_data, key=lambda x: x['date'])
    html = ''
    for entry in sorted_entries:
        # heading
        html += "<!-- wp:heading -->\n"
        if entry['link']:
            html += "<h2>"
            html += "<a href=\"%s\" data-type=\"URL\" data-id=\"%s\">" % (entry['link'], entry['link'])
            html += "%s" % (entry['project'])
            html += "</a>"
            html += " - %s %s" % (entry['month'], entry['year'])
            
            html += "</h2>"
            html += "\n"
        else:
            html += "<h2>%s - %s %s</h2>\n" % (entry['project'], entry['month'], entry['year'])
        html += "<!-- /wp:heading -->\n"
        html += "\n"
        
        # Location
        html += "<!-- wp:paragraph -->\n"
        html += "<p><strong>Location:</strong> %s</p>\n" % (entry["location"])
        html += "<!-- /wp:paragraph -->\n"
        html += "\n"
        
        if len(entry['people']) > 0:
            # People
        #     html += "<!-- wp:paragraph -->\n"
        #     html += "<p>People:</p>\n"
        #     html += "<!-- /wp:paragraph -->\n"
        #     html += "\n"

            html += "<!-- wp:list -->\n"
            html += "<ul>"
            for person in entry['people']:
                html += "<li>%s</li>" % (person)
            html += "</ul\n"
            html += "<!-- /wp:list -->\n"
            html += "\n"
    with open('expeditions.html', 'w', encoding='ascii') as handle:
        handle.write(html)

if __name__ == '__main__':
    main()