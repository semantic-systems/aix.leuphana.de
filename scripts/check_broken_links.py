# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
#     "beautifulsoup4",
#     "pyyaml",
#     "python-dotenv",
#     "playwright",
#     "playwright-stealth"
# ]
# ///

import os
import requests
from bs4 import BeautifulSoup
import yaml
import glob
import re
import argparse
import time
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

# Automatically load the .env file in the current directory if it exists
load_dotenv()

def parse_frontmatter(file_path):
    """Extract YAML frontmatter from a Markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            pass
    return {}

def build_author_map():
    """Build a mapping of team member names to their email addresses."""
    author_map = {}
    team_files = glob.glob('_team/*.md') + glob.glob('_team/*.markdown')
    for tf in team_files:
        fm = parse_frontmatter(tf)
        name = fm.get('name')
        email = fm.get('email')
        if name and email:
            author_map[name.strip()] = email.strip()
    return author_map

def find_source_file_for_html(html_path):
    """Attempt to find the source markdown file for a given HTML file in _site/."""
    rel_path = os.path.relpath(html_path, '_site')
    parts = rel_path.split(os.sep)
    
    if len(parts) >= 2 and parts[-1] == 'index.html':
        collection = parts[0]
        slug = parts[-2]
        
        source_dirs = {
            'projects': '_projects',
            'team': '_team',
            'news': '_posts',
            'demos': '_demos',
            'publications': '_publications'
        }
        
        if collection in source_dirs:
            source_dir = source_dirs[collection]
            if collection == 'news':
                matches = glob.glob(f"{source_dir}/*-{slug}.*")
                if matches:
                    return matches[0]
            else:
                matches = glob.glob(f"{source_dir}/{slug}.*")
                if matches:
                    return matches[0]
    
    return None

def find_responsible_person(html_path):
    """Find the responsible person's name for a given page."""
    source_file = find_source_file_for_html(html_path)
    if not source_file:
        return None
        
    fm = parse_frontmatter(source_file)
    
    if 'author' in fm:
        return fm['author']
        
    if 'project_members' in fm and isinstance(fm['project_members'], list) and len(fm['project_members']) > 0:
        member = fm['project_members'][0]
        if isinstance(member, dict) and 'name' in member:
            return member['name']
        elif isinstance(member, str):
            return member
            
    if 'name' in fm:
        return fm['name']
        
    return None

def check_link_playwright(url, page):
    """Fallback check using playwright."""
    print(f"  [Fallback] Checking via Playwright Stealth: {url}")
    # Random sleep to mimic human behavior and avoid rate limits
    time.sleep(random.uniform(2.0, 4.0))
    try:
        response = page.goto(url, wait_until="domcontentloaded", timeout=15000)
        time.sleep(random.uniform(1.0, 2.0)) # Stay on page briefly like a human
        if response:
            return response.status < 400
        return False
    except Exception:
        return False

def check_link(url, page=None, base_url="http://localhost:4000"):
    """Check if a URL is broken."""
    if url.startswith('mailto:') or url.startswith('tel:'):
        return True
        
    if url.startswith('/'):
        local_path = os.path.join('_site', url.lstrip('/'))
        if os.path.isdir(local_path):
            local_path = os.path.join(local_path, 'index.html')
        elif not local_path.endswith('.html') and not '.' in os.path.basename(local_path):
            local_path += '.html'
            
        return os.path.exists(local_path)

    if url.startswith('http://') or url.startswith('https://'):
        # Small delay between external requests to avoid triggering WAFs
        time.sleep(random.uniform(0.5, 1.5))
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            resp = requests.head(url, headers=headers, allow_redirects=True, timeout=10)
            if resp.status_code >= 400 and resp.status_code != 405:
                resp = requests.get(url, headers=headers, stream=True, timeout=10)
                if resp.status_code >= 400 and page is not None:
                    return check_link_playwright(url, page)
                return resp.status_code < 400
            return resp.status_code < 400
        except requests.RequestException:
            if page is not None:
                return check_link_playwright(url, page)
            return False
            
    return True

def send_email_notification(smtp_host, smtp_port, smtp_user, smtp_pass, from_email, to_email, user_name, links):
    """Send an email notification about broken links via SMTP."""
    msg = MIMEMultipart()
    msg['From'] = f"AIX Link Checker <{from_email}>"
    msg['To'] = to_email
    msg['Subject'] = "Broken Links Detected on AIX Website"
    
    body = f"Hello {user_name},\n\nThe automated broken link checker has found some dead links on pages you are responsible for:\n\n"
    body += "\n".join(links)
    body += "\n\nPlease update these links in the source Markdown files. Thanks!\n\nAIX Link Checker Bot"
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls() # Secure the connection
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
        print(f"Sent email successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Check for broken links in the _site directory.")
    parser.add_argument("--smtp-host", default="sysmail.leuphana.de")
    parser.add_argument("--smtp-port", type=int, default=587)
    parser.add_argument("--smtp-user", default="creativespace")
    parser.add_argument("--smtp-pass", help="SMTP Password", default=os.environ.get('SMTP_PASSWORD', ''))
    parser.add_argument("--from-email", default="creativespace-noreply@leuphana.de")
    parser.add_argument("--admin-email", help="Fallback admin email", default="admin@leuphana.de")
    parser.add_argument("--dry-run", action="store_true", help="Print emails instead of sending them")
    parser.add_argument("--test-only", help="Only send emails to this specific address (for testing)", default=None)
    args = parser.parse_args()

    if not os.path.exists('_site'):
        print("Error: _site/ directory not found. Please run 'jekyll build' first.")
        return

    print("Building author map...")
    author_map = build_author_map()
    print(f"Found {len(author_map)} team members with email addresses.")

    html_files = []
    for root, _, files in os.walk('_site'):
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))
                
    print(f"Scanning {len(html_files)} HTML files...")
    
    broken_links = []
    checked_urls = {}
    
    # Initialize Playwright exactly once for all files
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        stealth_plugin = Stealth()
        stealth_plugin.apply_stealth_sync(page) # Apply stealth to avoid bot detection
        
        for file_path in html_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                
                if href in checked_urls:
                    is_valid = checked_urls[href]
                else:
                    is_valid = check_link(href, page)
                    checked_urls[href] = is_valid
                    
                if not is_valid:
                    print(f"Broken link found in {file_path}: {href}")
                    responsible = find_responsible_person(file_path)
                    email = author_map.get(responsible) if responsible else None
                    broken_links.append((file_path, href, email, responsible or "Admin"))
        
        browser.close()
                
    if not broken_links:
        print("No broken links found!")
        return
        
    print(f"Found {len(broken_links)} broken links.")
    
    # Group by email to avoid spamming
    issues = {}
    for file_path, href, email, responsible in broken_links:
        # TEMPORARY: Hardcode recipient to Muratbek for testing purposes
        user_email = "Muratbek.Nurmatov@stud.leuphana.de"
        # user_email = email if email else args.admin_email
        if user_email not in issues:
            issues[user_email] = {"name": responsible, "links": []}
            
        page_url = "/" + os.path.relpath(file_path, '_site').replace('index.html', '')
        issues[user_email]["links"].append(f"- Broken Link: {href} (on page: {page_url})")
        
    for user_email, data in issues.items():
        if args.test_only and user_email != args.test_only:
            continue
            
        if args.dry_run:
            print(f"\n--- DRY RUN EMAIL TO {user_email} ---")
            print(f"Subject: Broken Links Detected on AIX Website")
            print(f"Hello {data['name']},\n\nThe automated broken link checker has found some dead links:\n")
            print("\n".join(data["links"]))
            print("-------------------------------------\n")
        else:
            if args.smtp_pass:
                send_email_notification(
                    args.smtp_host, args.smtp_port, args.smtp_user, args.smtp_pass,
                    args.from_email, user_email, data["name"], data["links"]
                )
                time.sleep(1) # Prevent rate limiting
            else:
                print(f"Skipping email to {user_email}: --smtp-pass not provided.")

if __name__ == "__main__":
    main()
