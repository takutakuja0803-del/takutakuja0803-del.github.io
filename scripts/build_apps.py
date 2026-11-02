#!/usr/bin/env python3
"""Render shared app information into static HTML for GitHub Pages."""

import argparse
import json
import os
import re
import sys
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote


ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "data/apps.json"
APP_FIELDS = {
    "id", "name", "shortDescription", "metaDescription", "icon", "ownership",
    "operator", "supportOwner", "supportContact", "privacyOwner", "status",
    "appStoreUrl", "detailUrl", "supportUrl", "privacyUrl", "showOnHome",
    "showOnProjects", "featuredOnHome", "order", "category",
}
STATUSES = {"Released", "Pre-release", "In Development", "Unconfirmed"}


def fail(message):
    raise ValueError(message)


def local_file(value, field):
    if not isinstance(value, str) or not value or value.startswith(("/", "~")):
        fail(f"{field}: expected a relative file path")
    parts = Path(value).parts
    if ".." in parts or urlsplit(value).scheme or urlsplit(value).query or urlsplit(value).fragment:
        fail(f"{field}: unsafe path {value!r}")
    target = ROOT / value
    if not target.is_file():
        fail(f"{field}: missing file {value}")
    return target


def page_url(value, field):
    if isinstance(value, str) and urlsplit(value).scheme == 'https':
        if not urlsplit(value).netloc:
            fail(f'{field}: invalid HTTPS URL')
        return None
    return local_file(value, field)


def validate_registry(data):
    if not isinstance(data, dict) or not isinstance(data.get("apps"), list):
        fail("Registry must contain an apps array")
    site_url = data.get("siteUrl")
    if not isinstance(site_url, str) or urlsplit(site_url).scheme != "https" or not urlsplit(site_url).netloc or not site_url.endswith("/"):
        fail("siteUrl must be an HTTPS URL ending in /")
    ids, orders, details = set(), set(), set()
    for app in data["apps"]:
        if not isinstance(app, dict) or APP_FIELDS - app.keys():
            fail(f"App missing required fields: {sorted(APP_FIELDS - app.keys()) if isinstance(app, dict) else app}")
        app_id = app["id"]
        if not isinstance(app_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", app_id):
            fail(f"Invalid app id: {app_id!r}")
        if app_id in ids:
            fail(f"Duplicate app id: {app_id}")
        ids.add(app_id)
        order = app["order"]
        if type(order) is not int or order < 1 or order in orders:
            fail(f"{app_id}: order must be a unique positive integer")
        orders.add(order)
        for field in ("name", "shortDescription", "metaDescription", "operator", "supportOwner", "supportContact", "privacyOwner", "category"):
            if not isinstance(app[field], str) or not app[field].strip():
                fail(f"{app_id}: {field} is required")
        for field in ("projectDescription", "featuredDescription", "ogDescription", "statusSuffix", "featuredCategory", "appStoreName", "availabilityDetails"):
            if app.get(field) is not None and (not isinstance(app[field], str) or not app[field].strip()):
                fail(f"{app_id}: {field} must be text or null")
        for field in ("showOnHome", "showOnProjects", "featuredOnHome"):
            if type(app[field]) is not bool:
                fail(f"{app_id}: {field} must be boolean")
        if app["featuredOnHome"] and (not app["showOnHome"] or not app.get("featuredDescription") or not app.get("featuredCategory")):
            fail(f"{app_id}: featured app needs Home visibility, description, and category")
        if app["showOnProjects"] and not app.get("projectDescription"):
            fail(f"{app_id}: projectDescription is required")
        if app["ownership"] not in ("first-party", "client"):
            fail(f"{app_id}: ownership must be first-party or client")
        if app["status"] not in STATUSES:
            fail(f"{app_id}: invalid status {app['status']!r}")
        store_url = app["appStoreUrl"]
        if app["status"] == "Released":
            if not isinstance(store_url, str) or urlsplit(store_url).scheme != "https" or urlsplit(store_url).netloc != "apps.apple.com":
                fail(f"{app_id}: Released requires a verified App Store URL")
        elif store_url is not None:
            fail(f"{app_id}: unreleased app must not have an App Store URL")
        contact = urlsplit(app["supportContact"])
        if contact.scheme not in ("mailto", "https") or (contact.scheme == "mailto" and not contact.path) or (contact.scheme == "https" and not contact.netloc):
            fail(f"{app_id}: supportContact must be mailto: or HTTPS")
        for field in ("icon", "detailUrl"):
            local_file(app[field], f"{app_id}.{field}")
        for field in ("supportUrl", "privacyUrl"):
            page_url(app[field], f"{app_id}.{field}")
        support_page = page_url(app["supportUrl"], f"{app_id}.supportUrl")
        if support_page and app["supportContact"] not in support_page.read_text(encoding='utf-8'):
            fail(f"{app_id}: supportContact is missing from the Support page")
        privacy_page = page_url(app["privacyUrl"], f"{app_id}.privacyUrl")
        if privacy_page and app["privacyOwner"] not in privacy_page.read_text(encoding='utf-8'):
            fail(f"{app_id}: privacyOwner is missing from the Privacy page")
        if support_page:
            privacy_link = relative_url(app["supportUrl"], app["privacyUrl"])
            if f'href="{privacy_link}"' not in support_page.read_text(encoding='utf-8'):
                fail(f"{app_id}: Support page must link to its Privacy page")
        if privacy_page:
            support_link = relative_url(app["privacyUrl"], app["supportUrl"])
            if f'href="{support_link}"' not in privacy_page.read_text(encoding='utf-8'):
                fail(f"{app_id}: Privacy page must link to its Support page")
        if app["detailUrl"] in details:
            fail(f"Duplicate detailUrl: {app['detailUrl']}")
        details.add(app["detailUrl"])
    return sorted(data["apps"], key=lambda app: app["order"])


def h(value):
    return escape(value, quote=True)


def relative_url(source, target):
    parts = urlsplit(target)
    if parts.scheme or parts.netloc:
        return target
    return os.path.relpath(ROOT / target, (ROOT / source).parent).replace(os.sep, "/")


def marker_replace(content, key, fragment, path):
    start = f"<!-- APP_REGISTRY:{key}:START -->"
    end = f"<!-- APP_REGISTRY:{key}:END -->"
    pattern = re.compile(
        r"(?m)^(?P<indent>[ \t]*)" + re.escape(start)
        + r"\n.*?^(?P=indent)" + re.escape(end), re.DOTALL
    )
    matches = list(pattern.finditer(content))
    if len(matches) != 1:
        fail(f"{path}: expected exactly one {key} marker pair, found {len(matches)}")
    indent = matches[0].group("indent")
    lines = "\n".join(indent + line if line else "" for line in fragment.splitlines())
    replacement = f"{indent}{start}\n{lines}\n{indent}{end}"
    return pattern.sub(lambda _: replacement, content, count=1)


def home_card(app):
    description = app["shortDescription"]
    if app["status"] == "Released" and app.get("appStoreName"):
        description = f'Released on the App Store as {app["appStoreName"]}. ' + description
    lines = [
        '<article class="app-card">',
        f'  <img class="app-icon" src="{h(app["icon"])}" alt="{h(app["name"])} app icon" width="72" height="72">',
        '  <div class="app-details">',
        f'    <h3>{h(app["name"])}</h3>',
        f'    <p>{h(description)}</p>',
    ]
    if app["ownership"] == "client":
        lines.append(f'    <p>Operated by {h(app["operator"])}.</p>')
    lines.extend((
        '  </div>',
        f'  <a class="text-link" href="{h(app["detailUrl"])}">Learn more <span aria-hidden="true">→</span></a>',
        '</article>',
    ))
    return "\n".join(lines)


def project_card(app):
    status = app["status"] + (f' · {app["statusSuffix"]}' if app.get("statusSuffix") else "")
    description = app["projectDescription"]
    if app["status"] == "Released" and app.get("appStoreName"):
        description += f' Released on the App Store as {app["appStoreName"]}.'
    lines = [
        f'<section class="content-card" id="{h(app["id"])}">',
        f'  <h3>{h(app["name"])}</h3>',
        f'  <p><strong>Category:</strong> {h(app["category"])}<br><strong>Status:</strong> {h(status)}</p>',
        f'  <p>{h(description)}</p>',
    ]
    if app["ownership"] == "client":
        lines.append(f'  <p><strong>Operator:</strong> {h(app["operator"])}</p>')
    lines.extend((
        f'  <img class="app-icon" src="{h(app["icon"])}" alt="{h(app["name"])} app icon" width="72" height="72">',
        f'  <p><a class="text-link" href="{h(app["detailUrl"])}">App overview →</a></p>',
    ))
    if app["appStoreUrl"]:
        lines.append(f'  <p><a class="button" href="{h(app["appStoreUrl"])}" target="_blank" rel="noopener noreferrer">View on the App Store</a></p>')
    lines.append('</section>')
    return "\n".join(lines)


def featured_card(app):
    status = app["status"] + (f' · {app["featuredCategory"]}' if app.get("featuredCategory") else "")
    return "\n".join((
        '<section class="content-card">',
        f'  <h3>{h(app["name"])}</h3>',
        f'  <p><strong>{h(status)}</strong></p>',
        f'  <p>{h(app["featuredDescription"])}</p>',
        f'  <p><a class="text-link" href="{h(app["detailUrl"])}">Explore {h(app["name"])} →</a></p>',
        '</section>',
    ))


def detail_meta(app, site_url):
    description = app["metaDescription"]
    if app["status"] == "Released" and app.get("appStoreName"):
        description += f' Listed on the App Store as {app["appStoreName"]}.'
    lines = [f'<meta name="description" content="{h(description)}">']
    if app.get("ogDescription"):
        lines.extend((
            f'<meta property="og:title" content="{h(app["name"])} — TAKUMI Lab">',
            f'<meta property="og:description" content="{h(app["ogDescription"])}">',
            f'<meta property="og:image" content="{h(urljoin(site_url, app["icon"]))}">',
            f'<meta property="og:url" content="{h(urljoin(site_url, app["detailUrl"].removesuffix("index.html")))}">',
            '<meta property="og:type" content="website">',
        ))
    lines.append(f'<title>{h(app["name"])} — TAKUMI Lab</title>')
    return "\n".join(lines)


def detail_hero(app):
    return "\n".join((
        '<div class="app-hero">',
        f'  <img class="app-icon app-icon-large" src="../{h(app["icon"])}" alt="{h(app["name"])} app icon" width="96" height="96">',
        '  <div>',
        '    <p class="eyebrow">App</p>',
        f'    <h1 class="page-title">{h(app["name"])}</h1>',
        '  </div>',
        '</div>',
    ))


def detail_cta(app):
    if not app["appStoreUrl"]:
        return ""
    return f'<p><a class="button" href="{h(app["appStoreUrl"])}" rel="noopener noreferrer" target="_blank">View on the App Store</a></p>'


def detail_availability(app):
    if app["status"] == "Released":
        summary = "Released on the App Store"
        if app.get("appStoreName"):
            summary += f' as {app["appStoreName"]}'
        summary += "."
        if app.get("availabilityDetails"):
            summary += " " + app["availabilityDetails"]
    elif app["status"] == "Pre-release":
        summary = "Not yet available on the App Store."
    elif app["status"] == "In Development":
        summary = "In development. App Store availability has not been announced."
    else:
        summary = "Release status has not yet been confirmed."
    lines = ['<section class="content-card">', '  <h2>Availability</h2>', f'  <p>{h(summary)}</p>']
    if app["appStoreUrl"]:
        lines.append(f'  <p><a class="text-link" href="{h(app["appStoreUrl"])}" target="_blank" rel="noopener noreferrer">View on the App Store <span aria-hidden="true">→</span></a></p>')
    lines.append('</section>')
    return "\n".join(lines)


def detail_link(app, source, field, label):
    href = relative_url(source, app[field])
    return f'<p><a class="text-link" href="{h(href)}">{label} <span aria-hidden="true">→</span></a></p>'


def app_footer(app, source):
    return "\n".join((
        '<nav aria-label="App navigation">',
        f'  <a href="{h(relative_url(source, app["supportUrl"]))}">Support</a>',
        f'  <a href="{h(relative_url(source, app["privacyUrl"]))}">Privacy</a>',
        '</nav>',
    ))


def render_pages(apps, site_url):
    home = ROOT / 'index.html'
    text = home.read_text(encoding='utf-8')
    text = marker_replace(text, 'home-apps', "\n\n".join(home_card(a) for a in apps if a['showOnHome']), home)
    text = marker_replace(text, 'home-featured', "\n\n".join(featured_card(a) for a in apps if a['featuredOnHome']), home)
    result = {home: text}

    projects = ROOT / 'projects.html'
    text = projects.read_text(encoding='utf-8')
    selected = [a for a in apps if a['showOnProjects']]
    text = marker_replace(text, 'projects-released', "\n\n".join(project_card(a) for a in selected if a['status'] == 'Released'), projects)
    text = marker_replace(text, 'projects-other', "\n\n".join(project_card(a) for a in selected if a['status'] != 'Released'), projects)
    result[projects] = text

    for app in apps:
        path = ROOT / app['detailUrl']
        text = path.read_text(encoding='utf-8')
        fragments = {
            'meta': detail_meta(app, site_url),
            'hero': detail_hero(app),
            'cta': detail_cta(app),
            'availability': detail_availability(app),
            'support-link': detail_link(app, app['detailUrl'], 'supportUrl', 'Open Support'),
            'privacy-link': detail_link(app, app['detailUrl'], 'privacyUrl', 'Read the Privacy Policy'),
            'app-footer': app_footer(app, app['detailUrl']),
        }
        for key, fragment in fragments.items():
            text = marker_replace(text, key, fragment, path)
        result[path] = text
    return result


class LinkScanner(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = []
        self.titles = 0
        self.meta = set()
        self.missing_alt = False

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if tag == 'title':
            self.titles += 1
        if tag == 'meta' and attrs.get('name') in ('description', 'viewport'):
            self.meta.add(attrs['name'])
        if tag == 'img' and 'alt' not in attrs:
            self.missing_alt = True
        if attrs.get('id'):
            self.ids.append(attrs['id'])
        for field in ('href', 'src'):
            if field in attrs:
                self.refs.append(attrs[field])


def validate_html(pages):
    all_pages = {p: p.read_text(encoding='utf-8') for p in ROOT.rglob('*.html') if '.git' not in p.parts}
    all_pages.update(pages)
    scans = {}
    for path, content in all_pages.items():
        scan = LinkScanner()
        scan.feed(content)
        if len(scan.ids) != len(set(scan.ids)):
            fail(f'{path}: duplicate HTML id')
        if scan.titles != 1 or scan.meta != {'description', 'viewport'} or scan.missing_alt:
            fail(f'{path}: missing title, metadata, or image alt')
        scans[path] = scan
    for path, scan in scans.items():
        for ref in scan.refs:
            parts = urlsplit(ref)
            if parts.scheme in ('https', 'http'):
                if not parts.netloc:
                    fail(f'{path}: invalid external reference {ref!r}')
                continue
            if parts.scheme == 'mailto':
                if not parts.path:
                    fail(f'{path}: empty email link')
                continue
            if parts.scheme == 'data':
                continue
            if parts.scheme or parts.netloc or ref.startswith('/') or not ref:
                fail(f'{path}: invalid internal reference {ref!r}')
            target = (path.parent / unquote(parts.path)).resolve() if parts.path else path
            if not target.is_file():
                fail(f'{path}: broken internal reference {ref!r}')
            if parts.fragment and target in scans and unquote(parts.fragment) not in scans[target].ids:
                fail(f'{path}: missing fragment {ref!r}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate and fail if generated HTML is stale')
    args = parser.parse_args()
    data = json.loads(REGISTRY.read_text(encoding='utf-8'))
    apps = validate_registry(data)
    pages = render_pages(apps, data['siteUrl'])
    validate_html(pages)
    stale = [path for path, content in pages.items() if path.read_text(encoding='utf-8') != content]
    if args.check:
        if stale:
            print('Stale generated HTML:', *[str(p.relative_to(ROOT)) for p in stale], sep='\n  ', file=sys.stderr)
            return 1
        print(f'PASS: {len(apps)} apps, links, assets, and generated HTML')
        return 0
    for path in stale:
        path.write_text(pages[path], encoding='utf-8')
        print(f'Updated {path.relative_to(ROOT)}')
    print(f'Validated {len(apps)} apps and internal references')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, json.JSONDecodeError) as error:
        print(f'App Registry error: {error}', file=sys.stderr)
        sys.exit(1)
