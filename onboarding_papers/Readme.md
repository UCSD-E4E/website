# Onboarding Papers
Controls the source for https://e4e.ucsd.edu/onboarding-papers
## Configuration
In `projects.yml`, ensure that there is an entry for the project. `bib_file` should be the relative path to the `.bib` file without the file extension.  `name` should be the name displayed on the website.

## Usage
Add the `bibtex` entry for the desired papers into the corresponding `.bib` file and create a PR.  Once this is pushed to `main`, the website will update. You can inspect the output of the `Onboarding Page Build` GitHub Action to make sure that the HTML was made correctly.
