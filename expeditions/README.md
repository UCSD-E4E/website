# Expeditions List
This folder contains the scripts to generate the code to put into https://e4e.ucsd.edu/expeditions

## Adding a new expedition
1. Open `expeditions.yml`
2. At the bottom of the file, add a new entry:
```
- project: 
  location:
  year:
  month:
  link:
  media:
    - 
  lead:
    - 
  people:
    - 
  data:
    - 
  properties:
```

If any of these fields are not to be used, remove them.

Entries should following the below schema:
```
{
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "project": {
                "type": "string"
            },
            "location": {
                "type": "string"
            },
            "year": {
                "type": "integer"
            },
            "month": {
                "type": "string"
            },
            "link": {
                "type": "string",
                "default": ""
            },
            "media": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "default": []
            },
            "lead": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "default": []
            },
            "people": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "default": []
            },
            "data": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "default": []
            },
            "properties": {
                "type": "object"
            }
        },
        "required": [
            "project",
            "location",
            "year",
            "month"
        ],
        "additionalProperties": false
    },
    "$id": "",
    "$schema": "http://json-schema.org/draft-07/schema#"
}
```
3. Commit the change to a new branch (recommend naming the branch `YYYY-MM.PROJECT.LOCATION`)
4. Open a pull request to main

## Website admins
1. Verify that all information has been completed
2. Approve pull request
3. Download the build artifact
4. Copy the entire contents of `expeditions.html` into the HTML box on https://e4e.ucsd.edu/expeditions and publish.
