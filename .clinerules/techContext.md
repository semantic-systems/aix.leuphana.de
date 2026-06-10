# Technical Context: AIX Leuphana Website

## Technologies Used
- **Jekyll**: Static site generator (version specified in Gemfile)
- **Ruby**: Programming language for Jekyll (version managed by Bundler)
- **GitHub Pages**: Hosting and deployment platform
- **SCSS**: CSS preprocessor for styling
- **HTML5**: Semantic markup for content structure
- **Markdown**: Content format for easy editing

## Development Setup
- **Dependency Management**: Bundler for Ruby gem management
- **Build Process**: Jekyll build system with GitHub Pages integration
- **Version Control**: Git for source code management
- **Deployment**: Automated through GitHub Pages

## Technical Constraints
- **GitHub Pages Requirements**: Must use supported Jekyll plugins
- **Static Site Limitations**: No server-side processing or databases
- **Markdown Processing**: Content must be valid Markdown format
- **SCSS Compilation**: Styles must compile to valid CSS

## Dependencies
- **Ruby Gems**: Specified in Gemfile (jekyll, bundler, etc.)
- **GitHub Pages**: Requires specific Jekyll version compatibility
- **Browser Support**: Modern browsers with HTML5 and CSS3 support

## Tool Usage Patterns
- **Content Management**: Markdown files for easy editing and version control
- **Styling**: SCSS partials organized by component/function
- **Component Reuse**: Includes system for shared UI elements
- **Asset Management**: Organized structure for images and media
- **Configuration**: Centralized settings in _config.yml