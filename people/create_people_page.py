'''Creates the people page
'''
import argparse
import datetime as dt
from pathlib import Path
from typing import Dict, List, Tuple

import yaml
from schema import Optional, Or, Schema

levels_map = {
    "Project Candidate": 1,
    "Project Member": 2,
    "Project Lead": 4,
    "Staff Engineer": 5,
    "E4E Director": 6,
    "Project Member - Alumni": 22,
    "Project Lead - Alumni": 24,
    "Former Staff Engineer": 25,
    "Former E4E Director": 26
}

base_level_headings = {
    1: "Project Candidates",
    2: "Project Member",
    4: "Project Leads",
    5: "Staff Engineers",
    6: "E4E Directors",
    22: "Project Member - Alumni",
    24: "Project Lead - Alumni",
    25: "Former Staff Engineers",
    26: "Former E4E Directors"
}

section_output = {
    1: ("<!-- wp:list -->\n<ul>\n", "</ul>\n<!-- /wp:list -->\n"),
    2: ("", ""),
    3: ("", ""),
    4: ("", ""),
    5: ("", ""),
    6: ("", ""),
    22: ("", ""),
    23: ("", ""),
    24: ("", ""),
    25: ("", ""),
    26: ("", "")
}

def standard_html(name: str, desc: str, img: str, expedition: bool, link: str) -> str:
    """Standard HTML output

    Args:
        name (str): Name
        desc (str): Description
        img (str): Image URL
        expedition (bool): Expedition flag
        link (str): link

    Returns:
        str: HTML block
    """
    title = name
    alt_title = name
    url = img
    description = desc
    html = ""
    if link == "":
        link = None

    if expedition:
        title += "*"
    html += "<!-- wp:html -->\n"
    html += "<div class=\"personnel\">\n"
    html += f'<p><img class="profileimg" title="{alt_title}" src="{url}" alt="{alt_title}">'
    html += '</p>\n'
    if link:
        html += f'<p class="projecttitle"><a href="{link}">{title}</a></p>\n'
    else:
        html += f'<p class="projecttitle">{title}</p>\n'
    html += f'<p class="projectdescription">{description}</p>\n'
    html += '</div>\n'
    html += '<!-- /wp:html -->\n'
    html += '\n'
    return html

def minimal_html(name: str, desc: str, img: str, expedition: bool, link: str) -> str:
    """Minimal output

    Args:
        name (str): Name
        desc (str): Description
        img (str): Image link
        expedition (bool): Expedition flag
        link (str): Link

    Returns:
        str: HTML Block
    """
    # pylint: disable=unused-argument
    title = name
    html = ""
    if expedition:
        title += "*"

    html += f'<li>{title} - {desc}</li>\n'
    return html

def no_output(nname: str, desc: str, img: str, expedition: bool, link: str) -> str:
    """No output

    Args:
        nname (str): Name
        desc (str): Description
        img (str): Image link
        expedition (bool): Expedition flag
        link (str): link

    Returns:
        str: HTML block
    """
    # pylint: disable=unused-argument
    return ""

def check_url(url: str) -> bool:
    """Checks that this is an image

    Args:
        url (str): URL to image

    Returns:
        bool: True if image, otherwise False
    """
    if not isinstance(url, str):
        return False
    # if requests.head(url).status_code > 400:
    #     return False
    return True

level_formatters = {
    1: no_output,
    2: standard_html,
    3: standard_html,
    4: standard_html,
    5: standard_html,
    6: standard_html,
    22: standard_html,
    23: standard_html,
    24: standard_html,
    25: standard_html,
    26: standard_html
}

def create_alumni_page(data: Dict) -> str:
    """Creates the Alumni page

    Args:
        data (Dict): Dictionary of people data

    Returns:
        str: HTML of Alumni page
    """
    alumni_page_order = [
        26, 25, 24, 23, 22
    ]

    html = ''
    html += "<!-- wp:paragraph -->\n"
    html += ("<p>* Denotes people that have participated in one of our "
            "<a href=\"http://e4e.ucsd.edu/expeditions\">expeditions/deployments</a>.</p>\n")
    html += "<!-- /wp:paragraph -->\n"
    html += "\n"
    for level in alumni_page_order:
        people = [person for person in data if levels_map[person['level']] == level]

        if len(people) > 0:
            html += '<!-- wp:heading -->\n'
            html += f'<h2 class="wp-block-heading">{base_level_headings[level]}</h2>\n'
            html += '<!-- /wp:heading -->\n'
            html += '\n'

            html += section_output[level][0]

        for person in sorted(people, key=lambda x: (x['end'], x['start'])):
            title = person["name"]
            image = person["image"]
            description = person["description"]
            expedition = person["expedition"]
            link = person["link"]
            html += level_formatters[level](title, description, image, expedition, link)

        html += section_output[level][1]

    html += '<!-- wp:heading -->\n'
    html += f'<h2 class="wp-block-heading"></h2>\n'
    html += '<!-- /wp:heading -->\n'
    html += '\n'

    html += '<!-- wp:paragraph -->\n'
    html += f'<p>Updated {dt.datetime.now().isoformat(timespec="seconds")}</p>\n'
    html += '<!-- /wp:paragraph -->\n'
    html += '\n'
    return html

def main():
    """Main application logic
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('yml', type=Path)
    args = parser.parse_args()

    people_data_path: Path = args.yml

    with open(people_data_path, 'r', encoding='ascii') as handle:
        data = yaml.safe_load(handle)

    people_html, alumni_html = create_html(data)

    with open('people.html', 'w', encoding='ascii') as handle:
        handle.write(people_html)

    with open("alumni.html", 'w', encoding='ascii') as file:
        file.write(alumni_html)

def create_html(data: Dict) -> Tuple[str, str]:
    schema = Schema([
        {
            'name': str,
            Optional('image',
                     default="http://e4e.ucsd.edu/wp-content/uploads/blank-profile-drawing.png"):
                     Schema(check_url),
            'description': str,
            'start': int,
            Optional('end', default=9999): int,
            'level': Or(
                "Project Candidate",
                "Project Member",
                "Project Lead",
                "Staff Engineer",
                "E4E Director",
                "Project Member - Alumni",
                "Project Lead - Alumni",
                "Former Staff Engineer",
                "Former E4E Director"
            ),
            Optional('link', default=None): Schema(check_url),
            Optional('expedition', default=False): bool
        }
    ])
    valid_data: List[Dict] = schema.validate(data)

    people_html = create_people_page(valid_data)
    alumni_html = create_alumni_page(valid_data)
    return people_html,alumni_html

def create_people_page(valid_data: Dict) -> str:
    """Creates the People page

    Args:
        valid_data (Dict): Dictionary of data

    Returns:
        str: HTML of People page
    """
    people_page_order = [
        6, 5, 4, 3, 2
    ]

    html = ''
    html += "<!-- wp:paragraph -->\n"
    html += ("<p>* Denotes people that have participated in one of our "
             "<a href=\"http://e4e.ucsd.edu/expeditions\">expeditions/deployments</a>.</p>\n")
    html += "<!-- /wp:paragraph -->\n"
    html += "\n"

    for level in people_page_order:
        people = [person for person in valid_data if levels_map[person['level']] == level]
        if len(people) > 0:
            html += "<!-- wp:heading -->\n"
            html += f"<h2>{base_level_headings[level]}</h2>\n"
            html += "<!-- /wp:heading -->\n"
            html += "\n"

            html += section_output[level][0]

        for person in sorted(people, key=lambda x: (x['end'], x['start'])):
            title = person["name"]
            image = person["image"]
            description = person["description"]
            expedition = person["expedition"]
            link = person["link"]
            html += level_formatters[level](title, description, image, expedition, link)

        html += section_output[level][1]

    html += '<!-- wp:heading -->\n'
    html += f'<h2 class="wp-block-heading"></h2>\n'
    html += '<!-- /wp:heading -->\n'
    html += '\n'

    html += '<!-- wp:paragraph -->\n'
    html += f'<p>Updated {dt.datetime.now().isoformat(timespec="seconds")}</p>\n'
    html += '<!-- /wp:paragraph -->\n'
    html += '\n'
    return html

if __name__ == '__main__':
    main()
