# MyNextFireBlog

A Jekyll-powered blog hosted on GitHub Pages.

## Setup

This repository is configured to work with GitHub Pages using Jekyll.

### Local Development

To run Jekyll locally:

1. Install Ruby and Bundler (if not already installed)
2. Install dependencies:
   ```bash
   bundle install
   ```
3. Run Jekyll server:
   ```bash
   bundle exec jekyll serve
   ```
4. Open your browser to `http://localhost:4000`

### Adding Blog Posts

Create new posts in the `_posts` directory using the format:
- `YYYY-MM-DD-post-title.md`

Each post should include front matter at the top:
```yaml
---
layout: post
title: "Your Post Title"
date: YYYY-MM-DD HH:MM:SS +0000
categories: category-name
---
```

### GitHub Pages

This site will automatically build and deploy when you push to the `main` branch (or `gh-pages` branch, depending on your repository settings).

## Structure

- `_config.yml` - Jekyll configuration
- `_layouts/` - HTML layouts (default, home, post)
- `_posts/` - Blog posts (Markdown files)
- `assets/` - CSS and JavaScript files
- `index.md` - Homepage

## License

This project is open source and available under the MIT License.
