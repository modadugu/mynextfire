#!/usr/bin/env python3
"""
Convert WordPress XML export to Jekyll markdown posts
"""

import xml.etree.ElementTree as ET
import re
import os
from datetime import datetime
from urllib.parse import unquote

def clean_filename(title):
    """Convert title to a valid filename"""
    # Remove special characters and replace spaces with hyphens
    filename = re.sub(r'[^\w\s-]', '', title)
    filename = re.sub(r'[-\s]+', '-', filename)
    return filename.lower()[:50]  # Limit length

def extract_cdata(text):
    """Extract CDATA content if present"""
    if text is None:
        return ""
    # Remove CDATA markers if present
    text = text.strip()
    if text.startswith('<![CDATA[') and text.endswith(']]>'):
        text = text[9:-3]
    return text

def parse_date(date_str):
    """Parse WordPress date string to Jekyll format"""
    try:
        # WordPress format: "2025-03-02 22:59:12"
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%Y-%m-%d %H:%M:%S %z")
    except:
        return date_str

def convert_html_to_markdown(html_content):
    """Basic HTML to Markdown conversion"""
    if not html_content:
        return ""
    
    # Remove HTML tags but keep content (basic approach)
    # For better conversion, you might want to use html2text library
    text = html_content
    
    # Convert common HTML tags
    text = re.sub(r'<h1>(.*?)</h1>', r'# \1', text, flags=re.DOTALL)
    text = re.sub(r'<h2>(.*?)</h2>', r'## \1', text, flags=re.DOTALL)
    text = re.sub(r'<h3>(.*?)</h3>', r'### \1', text, flags=re.DOTALL)
    text = re.sub(r'<strong>(.*?)</strong>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<em>(.*?)</em>', r'*\1*', text, flags=re.DOTALL)
    text = re.sub(r'<a href="(.*?)">(.*?)</a>', r'[\2](\1)', text, flags=re.DOTALL)
    text = re.sub(r'<img[^>]*src="([^"]*)"[^>]*>', r'![](\1)', text)
    text = re.sub(r'<p>(.*?)</p>', r'\1\n\n', text, flags=re.DOTALL)
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<li>(.*?)</li>', r'- \1', text, flags=re.DOTALL)
    
    # Remove remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Decode HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#8217;', "'")
    text = text.replace('&#8220;', '"')
    text = text.replace('&#8221;', '"')
    text = text.replace('&#8211;', '-')
    text = text.replace('&#8212;', '--')
    
    return text.strip()

def parse_wordpress_xml(xml_file):
    """Parse WordPress XML export file"""
    print(f"Parsing {xml_file}...")
    
    # Parse XML with namespace handling
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Define namespaces
    namespaces = {
        'content': 'http://purl.org/rss/1.0/modules/content/',
        'wp': 'http://wordpress.org/export/1.2/',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'excerpt': 'http://wordpress.org/export/1.2/excerpt/'
    }
    
    posts = []
    items = root.findall('.//item')
    
    print(f"Found {len(items)} items in XML")
    
    for item in items:
        # Check if this is a post (not attachment or page)
        post_type_elem = item.find('wp:post_type', namespaces)
        if post_type_elem is None:
            continue
        
        post_type = extract_cdata(post_type_elem.text)
        if post_type != 'post':
            continue
        
        # Check if post is published
        status_elem = item.find('wp:status', namespaces)
        if status_elem is not None:
            status = extract_cdata(status_elem.text)
            if status not in ['publish', '']:
                continue
        
        # Extract post data
        title_elem = item.find('title')
        title = extract_cdata(title_elem.text) if title_elem is not None else "Untitled"
        
        # Get post date
        post_date_elem = item.find('wp:post_date', namespaces)
        post_date = extract_cdata(post_date_elem.text) if post_date_elem is not None else ""
        
        # Get content
        content_elem = item.find('content:encoded', namespaces)
        content = extract_cdata(content_elem.text) if content_elem is not None else ""
        
        # Get excerpt
        excerpt_elem = item.find('excerpt:encoded', namespaces)
        excerpt = extract_cdata(excerpt_elem.text) if excerpt_elem is not None else ""
        
        # Get categories
        categories = []
        for category in item.findall('category'):
            domain = category.get('domain', '')
            if domain == 'category':
                cat_name = extract_cdata(category.text)
                if cat_name:
                    categories.append(cat_name)
        
        # Get tags
        tags = []
        for category in item.findall('category'):
            domain = category.get('domain', '')
            if domain == 'post_tag':
                tag_name = extract_cdata(category.text)
                if tag_name:
                    tags.append(tag_name)
        
        # Get author
        creator_elem = item.find('dc:creator', namespaces)
        author = extract_cdata(creator_elem.text) if creator_elem is not None else ""
        
        posts.append({
            'title': title,
            'date': post_date,
            'content': content,
            'excerpt': excerpt,
            'categories': categories,
            'tags': tags,
            'author': author
        })
    
    print(f"Found {len(posts)} blog posts")
    return posts

def create_jekyll_post(post, output_dir='_posts'):
    """Create a Jekyll markdown post file"""
    # Parse date
    try:
        dt = datetime.strptime(post['date'], "%Y-%m-%d %H:%M:%S")
        date_str = dt.strftime("%Y-%m-%d")
        time_str = dt.strftime("%H:%M:%S +0000")  # Add timezone
    except:
        date_str = "2024-01-01"
        time_str = "12:00:00 +0000"
    
    # Create filename
    filename = clean_filename(post['title'])
    if not filename:
        filename = "untitled-post"
    
    filename = f"{date_str}-{filename}.md"
    filepath = os.path.join(output_dir, filename)
    
    # Create front matter
    front_matter = "---\n"
    front_matter += f"layout: post\n"
    front_matter += f"title: \"{post['title'].replace('"', '\\"')}\"\n"
    front_matter += f"date: {date_str} {time_str}\n"
    
    if post['categories']:
        front_matter += f"categories: {post['categories']}\n"
    
    if post['tags']:
        # Format tags as YAML list
        if len(post['tags']) == 1:
            front_matter += f"tags: {post['tags'][0]}\n"
        else:
            front_matter += "tags:\n"
            for tag in post['tags']:
                front_matter += f"  - {tag}\n"
    
    if post['author']:
        front_matter += f"author: {post['author']}\n"
    
    front_matter += "---\n\n"
    
    # Convert content to markdown
    content = convert_html_to_markdown(post['content'])
    
    # Combine front matter and content
    post_content = front_matter + content
    
    # Write file
    os.makedirs(output_dir, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(post_content)
    
    return filepath

def main():
    xml_file = r"c:\Users\modad\Downloads\mynextfire.WordPress.2026-01-18.xml"
    output_dir = "_posts"
    
    if not os.path.exists(xml_file):
        print(f"Error: XML file not found: {xml_file}")
        return
    
    # Parse WordPress XML
    posts = parse_wordpress_xml(xml_file)
    
    if not posts:
        print("No posts found to convert.")
        return
    
    # Convert each post
    print(f"\nConverting {len(posts)} posts to Jekyll format...")
    for i, post in enumerate(posts, 1):
        filepath = create_jekyll_post(post, output_dir)
        print(f"[{i}/{len(posts)}] Created: {filepath}")
    
    print(f"\nSuccessfully converted {len(posts)} posts to Jekyll format!")
    print(f"Posts saved in: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    main()

