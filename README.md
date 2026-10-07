# WOOTREX public website

Plain static HTML, CSS and JavaScript. No backend or runtime framework. Cloudflare Web Analytics is the only analytics provider; no advertising scripts or tracking cookies.

## Public URLs

Final canonical origin: https://wootrex.cz/

Landing pages: /cs/, /en/, /de/, /sk/, /pl/.
Privacy pages: /cs/privacy.html, /en/privacy.html, /de/privacy.html, /sk/privacy.html, /pl/privacy.html.

The root index.html contains complete Czech content. JavaScript chooses a supported browser language only at this entry point. Manual selection is remembered in localStorage as wootrex.language; this stores only a language code. Explicit localized URLs never redirect. Language links and compact navigation remain available without JavaScript.

The legacy privacy.html remains bilingual Czech/English, with a canonical link to /cs/privacy.html. Privacy claims and the 7 October 2026 date are preserved.

## Local preview

From this directory run:

    python -m http.server 8080

Open the local address printed by Python, then navigate to a language directory. E-mail CTAs require an e-mail client; no message is sent by this website.

## Editing and generation

- tools/templates/index.html — landing page source
- tools/templates/privacy.html — approved Czech/English privacy source
- tools/build_locales.py — translations and static page generation
- assets/css/style.css — shared presentation
- assets/js/main.js — navigation and reveal animations
- assets/js/language.js — language preference handling

Regenerate all pages:

    python tools/build_locales.py

The generator defaults to https://wootrex.cz/. To deliberately change the hosting origin, pass --base-url followed by the complete HTTPS origin and any project subpath. Canonical, hreflang and Open Graph metadata are regenerated together. Do not edit generated localized pages independently.

## GitHub Pages

The repository root is ready for branch-based static publishing. In GitHub Settings > Pages, choose Deploy from a branch, main, and / (root), then Save. The .nojekyll file disables Jekyll processing. Relative assets and language links also work under a GitHub Pages repository subpath. No routing rewrites or build process are needed.

Custom-domain configuration, DNS and HTTPS activation are separate manual deployment steps. No CNAME or Pages setting has been configured by this preparation. Canonical URLs target the intended domain; they do not prove that it is live.

## Asset provenance

Only public branding assets were copied from the separate gym_log Flutter repository:

| Website asset | Original repository-relative source |
| --- | --- |
| assets/images/wootrex-symbol.png | gym_log: assets/branding/wootrex_symbol.png |
| assets/images/favicon.png | gym_log: assets/branding/wootrex_app_icon.png |
| assets/images/wootrex-splash-logo.png | gym_log: assets/images/wootrex_splash_logo_transparent.png |

The sharp splash logo is used in current headers, hero, favicon and Open Graph metadata. Older branding files remain unused.

The supplied screenshots training.png.jpg, statistics.png.jpg and physique.png.jpg remain unchanged, including their Czech app UI. Surrounding captions and alt text are localized. No Outdoor screenshot was provided.

The progress illustration is not an app screenshot or actual data. No private Flutter files, databases, signing files or APKs belong in this repository.

## Release review items

Native-language review is recommended for DE/SK/PL privacy wording and fitness terminology. The feedback-email retention/deletion practice remains unconfirmed and should be resolved before store submission. Localization did not add privacy claims.

The audit checks static links, asset availability, language selection, responsive layouts, metadata and repository contents. It does not certify a live custom domain, DNS or store approval.

## Website analytics

The generator installs the supplied public Cloudflare Web Analytics beacon once before the closing body tag on all 12 public HTML pages. Source templates are not instrumented. The site token is public and is not a Cloudflare account API token. Privacy policies disclose aggregate website traffic and page usage analytics, with no advertising use, Google Analytics or sale of visitor data.

The snippet uses an absolute HTTPS script URL and is identical on the apex and www hostnames. Cloudflare hostname/rule settings and successful production reporting must be verified in the dashboard; repository changes do not configure these.
