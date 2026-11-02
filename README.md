# takutakuja0803-del.github.io
TAKUMI Lab website and app support pages.

## App Registry

`data/apps.json` is the source of truth for shared app information: ID, name,
list descriptions, icon, ownership, operator, support contact and owner,
privacy owner, status, App Store URL, page URLs, visibility, and order.
`scripts/build_apps.py` writes static HTML into the marked regions of Home,
Projects, and each app detail page. App-specific descriptions, features,
Support copy, and Privacy Policy content remain in their own HTML files.
The generated HTML is served directly by GitHub Pages; visitors do not need
JavaScript or a runtime JSON request to see app information.

## Add or update an app

1. Read `AGENTS.md` and `TAKUMI_DESIGN.md`; compare SwifKit, Smart GPA, and Kama Chemistry.
2. Add the icon and app detail page using the existing CSS, navigation, relative links, and `APP_REGISTRY` markers. Add an app-specific Support page and a fact-checked Privacy Policy. For a client app, confirm the developer, operator, support contact, and privacy-policy owner separately; do not assume TAKUMI Lab handles support.
3. Add one entry to `data/apps.json`. Use a unique `id` and `order`. Set `showOnHome`, `showOnProjects`, and `featuredOnHome` deliberately. Local page URLs must point to existing files; Support and Privacy URLs may instead be HTTPS links to the responsible party's pages.
4. Set `status` to `Released`, `Pre-release`, `In Development`, or `Unconfirmed`. `Released` requires a verified `appStoreUrl`; all other statuses require `null`. Update `appStoreName` and `availabilityDetails` when applicable. Never invent release or privacy details.
5. Run `python3 scripts/build_apps.py`, then `python3 scripts/build_apps.py --check`. Commit both `data/apps.json` and the generated HTML after reviewing the diff. Do not edit content between `APP_REGISTRY` markers by hand; it will be regenerated.

Privacy text must reflect the app's real collection, storage, sharing, SDK,
analytics, and retention practices. If any are unverified, say so clearly and
confirm them with the developer or operator before release. Never copy
another app's privacy claims. The validator checks local page and asset
existence, required fields, ID/order uniqueness, release URL consistency,
internal links, and whether generated HTML is current. It cannot verify the
truth of product claims or availability of third-party HTTPS pages.
For `ownership: "client"`, the generated Home and Projects cards identify
the registered operator; the detail, Support, and Privacy pages must also
describe the correct responsible parties in their app-specific text.

## Local check and GitHub Pages

From the repository root, run `python3 scripts/build_apps.py --check` and
`python3 -m http.server 8000`. Open `http://localhost:8000/` and check Home,
Projects, each app's detail/Support/Privacy pages, and mobile widths. Stop
the server with Ctrl+C. This repository uses the username GitHub Pages URL
`https://takutakuja0803-del.github.io/` and relative asset/page paths.
After checks, commit the registry, generated HTML, and assets to the branch
configured as the Pages source, then push that branch. GitHub Pages publishes
the committed HTML directly; it does not run `build_apps.py` for you. Confirm
the Pages source branch and folder in the repository settings before release.
