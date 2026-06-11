# Team Members and Publications System

This document explains the new dynamic team members and publications system that has been implemented for the AIX Leuphana website.

## Overview

The system uses Jekyll collections to create a maintainable structure where:

1. **Team Members** can create their own personal pages
2. **Publications** can be added with links to GitHub pages
3. **Dynamic Generation** automatically updates the team and publications pages

## Team Members System

### Folder Structure
```
_team/
  template.md                # Template for creating new team member files
  ricardo-usbeck.md          # Sample implementation for Prof. Dr. Ricardo Usbeck
  [new-member-files].md      # Future team member files go here
```

### How to Add a New Team Member

1. **Copy the template**: Copy `_team/template.md` to `_team/[first-name-last-name].md`
2. **Fill in the details**: Edit the front matter with the team member's information
3. **Add an image**: Place the team member's photo in `assets/images/` (use lowercase with underscores, e.g., `john_doe.jpg`)
4. **Set the job category**: Use one of these categories:
   - `head`
   - `academic_advisor`
   - `research_assistant`
   - `research_associate`
   - `scholarship_holder`
   - `external_phd`
   - `student_assistant`
   - `alumni`

### Required Fields
- `name`: Full name
- `title`: Academic/Professional title
- `image`: Image filename (must be in `assets/images/`)
- `job_category`: One of the categories listed above

### Optional Fields
- `bio`: Short biography
- `research_interests`: List of research interests
- `email`: Contact email
- `website`: Personal website URL
- `github`: GitHub username
- `linkedin`: LinkedIn profile URL
- `office`: Office location

### Example
See `_team/ricardo-usbeck.md` for a complete example.

## Publications System

### Folder Structure
```
_publications/
  template.md                                # Template for creating new publication files
  georelating-inferring-disaster-affected-areas.md  # Sample publication
  [new-publication-files].md                 # Future publication files go here
```

### How to Add a New Publication

1. **Copy the template**: Copy `_publications/template.md` to `_publications/[publication-title].md`
2. **Fill in the details**: Edit the front matter with the publication information
3. **Include GitHub links**: Add both the repository URL and GitHub Pages URL if available

### Required Fields
- `title`: Publication title
- `authors`: List of authors
- `year`: Publication year
- `github_repo`: GitHub repository URL
- `github_page`: GitHub Pages URL (if available)

### Optional Fields
- `abstract`: Publication abstract
- `conference`: Conference name
- `doi`: DOI link
- `pdf`: PDF download link
- `website`: Publication website

### Example
See `_publications/georelating-inferring-disaster-affected-areas.md` for a complete example.

## How It Works

### Team Page Generation
The `team.markdown` file now uses Liquid templating to:

1. Group team members by their `job_category`
2. Display each member with their image and name
3. Link to their individual profile page
4. Automatically show only team members who have created their files

### Publications Page Generation
The `publications.markdown` file now uses Liquid templating to:

1. Group publications by year (newest first)
2. Display each publication with title, authors, and conference
3. Show a GitHub Page badge if available
4. Include a truncated abstract with "Read more" link
5. Link to the full publication page

### Individual Pages
Each team member and publication gets their own dedicated page with the layout defined in:
- `_layouts/team_member.html`
- `_layouts/publication.html`

## Configuration

The Jekyll configuration in `_config.yml` has been updated to include:

```yaml
collections:
  team:
    output: true
    permalink: /team/:path/
  publications:
    output: true
    permalink: /publications/:path/
```

## Usage

1. **Add your team member file** to the `_team/` directory
2. **Add your publication files** to the `_publications/` directory
3. **Run Jekyll** to generate the updated site
4. **Commit and push** your changes

The team and publications pages will automatically update to include your new entries!

## Notes

- Team members will only appear on the team page if they have created their personal file
- Publications will only appear if they have a GitHub repository link
- The system maintains the same visual style and categorization as the original site
- All individual pages include a "Back to [Team/Publications]" link for easy navigation