# Website Publications List

This folder contains the scripts to generate the code to put into http://e4e.ucsd.edu/publications.

## Adding a new publication

1. Obtain the BibTeX citation for the publication.  For example, the article "Small Unmanned Aerial Vehicle System for Wildlife Radio Collar Tracking", published at https://ieeexplore.ieee.org/document/7035779, provides a button "Cite This" that allows you to generate the BibTeX entry.
2. Ensure the BibTeX entry contains the following fields:
	- `title`
	- `author`
	- `url`
	- `abstract`
	- `year`
	- `month`
	- If the publication is part of a journal or conference article, ensure the following fields are present:
		- `booktitle` (name of journal/conference)
		- `DOI`
		- `volume` (can be `{}`)
		- `number` (can be `{}`)
		- `pages` (can be `{}`)
		- `keywords`
3. Set the BibTeX key as follows: first three last names separated by underscores, followed by "et al" if more than three authors, followed by the abbreviated journal/conference/publisher, followed by the year.  If more than one entry matches the same key, suffix this with "\_2" for the second publication, "\_3" for the third, and so on.
4. Append the BibTeX entry to `publications.bib`.  Ideally, format the same as the other entries.
5. Run `createHTML.sh`.
6. Copy the entire contents of `publications.html` into the HTML box on http://e4e.ucsd.edu/publications and publish.

## Requirements
1.  `bibtex2html`
