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
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

from playwright.sync_api import sync_playwright
try:
    from playwright_stealth import Stealth
    stealth = lambda page: Stealth().apply_stealth_sync(page)
except ImportError:
    stealth = None

# Automatically load the .env file in the current directory if it exists
load_dotenv()

CACHE_FILE = 'link_cache.json'
CACHE_EXPIRY = 86400  # 1 day in seconds

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                # Filter out expired entries
                current_time = time.time()
                return {k: v for k, v in cache.items() if current_time - v.get('timestamp', 0) < CACHE_EXPIRY}
        except Exception:
            pass
    return {}

def save_cache(cache):
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f)
    except Exception as e:
        print(f"Failed to save cache: {e}")

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
            return (response.status < 400), response.status
        return False, "No Response"
    except Exception as e:
        return False, f"Exception: {type(e).__name__}"

def check_link_http(url, session):
    """Check if a URL is broken using standard HTTP requests."""
    if url.startswith('mailto:') or url.startswith('tel:'):
        return True, False, 200
        
    if url.startswith('https://www.linkedin.com/school/aix-leuphana'):
        return True, False, 200
        
    if url.startswith('/'):
        url = url.split('#')[0]
        local_path = os.path.join('_site', url.lstrip('/'))
        if os.path.isdir(local_path):
            local_path = os.path.join(local_path, 'index.html')
        elif not local_path.endswith('.html') and not '.' in os.path.basename(local_path):
            local_path += '.html'
            
        exists = os.path.exists(local_path)
        return exists, False, (200 if exists else 404)

    if url.startswith('http://') or url.startswith('https://'):
        url = url.split('#')[0]
        # Small delay between external requests to avoid triggering WAFs
        time.sleep(random.uniform(0.5, 1.5))
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            resp = session.head(url, headers=headers, allow_redirects=True, timeout=10)
            if resp.status_code >= 400 and resp.status_code != 405:
                resp = session.get(url, headers=headers, stream=True, timeout=10)
                if resp.status_code >= 400:
                    return False, True, resp.status_code # False for HTTP success, True for needs Playwright
                return resp.status_code < 400, False, resp.status_code
            return resp.status_code < 400, False, resp.status_code
        except requests.RequestException as e:
            return False, True, type(e).__name__
            
    return True, False, 200

def classify_error(status):
    if status in [401, 403, 405, 429, 503, 999]:
        return f"Blocked by Website ({status})"
    elif status in [404, 410]:
        return f"Actually Broken ({status})"
    elif isinstance(status, str) and ("Timeout" in status or "TimeoutError" in status):
        return "Timeout (Likely Blocked or Server Down)"
    else:
        return f"Broken / Error ({status})"

def send_email_notification(smtp_host, smtp_port, smtp_user, smtp_pass, from_email, to_email, user_name, links_by_page):
    """Send an email notification about broken links via SMTP."""
    msg = MIMEMultipart()
    msg['From'] = f"AIX Link Checker <{from_email}>"
    msg['To'] = to_email
    msg['Subject'] = "Action Required: Broken Links Detected on AIX Website"
    
    blocked_count = 0
    broken_count = 0
    other_count = 0
    for page_url, links in links_by_page.items():
        for link, classification in links:
            if "Blocked" in classification:
                blocked_count += 1
            elif "Actually Broken" in classification:
                broken_count += 1
            else:
                other_count += 1
                
    total_links = blocked_count + broken_count + other_count

    body = f"Hello {user_name},\n\n"
    body += "The automated broken link checker has found some dead links on pages you are responsible for.\n\n"
    body += "Broken Links Summary:\n"
    body += "-" * 50 + "\n"
    body += f"- Total flagged links: {total_links}\n"
    body += f"- Blocked by website (Anti-Bot): {blocked_count}\n"
    body += f"- Actually broken (404/410): {broken_count}\n"
    if other_count > 0:
        body += f"- Other errors (Timeout/Unknown): {other_count}\n"
    body += "-" * 50 + "\n"
    
    for page_url, links in links_by_page.items():
        body += f"\nPage: {page_url}\n"
        for link, classification in links:
            body += f"  ❌ {link}\n      Reason: {classification}\n"
            
    body += "\n" + "-" * 50 + "\n\n"
    body += "Please update these links in the source Markdown files. Thanks!\n\nAIX Link Checker Bot"
    
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
    
    cache = load_cache()
    
    # Collect all links to check
    links_to_check = []
    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            url_stripped = href.split('#')[0]
            if url_stripped:
                links_to_check.append((file_path, href, url_stripped))

    unique_urls = list(set(url for _, _, url in links_to_check))
    results = {}
    needs_playwright = []
    
    print(f"Total unique URLs to check: {len(unique_urls)}")
    
    # Use ThreadPoolExecutor and requests.Session
    with requests.Session() as session:
        # We limit max_workers to avoid completely overwhelming servers or being blocked immediately
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {}
            for url in unique_urls:
                if url in cache and cache[url].get('is_valid'):
                    results[url] = {'is_valid': True, 'status': 200}
                else:
                    future_to_url[executor.submit(check_link_http, url, session)] = url
            
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    is_valid, needs_pw, status = future.result()
                    if needs_pw:
                        needs_playwright.append(url)
                    else:
                        results[url] = {'is_valid': is_valid, 'status': status}
                        if is_valid:
                            cache[url] = {'is_valid': True, 'timestamp': time.time()}
                except Exception as exc:
                    print(f"{url} generated an exception: {exc}")
                    needs_playwright.append(url)

    # Playwright fallback sequentially
    if needs_playwright:
        print(f"Using Playwright fallback for {len(needs_playwright)} URLs...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            if stealth:
                stealth(page)
            
            for url in needs_playwright:
                is_valid, status = check_link_playwright(url, page)
                results[url] = {'is_valid': is_valid, 'status': status}
                if is_valid:
                    cache[url] = {'is_valid': True, 'timestamp': time.time()}
            
            browser.close()

    save_cache(cache)

    for file_path, original_href, url_stripped in links_to_check:
        res = results.get(url_stripped, {'is_valid': False, 'status': 'Unknown'})
        if not res['is_valid']:
            classification = classify_error(res['status'])
            print(f"Broken link found in {file_path}: {original_href} [{classification}]")
            responsible = find_responsible_person(file_path)
            email = author_map.get(responsible) if responsible else None
            broken_links.append((file_path, original_href, email, responsible or "Admin", classification))

    # Remove duplicates from broken_links just in case
    broken_links = list(set(broken_links))
                
    if not broken_links:
        print("No broken links found!")
        return
        
    blocked = sum(1 for x in broken_links if "Blocked" in x[4])
    broken = sum(1 for x in broken_links if "Actually Broken" in x[4])
    others = len(broken_links) - blocked - broken
    print(f"Found {len(broken_links)} flagged links: {blocked} Blocked, {broken} Actually Broken, {others} Other.")
    
    # Group by email to avoid spamming
    issues = {}
    for file_path, href, email, responsible, classification in broken_links:
        # TEMPORARY: Hardcode recipient to Muratbek for testing purposes
        user_email = "Muratbek.Nurmatov@stud.leuphana.de"
        # user_email = email if email else args.admin_email
        if user_email not in issues:
            issues[user_email] = {"name": responsible, "links_by_page": {}}
            
        page_url = "https://aix.leuphana.de/" + os.path.relpath(file_path, '_site').replace('index.html', '').lstrip('/')
        if page_url not in issues[user_email]["links_by_page"]:
            issues[user_email]["links_by_page"][page_url] = []
            
        issues[user_email]["links_by_page"][page_url].append((href, classification))
        
    for user_email, data in issues.items():
        if args.test_only and user_email != args.test_only:
            continue
            
        if args.dry_run:
            blocked_count = 0
            broken_count = 0
            other_count = 0
            for page_url, links in data["links_by_page"].items():
                for link, classification in links:
                    if "Blocked" in classification:
                        blocked_count += 1
                    elif "Actually Broken" in classification:
                        broken_count += 1
                    else:
                        other_count += 1
            
            print(f"\n--- DRY RUN EMAIL TO {user_email} ---")
            print(f"Subject: Action Required: Broken Links Detected on AIX Website")
            print(f"Hello {data['name']},\n\nThe automated broken link checker has found some dead links:\n")
            print(f"Summary: {blocked_count} Blocked, {broken_count} Actually Broken, {other_count} Other\n")
            for page_url, links in data["links_by_page"].items():
                print(f"\nPage: {page_url}")
                for link, classification in links:
                    print(f"  ❌ {link}\n      Reason: {classification}")
            print("\n-------------------------------------\n")
        else:
            if args.smtp_pass:
                send_email_notification(
                    args.smtp_host, args.smtp_port, args.smtp_user, args.smtp_pass,
                    args.from_email, user_email, data["name"], data["links_by_page"]
                )
                time.sleep(1) # Prevent rate limiting
            else:
                print(f"Skipping email to {user_email}: --smtp-pass not provided.")

if __name__ == "__main__":
    main()
