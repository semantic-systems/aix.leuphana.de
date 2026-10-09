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
import fnmatch
import re
import argparse
import time
import random
import smtplib
import json
from email.utils import parseaddr
from urllib.parse import urlsplit, unquote
from html import unescape
from concurrent.futures import ThreadPoolExecutor, as_completed
from email.mime.text import MIMEText
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
NOTIFICATION_STATE_FILE = 'link_notification_state.json'
OWNER_FILE = 'scripts/link_owners.yml'
SITE_URL = 'https://aix.leuphana.de'
REMINDER_SECONDS = 7 * 86400
DNS_FAILURE = 'DNS_NAME_NOT_RESOLVED'

def is_dns_resolution_error(error):
    message = str(error).lower()
    return any(marker in message for marker in (
        'err_name_not_resolved', 'nameresolutionerror', 'gaierror',
        'name or service not known', 'nodename nor servname provided',
        'failed to resolve', 'dns_probe_finished_nxdomain',
    ))

def is_ignored_link(url):
    host = urlsplit(url).hostname
    if not host:
        return False
    host = host.lower()
    return any(host == domain or host.endswith('.' + domain)
               for domain in ('doi.org', 'linkedin.com'))

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
            return yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            pass
    return {}

def valid_email(value):
    if not isinstance(value, str):
        return False
    name, address = parseaddr(value.strip())
    return (not name and address == value.strip()
            and re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', address) is not None
            and not address.lower().endswith(('@example.org', '@example.com')))

def build_team_map():
    """Team profile filename is the stable owner ID; display names may change."""
    team = {}
    for path in sorted(glob.glob('_team/*.md') + glob.glob('_team/*.markdown')):
        fm = parse_frontmatter(path)
        slug = os.path.splitext(os.path.basename(path))[0]
        email = fm.get('email')
        team[slug] = {'name': fm.get('name', slug), 'email': email.strip().lower() if valid_email(email) else None}
    return team

def load_owner_assignments():
    if not os.path.exists(OWNER_FILE):
        return {}
    with open(OWNER_FILE, encoding='utf-8') as stream:
        data = yaml.safe_load(stream) or {}
    pages = data.get('pages', {})
    if not isinstance(pages, dict):
        raise ValueError(f'{OWNER_FILE}: pages must be a mapping of source paths to owner IDs')
    return pages

def page_path(html_path, site_dir='_site'):
    relative = os.path.relpath(html_path, site_dir).replace(os.sep, '/')
    if relative == 'index.html':
        return '/'
    if relative.endswith('/index.html'):
        return '/' + relative[:-len('index.html')]
    return '/' + relative

def normalize_permalink(value):
    if not value:
        return None
    path = '/' + str(value).lstrip('/')
    if path.endswith('/'):
        return path
    if path.endswith('.html'):
        return path
    return path + '/'

def build_source_index():
    """Map generated page paths to source files, including fixed permalinks."""
    index = {}
    directories = {'_team': 'team', '_projects': 'projects', '_publications': 'publications', '_demos': 'demos'}
    for directory, route in directories.items():
        for path in sorted(glob.glob(f'{directory}/*.md') + glob.glob(f'{directory}/*.markdown')):
            fm = parse_frontmatter(path)
            if fm.get('published') is False:
                continue
            slug = os.path.splitext(os.path.basename(path))[0]
            index[f'/{route}/{slug}/'] = path
            permalink = fm.get('permalink')
            if permalink:
                resolved = str(permalink).replace(':path', slug).replace(':title', slug)
                index[normalize_permalink(resolved)] = path
    for path in sorted(glob.glob('_posts/*.md') + glob.glob('_posts/*.markdown')):
        fm = parse_frontmatter(path)
        if fm.get('published') is False:
            continue
        stem = os.path.splitext(os.path.basename(path))[0]
        match = re.match(r'^(\d{4})-(\d{2})-(\d{2})-(.+)$', stem)
        if not match:
            continue
        year, month, day, slug = match.groups()
        index[f'/{year}/{month}/{day}/{slug}.html'] = path
        index[f'/news/{slug}/'] = path
        if fm.get('permalink'):
            index[normalize_permalink(fm['permalink'])] = path
    return index

def find_source_file_for_html(html_path, source_index, site_dir='_site'):
    return source_index.get(page_path(html_path, site_dir))

def page_is_stale(html_path, source_file, html_signature=None):
    """Avoid comparing generated HTML with a newer or concurrently rebuilt source."""
    if not source_file:
        return False
    try:
        html_stat = os.stat(html_path)
        source_stat = os.stat(source_file)
    except OSError:
        return True
    if source_stat.st_mtime_ns > html_stat.st_mtime_ns:
        return True
    return html_signature is not None and html_signature != (html_stat.st_mtime_ns, html_stat.st_size)

def owners_for_source(source_file, team_map, assignments):
    if not source_file:
        return [], 'no source file found'
    fm = parse_frontmatter(source_file)
    owner_ids = assignments.get(source_file)
    if owner_ids is None:
        for pattern, ids in assignments.items():
            if '*' in pattern and fnmatch.fnmatchcase(source_file, pattern):
                owner_ids = ids
                break
    if owner_ids is None:
        owner_ids = fm.get('link_check_owners', fm.get('link_check_owner'))
    if owner_ids is None and source_file.startswith('_team/'):
        owner_ids = os.path.splitext(os.path.basename(source_file))[0]
    if isinstance(owner_ids, str):
        owner_ids = [owner_ids]
    if not isinstance(owner_ids, list) or not owner_ids:
        return [], 'no owner assigned'
    recipients = []
    missing = []
    for owner_id in owner_ids:
        person = team_map.get(owner_id)
        if not person or not person['email']:
            missing.append(str(owner_id))
        elif person['email'] not in [entry['email'] for entry in recipients]:
            recipients.append(person)
    return recipients, ('missing owner email: ' + ', '.join(missing)) if missing else None

def link_in_source(source_file, href):
    """Links supplied only by shared layouts belong to the site admins."""
    if not source_file:
        return False
    with open(source_file, encoding='utf-8') as stream:
        source = unescape(stream.read())
    decoded = unescape(href)
    path = unquote(urlsplit(decoded).path)
    return decoded in source or (path and len(path) > 1 and path in source)

def load_notification_state():
    try:
        with open(NOTIFICATION_STATE_FILE, encoding='utf-8') as stream:
            state = json.load(stream)
            return state if isinstance(state, dict) else {}
    except (OSError, ValueError):
        return {}

def state_for_stale_pages(state, stale_page_urls):
    """A skipped page has not been checked, so retain its reminder history."""
    retained = {}
    for key, value in state.items():
        try:
            parts = json.loads(key)
        except (TypeError, ValueError):
            continue
        if isinstance(parts, list) and len(parts) == 3 and parts[1] in stale_page_urls:
            retained[key] = value
    return retained

def save_notification_state(state):
    temporary = NOTIFICATION_STATE_FILE + '.tmp'
    with open(temporary, 'w', encoding='utf-8') as stream:
        json.dump(state, stream, indent=2, sort_keys=True)
    os.replace(temporary, NOTIFICATION_STATE_FILE)

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
        if is_dns_resolution_error(e):
            return False, DNS_FAILURE
        return False, f"Exception: {type(e).__name__}"

def check_link_http(url, session, site_dir='_site'):
    """Check if a URL is broken using standard HTTP requests."""
    if url.startswith('mailto:') or url.startswith('tel:'):
        return True, False, 200
        
    if url.startswith('/'):
        url = url.split('#')[0]
        local_path = os.path.join(site_dir, url.lstrip('/'))
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
            if is_dns_resolution_error(e):
                return False, True, DNS_FAILURE
            return False, True, type(e).__name__
            
    return True, False, 200

def classify_error(status):
    if status == DNS_FAILURE:
        return "DNS name could not be resolved (check URL/domain)"
    elif status in [401, 403, 405, 429, 503, 999]:
        return f"Blocked by Website ({status})"
    elif status in [404, 410]:
        return f"Actually Broken ({status})"
    elif isinstance(status, str):
        if "Timeout" in status or "TimeoutError" in status:
            return "Timeout (Likely Blocked or Server Down)"
        elif any(err in status for err in ["ConnectionError", "NameResolutionError", "Exception", "Error"]):
            return "Connection failure (needs review)"
        else:
            return f"Broken / Error ({status})"
    else:
        return f"Broken / Error ({status})"

def send_email_notification(args, to_email, subject, body):
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = f"AIX Link Checker <{args.from_email}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    try:
        with smtplib.SMTP(args.smtp_host, args.smtp_port, timeout=20) as server:
            server.starttls()
            server.login(args.smtp_user, args.smtp_pass)
            server.send_message(msg)
        print(f"Sent email successfully to {to_email}")
        return True
    except Exception as exc:
        print(f"Failed to send email to {to_email}: {exc}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Check links in a built Jekyll site.")
    parser.add_argument("--smtp-host", default="sysmail.leuphana.de")
    parser.add_argument("--smtp-port", type=int, default=587)
    parser.add_argument("--smtp-user", default="creativespace")
    parser.add_argument("--smtp-pass", help="SMTP Password", default=os.environ.get('SMTP_PASSWORD', ''))
    parser.add_argument("--from-email", default="creativespace-noreply@leuphana.de")
    parser.add_argument("--admin-emails", "--admin-email", dest="admin_emails",
                        default=os.environ.get('LINK_CHECK_ADMIN_EMAILS', 'Muratbek.Nurmatov@stud.leuphana.de'),
                        help="Comma-separated admin recipients (also accepts LINK_CHECK_ADMIN_EMAILS)")
    parser.add_argument("--dry-run", action="store_true", help="Print emails instead of sending them")
    parser.add_argument("--site-dir", default='_site', help="Directory containing a freshly built site (default: _site)")
    parser.add_argument("--test-only", help="Only send emails addressed to this recipient", default=None)
    parser.add_argument("--ownership-report", action="store_true", help="Print page ownership without checking links or sending mail")
    args = parser.parse_args()

    admin_emails = list(dict.fromkeys(email.strip().lower() for email in args.admin_emails.split(',') if valid_email(email.strip())))
    if args.test_only:
        args.test_only = args.test_only.strip().lower()
    if not admin_emails:
        parser.error('Provide at least one valid admin address with --admin-emails or LINK_CHECK_ADMIN_EMAILS')

    team_map = build_team_map()
    assignments = load_owner_assignments()
    source_index = build_source_index()
    print(f"Found {sum(bool(person['email']) for person in team_map.values())} team profiles with usable email addresses.")
    if args.ownership_report:
        missing = 0
        for source_file in sorted(set(source_index.values())):
            recipients, reason = owners_for_source(source_file, team_map, assignments)
            if reason:
                missing += 1
            addresses = ', '.join(person['email'] for person in recipients) or 'admins only'
            print(f'{source_file}: {addresses}' + (f' [{reason}]' if reason else ''))
        print(f'Ownership review: {missing} page(s) need an owner or a usable email.')
        return

    site_dir = args.site_dir
    if not os.path.isdir(site_dir):
        print(f"Error: {site_dir}/ directory not found. Please run 'jekyll build' first.")
        return

    html_files = []
    for root, _, files in os.walk(site_dir):
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))
    html_files.sort()
    print(f"Scanning {len(html_files)} HTML files...")

    cache = load_cache()
    links_to_check = []
    html_signatures = {}
    stale_pages = {}
    for file_path in html_files:
        source_file = find_source_file_for_html(file_path, source_index, site_dir)
        if page_is_stale(file_path, source_file):
            stale_pages[SITE_URL + page_path(file_path, site_dir)] = source_file
            continue
        html_stat = os.stat(file_path)
        html_signatures[file_path] = (html_stat.st_mtime_ns, html_stat.st_size)
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            url_stripped = href.split('#')[0]
            if url_stripped and not is_ignored_link(url_stripped):
                links_to_check.append((file_path, href, url_stripped))

    unique_urls = sorted(set(url for _, _, url in links_to_check))
    results = {}
    needs_playwright = []
    dns_failures_from_http = set()
    print(f"Total unique URLs to check: {len(unique_urls)}")

    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {}
            for url in unique_urls:
                if url in cache and cache[url].get('is_valid'):
                    results[url] = {'is_valid': True, 'status': 200}
                else:
                    future_to_url[executor.submit(check_link_http, url, session, site_dir)] = url
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    is_valid, needs_pw, status = future.result()
                    if needs_pw:
                        needs_playwright.append(url)
                        if status == DNS_FAILURE:
                            dns_failures_from_http.add(url)
                    else:
                        results[url] = {'is_valid': is_valid, 'status': status}
                        if is_valid:
                            cache[url] = {'is_valid': True, 'timestamp': time.time()}
                except Exception as exc:
                    print(f"{url} generated an exception: {exc}")
                    needs_playwright.append(url)

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
                if not is_valid and url in dns_failures_from_http and (
                    status == 'No Response' or str(status).startswith('Exception:')
                ):
                    status = DNS_FAILURE
                results[url] = {'is_valid': is_valid, 'status': status}
                if is_valid:
                    cache[url] = {'is_valid': True, 'timestamp': time.time()}
            browser.close()

    if not args.dry_run:
        save_cache(cache)

    owner_reports = {}
    admin_records = []
    seen_issues = set()
    current_keys = set()
    now = time.time()
    previous_state = load_notification_state()
    next_state = {}
    unconfirmed_count = 0
    for file_path, href, url in links_to_check:
        page_url = SITE_URL + page_path(file_path, site_dir)
        source_file = find_source_file_for_html(file_path, source_index, site_dir)
        if page_is_stale(file_path, source_file, html_signatures[file_path]):
            stale_pages[page_url] = source_file
            continue
        result = results.get(url, {'is_valid': False, 'status': 'Unknown'})
        if result['is_valid']:
            continue
        issue_id = (page_url, href)
        if issue_id in seen_issues:
            continue
        seen_issues.add(issue_id)
        status = result['status']
        classification = classify_error(status)
        owner_actionable = status in (404, 410, DNS_FAILURE)
        if not owner_actionable:
            unconfirmed_count += 1
            continue
        recipients = []
        reason = None
        if not link_in_source(source_file, href):
            reason = 'link comes from shared layout or source could not be identified'
        else:
            recipients, reason = owners_for_source(source_file, team_map, assignments)

        issue = {'page': page_url, 'href': href, 'classification': classification,
                 'source': source_file or '(shared/site page)', 'reason': reason,
                 'recipients': [person['email'] for person in recipients]}
        admin_records.append(issue)
        for person in recipients:
            address = person['email']
            key = json.dumps([address, page_url, href], ensure_ascii=False)
            current_keys.add(key)
            prior = previous_state.get(key, {})
            if not isinstance(prior, dict):
                prior = {}
            elif prior:
                next_state[key] = prior
            if now - prior.get('last_sent', 0) < REMINDER_SECONDS:
                continue
            report = owner_reports.setdefault(address, {'name': person['name'], 'issues': []})
            report['issues'].append((key, issue))

    # A page may have changed after its first link was processed. Discard all
    # findings for it before any email is sent, including earlier findings.
    for file_path, signature in html_signatures.items():
        source_file = find_source_file_for_html(file_path, source_index, site_dir)
        if page_is_stale(file_path, source_file, signature):
            stale_pages[SITE_URL + page_path(file_path, site_dir)] = source_file
    if stale_pages:
        admin_records = [issue for issue in admin_records if issue['page'] not in stale_pages]
        owner_reports = {
            address: {'name': report['name'],
                      'issues': [(key, issue) for key, issue in report['issues']
                                 if issue['page'] not in stale_pages]}
            for address, report in owner_reports.items()
        }
        owner_reports = {address: report for address, report in owner_reports.items() if report['issues']}
        current_keys = {key for key in current_keys if json.loads(key)[1] not in stale_pages}

    if stale_pages:
        print(f"Skipped {len(stale_pages)} page(s) whose Markdown source is newer than the generated HTML or whose HTML changed during the scan. Rebuild {site_dir}/ and scan again.")

    http_failures = sum(record['classification'].startswith('Actually Broken') for record in admin_records)
    dns_failures = sum(record['classification'].startswith('DNS name') for record in admin_records)
    print(f"Found {len(admin_records)} broken page/link pairs: {http_failures} HTTP 404/410 and {dns_failures} DNS lookup failures. {unconfirmed_count} other errors omitted from email.")
    delivery_failures = []
    for address, report in sorted(owner_reports.items()):
        if address in admin_emails:
            # The admin summary already contains these issues.
            continue
        if args.test_only and address != args.test_only:
            continue
        lines = [f"Hello {report['name']},", '',
                 'Links needing attention were found on pages assigned to you:',
                 'A DNS lookup failure may be temporary; check the URL before changing it.', '']
        for _, issue in report['issues']:
            lines.extend([f"Page: {issue['page']}", f"Source: {issue['source']}",
                          f"Link: {issue['href']}", f"Reason: {issue['classification']}", ''])
        lines.append('Please update the source file, then the next scan will clear the issue.')
        body = '\n'.join(lines)
        subject = 'Action required: broken links on your AIX pages'
        if args.dry_run:
            print(f"\n--- DRY RUN TO {address} ---\nSubject: {subject}\n{body}")
            continue
        if not args.smtp_pass:
            delivery_failures.append(f'{address}: SMTP password missing')
            continue
        if send_email_notification(args, address, subject, body):
            for key, _ in report['issues']:
                next_state[key] = {'last_sent': now}
        else:
            delivery_failures.append(address)

    if admin_records:
        summary = [f'{len(admin_records)} broken link(s) found.', '']
        admin_subject = 'AIX link checker: broken links found'
    elif stale_pages:
        summary = ['No broken links found on the pages checked.']
        admin_subject = 'AIX link checker: scan incomplete'
    else:
        summary = ['No broken links found right now.']
        admin_subject = 'AIX link checker: no broken links'
    if stale_pages:
        summary.extend([f'Scan incomplete: {len(stale_pages)} page(s) have outdated generated HTML.',
                        f'Rebuild {site_dir}/ and run the checker again.', ''])
    shared_links = {}
    for issue in admin_records:
        if issue['reason'] == 'link comes from shared layout or source could not be identified':
            entry = shared_links.setdefault(issue['href'], {'count': 0, 'classification': issue['classification']})
            entry['count'] += 1
            continue
        routing = ', '.join(issue['recipients']) if issue['recipients'] else 'admins only'
        summary.extend([f"Page: {issue['page']}", f"Source: {issue['source']}",
                        f"Link: {issue['href']}", f"Status: {issue['classification']}",
                        f"Routing: {routing}"])
        if issue['reason']:
            summary.append(f"Review: {issue['reason']}")
        summary.append('')
    if shared_links:
        summary.append('Shared layout/site links (one entry per URL):')
        for href, entry in sorted(shared_links.items()):
            summary.append(f"{href} — {entry['classification']} on {entry['count']} page(s)")
        summary.append('')
    if delivery_failures:
        summary.extend(['Owner email delivery failures:', *delivery_failures, ''])
    summary_body = '\n'.join(summary)
    for address in admin_emails:
        if args.test_only and address != args.test_only:
            continue
        if args.dry_run:
            print(f"\n--- DRY RUN ADMIN SUMMARY TO {address} ---\nSubject: {admin_subject}\n{summary_body}")
        elif args.smtp_pass:
            send_email_notification(args, address, admin_subject, summary_body)
        else:
            print(f'Skipping admin summary to {address}: SMTP password missing')

    if not args.dry_run and not args.test_only:
        active_state = {key: value for key, value in next_state.items() if key in current_keys}
        active_state.update(state_for_stale_pages(previous_state, set(stale_pages)))
        save_notification_state(active_state)

if __name__ == "__main__":
    main()
