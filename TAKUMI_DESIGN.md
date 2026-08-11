# TAKUMI Lab Design Guide

Before creating or modifying any TAKUMI Lab web page, read this file first.
Existing implementation always has priority over assumptions.
New pages must visually match the existing TAKUMI Lab website unless the user explicitly requests a redesign.

If this file conflicts with the latest site implementation, follow the implementation first and update this file as part of the same change.

This guide is for AI/Codex agents editing the TAKUMI Lab GitHub Pages site. It documents the design system that already exists in the repository; do not treat it as permission to redesign the site.

## Current site structure

The site is a static GitHub Pages site with plain HTML and one shared CSS file.

- Top page: `index.html`
- Shared stylesheet: `styles.css`
- Ads file: `app-ads.txt`
- SwifKit overview: `swifkit/index.html`
- SwifKit support: `swifkit/support.html`
- SwifKit privacy policy: `swifkit/privacy.html`
- Smart GPA overview: `smart-gpa/index.html`
- Smart GPA support: `smart-gpa/support.html`
- Smart GPA privacy policy: `smart-gpa/privacy.html`
- SwifKit icon: `swifkit-icon.png`
- Smart GPA icon: `smart-gpa-icon.jpg`

There is currently no shared JavaScript. Do not add JavaScript unless the user explicitly asks for behavior that requires it.

Public GitHub Pages paths follow the same directory structure:

- `https://takutakuja0803-del.github.io/`
- `https://takutakuja0803-del.github.io/swifkit/`
- `https://takutakuja0803-del.github.io/swifkit/support.html`
- `https://takutakuja0803-del.github.io/swifkit/privacy.html`
- `https://takutakuja0803-del.github.io/smart-gpa/`
- `https://takutakuja0803-del.github.io/smart-gpa/support.html`
- `https://takutakuja0803-del.github.io/smart-gpa/privacy.html`

## 1. Design Philosophy

TAKUMI Lab uses a minimal, modern, Apple-inspired design. The site should feel calm, clean, spacious, and product-focused. It should look premium but not flashy.

The design should not compete with the apps. Keep pages simple, trustworthy, and easy to scan. Avoid startup-style hype, dense marketing copy, aggressive gradients, heavy animation, and overly decorative layouts.

## 2. Color System

Use the existing CSS custom properties in `styles.css`.

```css
:root {
  color-scheme: light;
  --background: #f5f7fb;
  --surface: rgba(255, 255, 255, 0.82);
  --text: #17181a;
  --secondary: #62666d;
  --accent: #0066cc;
  --border: rgba(20, 24, 30, 0.09);
  --shadow: 0 18px 50px rgba(21, 35, 55, 0.08);
}
```

Usage:

- `--background`: main page background.
- `--surface`: translucent card surface.
- `--text`: primary text, headings, and brand text.
- `--secondary`: body copy, footer text, and navigation links.
- `--accent`: links, eyebrow labels, CTA background, and focus outline.
- `--border`: card borders and footer divider.
- `--shadow`: standard soft card shadow.

The body background combines `--background` with a subtle radial gradient:

```css
radial-gradient(circle at 75% 0%, rgba(115, 180, 255, 0.16), transparent 34rem)
```

Button hover uses `#0056ad`.

Do not add new brand colors unless the user explicitly asks for a redesign or a new product accent. Prefer the existing variables.

## 3. Typography

Use the existing system font stack from `styles.css`:

```css
font-family:
  -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Arial,
  sans-serif;
```

Rules:

- Do not add Google Fonts or external font libraries.
- Use the existing system stack for all pages.
- Body text uses `17px` and `line-height: 1.6`.
- Headings use tight tracking and compact line-height:

```css
h1,
h2,
h3 {
  letter-spacing: -0.04em;
  line-height: 1.1;
}
```

Current heading sizes:

- Top-page `h1`: `clamp(3.4rem, 10vw, 7.5rem)`
- App/page title `.page-title`: `clamp(2.8rem, 8vw, 5rem)`
- `h2`: `clamp(2rem, 5vw, 3.5rem)`
- Card `h3`: `1.45rem`
- Content-card `h2`: `1.55rem`, `letter-spacing: -0.025em`

Small label style:

- `.eyebrow`
- `font-size: 0.78rem`
- `font-weight: 700`
- `letter-spacing: 0.12em`
- `text-transform: uppercase`
- color `--accent`

Button text:

- `font-size: 0.94rem`
- `font-weight: 650`

## 4. Layout

Use the shared width and spacing system.

Global page width:

```css
.site-header,
main,
footer {
  width: min(1080px, calc(100% - 40px));
  margin-inline: auto;
}
```

Mobile page width:

```css
width: min(100% - 28px, 1080px);
```

Standard app/page content:

- `.page-main`
- `max-width: 780px`
- `padding: 88px 0 120px`
- mobile: `padding: 64px 0 88px`

Top-page hero:

- `.hero`
- grid layout
- `min-height: 67vh`
- centered content
- mobile `min-height: 600px`

Top-page hero content:

- `.hero-content`
- `max-width: 820px`
- `padding: 88px 0 104px`

App cards:

- `.app-card`
- desktop grid: `auto 1fr auto`
- mobile grid: `auto 1fr`
- mobile link goes to column 2

Section spacing:

- `.section`: `padding: 96px 0 120px`
- mobile `.section`: `padding: 72px 0 88px`
- `.section-heading`: `max-width: 720px`, `margin-bottom: 40px`
- stacked cards: `margin-top: 22px`

Do not invent unrelated layout widths. Reuse `1080px`, `820px`, `780px`, and `720px` unless there is a clear reason.

## 5. Header / Navigation

Use the same header on every page.

Structure:

```html
<header class="site-header">
  <a class="brand" href="../">TAKUMI Lab</a>
  <nav aria-label="Primary navigation">
    ...
  </nav>
</header>
```

Top page uses `href="index.html"` for the brand. App subpages use `href="../"`.

Header rules:

- `.site-header`
- `display: flex`
- `align-items: center`
- `justify-content: space-between`
- `min-height: 72px`
- brand on the left
- navigation on the right
- navigation gap: `24px`

Brand:

- color `--text`
- `font-weight: 700`
- `letter-spacing: -0.02em`
- no underline on hover

Navigation links:

- color `--secondary`
- `font-size: 0.88rem`
- `font-weight: 600`
- default link hover underline

Do not create a custom header for one page. Use the existing `site-header`, `brand`, and `nav` patterns.

## 6. Footer

Use the shared footer on every page:

```html
<footer>
  <p>© 2026 TAKUMI Lab</p>
</footer>
```

Footer rules:

- width inherited from shared `footer` selector
- `padding: 28px 0 44px`
- `border-top: 1px solid var(--border)`
- color `--secondary`
- `font-size: 0.85rem`
- `footer p { margin: 0; }`
- no separate background

Keep the footer simple. Do not add large link groups unless the user asks.

## 7. Cards

Use existing card classes before adding new ones.

App list cards use `.app-card`:

```css
.app-card {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 24px;
  align-items: center;
  padding: 30px;
  border: 1px solid var(--border);
  border-radius: 26px;
  background: var(--surface);
  box-shadow: var(--shadow);
  backdrop-filter: blur(20px);
}
```

Content sections use `.content-card`:

```css
.content-card {
  padding: 34px;
  border: 1px solid var(--border);
  border-radius: 24px;
  background: var(--surface);
  box-shadow: var(--shadow);
}
```

Mobile content cards:

- `padding: 25px 22px`

Current cards do not use hover transforms or card transitions. Do not add card hover animations by default.

## 8. Buttons / CTA

Primary CTA uses `.button`:

```css
.button {
  display: inline-block;
  padding: 11px 21px;
  border-radius: 999px;
  color: white;
  background: var(--accent);
  font-size: 0.94rem;
  font-weight: 650;
}

.button:hover {
  background: #0056ad;
  text-decoration: none;
}
```

Text links use `.text-link`:

```css
.text-link {
  white-space: nowrap;
  font-weight: 650;
}
```

Rules:

- Use `.button` for primary page CTAs such as App Store links.
- Use `.text-link` for secondary actions such as Support and Privacy Policy.
- Do not create new button colors unless requested.
- If external links open in a new tab, use `target="_blank"` with `rel="noopener noreferrer"`.
- There is no defined active state beyond browser defaults.

## 9. App Icons and Images

Current app icons are 1024×1024 source assets:

- `swifkit-icon.png`
- `smart-gpa-icon.jpg`

App card icons use `.app-icon`:

- `display: block`
- `width: 72px`
- `height: 72px`
- `border-radius: 17px`
- `box-shadow: 0 10px 24px rgba(32, 96, 220, 0.25)`
- `object-fit: cover`

App page hero icons use `.app-icon app-icon-large`:

- desktop: `96px × 96px`
- desktop radius: `22px`
- mobile: `82px × 82px`
- mobile radius: `19px`

Hero icon layout:

- `.app-hero`
- `display: flex`
- `gap: 24px`
- `align-items: center`
- `margin-bottom: 18px`
- mobile gap: `18px`
- mobile `align-items: flex-start`

Rules:

- Keep app icons square.
- Do not crop, compress, or recolor icons unnecessarily.
- Always include useful `alt` text, e.g. `SwifKit app icon`.
- New app icons must visually match existing icon sizing, radius, shadow, and spacing.

## 10. Product Page Structure

Use Smart GPA and SwifKit overview pages as the standard product page model.

Default structure:

1. `<!doctype html>` and `<html lang="en">`
2. `<head>` with charset, viewport, description, title, stylesheet
3. Shared `.site-header`
4. `<main class="page-main">`
5. `.app-hero`
6. App icon (`.app-icon.app-icon-large`)
7. `.eyebrow` with `App`
8. `<h1 class="page-title">App Name</h1>`
9. `<p class="page-intro">Short description</p>`
10. Primary CTA if available (`.button`)
11. `<section class="content-card">` Overview
12. `<section class="content-card">` Main features
13. `<section class="content-card">` Support
14. `<section class="content-card">` Privacy
15. `<section class="content-card">` Contact when useful
16. Shared footer

Future app pages should follow this structure by default.

Metadata:

- Use app-specific `<title>`.
- Use app-specific meta description.
- Use OGP tags when already present on the comparable page or when adding a public product page.
- Do not leave another app’s name, icon, description, or URL in copied HTML.

## 11. Support Page Structure

Support pages use the shared app subpage pattern.

Default structure:

1. Shared header
2. Navigation back to Home, app overview, and Privacy where appropriate
3. `<main class="page-main">`
4. `.eyebrow` with `Support`
5. `<h1 class="page-title">App Name</h1>`
6. `.page-intro` with a one-sentence app summary
7. `.content-card` titled `Need help?`
8. Contact email link
9. `.content-card` titled `Privacy`
10. Link to `privacy.html`
11. Shared footer

Support copy should be concise and practical. Include device model and iOS version guidance when reporting technical issues.

## 12. Privacy Page Structure

Privacy pages use:

1. Shared header
2. Navigation back to Home/app/support as appropriate
3. `<main class="page-main">`
4. `.eyebrow` with the app name
5. `<h1 class="page-title">Privacy Policy</h1>`
6. `<p class="meta">Effective date: ...</p>`
7. Multiple `.content-card` sections
8. Contact section
9. Shared footer

Use factual, app-specific privacy language. Do not copy another app’s data practices unless they are actually true for the target app.

When Google AdMob is used, include the Google Privacy Policy link:

```html
<a href="https://policies.google.com/privacy" rel="noopener noreferrer">Google Privacy Policy</a>
```

## 13. Responsive Design

The current responsive breakpoint is:

```css
@media (max-width: 680px) { ... }
```

Responsive rules:

- Global horizontal page padding changes from `40px` total subtraction to `28px`.
- Top hero keeps a minimum height of `600px`.
- App cards switch from three columns to two columns.
- App card action link moves to the second column.
- Large app icons shrink from `96px` to `82px`.
- Page main padding reduces to `64px 0 88px`.
- Content cards reduce padding to `25px 22px`.
- Keep `body { min-width: 320px; }`.
- Avoid horizontal scrolling.

Always test new pages at desktop width and around `390px` mobile width.

## 14. Animation

Current animation is minimal.

Existing behavior:

- `html { scroll-behavior: smooth; }`
- `@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }`
- Link hover uses underline.
- Button hover changes background color.
- No transition declarations are currently defined.
- No JavaScript animation libraries are used.

Rules:

- Keep motion subtle and fast.
- Do not add flashy scroll effects.
- Do not add unnecessary parallax.
- Do not add animation libraries.
- Preserve `prefers-reduced-motion` behavior when adding motion.

## 15. Content Tone

TAKUMI Lab copy is simple, concise, confident, and product-first.

Use:

- short descriptions
- factual app capabilities
- minimal marketing language
- clear support and privacy wording
- English copy consistent with existing pages

Avoid:

- hype
- exaggerated claims
- “ultimate,” “revolutionary,” or similar inflated wording
- long paragraphs when a short section or list works
- features not verified in the app or existing site

## 16. Accessibility

Maintain these standards:

- Use semantic HTML (`header`, `nav`, `main`, `section`, `footer`).
- Use correct heading hierarchy.
- Include `alt` text for images.
- Use actual links for navigation and external destinations.
- Keep keyboard focus visible via existing `a:focus-visible` styling.
- Preserve readable contrast with `--text`, `--secondary`, and `--accent`.
- Use `aria-label` for navigation where appropriate.
- Do not make click-only elements that are not keyboard-accessible.

Existing focus style:

```css
a:focus-visible {
  border-radius: 6px;
  outline: 3px solid rgba(0, 102, 204, 0.3);
  outline-offset: 4px;
}
```

## 17. Do / Don’t

DO:

- Read this file before editing TAKUMI Lab pages.
- Reuse existing components and class names.
- Use existing CSS variables.
- Use existing spacing and max widths.
- Use the existing header and footer.
- Keep pages static unless interactivity is explicitly requested.
- Compare new app pages with both SwifKit and Smart GPA.
- Check mobile view.
- Verify links and image paths.
- Keep copy concise and factual.

DON’T:

- Add new fonts without explicit user approval.
- Add new brand colors unnecessarily.
- Build a separate design system per page.
- Add unnecessary gradients.
- Use heavier shadows than `--shadow`.
- Add strong animation or scroll effects.
- Perform a large redesign unless explicitly requested.
- Copy large duplicated CSS into individual HTML files.
- Leave copied product names, descriptions, icons, or URLs from another app.
- Break existing GitHub Pages paths.

## Current duplication and future cleanup candidates

The site already uses a shared `styles.css`, which is correct. Some page-level HTML patterns are repeated across app pages:

- header markup
- footer markup
- product page sections
- support page structure
- privacy page structure

This duplication is acceptable for a small static site. Do not introduce a build system solely to remove it unless the user asks.

Future cleanup could centralize design tokens further, but prefer the current variables instead of creating parallel names:

```css
:root {
  --background: #f5f7fb;
  --surface: rgba(255, 255, 255, 0.82);
  --text: #17181a;
  --secondary: #62666d;
  --accent: #0066cc;
  --border: rgba(20, 24, 30, 0.09);
  --shadow: 0 18px 50px rgba(21, 35, 55, 0.08);
}
```

If the site grows, consider adding named variables for repeated non-color values only after checking existing usage:

- content width: `1080px`
- page main width: `780px`
- card radius: `24px` / `26px`
- icon radius: `17px` / `22px` / `19px`
- mobile breakpoint: `680px`

Do not add these aliases unless there is a real maintenance need.
