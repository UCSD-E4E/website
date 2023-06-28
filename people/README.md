# People Page
This folder contains the scripts to generate the code to put into https://e4e.ucsd.edu/people and https://e4e.ucsd.edu/alumni

# Adding a new person
1. Open `people.yml`
2. At the bottom of the document, add the following block:
```
- name: {full name}
  description: {current project and date}
  level: {current level}
  start: {starting year}
```
The description should be along the lines of "{project} since {year}".  In the case of any support group, it would be "{group} supporting {project} since {year}".

For example:
```
- name: John Doe
  description: Aye-Aye Sleep Monitoring since 2014
  level: Project Candidate
  start: 2014
```

The `people.yml` document follows the following schema:
```
[
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
]
```
Please ensure that any fields added comply with the above schema.

If adding a new image, please attach the image to the pull request, as the image needs to be uploaded to the E4E website.  If the only change request is to add an image, please open the appropriate GitHub issue.

Please see below for more information regarding mug shots.

3. Start a pull request and add the website admin as a reviewer.

## Photo Requirements
Photos should be a clear representative photo of each person, suitable for public distribution.  Submitted photos should be PNG or JPEG format, scaled to 200x200px.  Filename should be {year}_{name}.{ext}.