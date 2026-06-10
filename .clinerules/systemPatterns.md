# System Patterns: AIX Leuphana Website

## System Architecture
- Static site generation using Jekyll
- Content-driven architecture with Markdown files
- Component-based design with reusable includes
- SCSS-based styling with modular partials
- GitHub Pages deployment infrastructure

## Key Technical Decisions
- **Jekyll Framework**: Chosen for its simplicity and GitHub Pages integration
- **Markdown Content**: Enables easy content management by non-technical users
- **Modular Components**: Header, footer, and social components as reusable includes
- **SCSS Organization**: Styles organized into partials for maintainability
- **Static Generation**: Fast, secure, and reliable deployment

## Design Patterns in Use
- **Separation of Concerns**: Content (Markdown) separate from presentation (HTML/SCSS)
- **Component Reusability**: Includes system for shared UI elements
- **Data-driven Content**: Team and publication data managed through structured Markdown files
- **Responsive Design**: Mobile-first approach with media queries
- **Semantic HTML**: Accessible and meaningful markup structure

## Component Relationships
- **Core Structure**: _config.yml defines site configuration and global settings
- **Content Files**: Markdown files in root and _posts directory
- **Includes**: Reusable HTML components in _includes directory
- **Styles**: SCSS files in _sass directory compiled to main.css
- **Assets**: Images, logos, and other media in assets directory

## Critical Implementation Paths
- **Content Management**: Markdown files for easy editing and version control
- **Build Process**: Jekyll build system with GitHub Pages integration
- **Deployment**: Automated deployment through GitHub Pages
- **Styling**: SCSS compilation to optimized CSS
- **Asset Management**: Organized asset structure for maintainability