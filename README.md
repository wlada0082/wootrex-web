# WOOTREX public website

Plain static HTML, CSS and JavaScript. No backend or runtime framework. Cloudflare Web Analytics is the only analytics provider; no advertising scripts or tracking cookies.

## Public URLs

Final canonical origin: https://wootrex.cz/

Landing pages: /cs/, /en/, /de/, /sk/, /pl/.
Privacy pages: /cs/privacy.html, /en/privacy.html, /de/privacy.html, /sk/privacy.html, /pl/privacy.html.

The root index.html contains complete Czech content. JavaScript chooses a supported browser language only at this entry point. Manual selection is remembered in localStorage as wootrex.language; this stores only a language code. Explicit localized URLs never redirect. Language links and compact navigation remain available without JavaScript.

The legacy privacy.html remains bilingual Czech/English, with a canonical link to /cs/privacy.html. Privacy claims and the 8 October 2026 date are preserved.

## Local preview

From this directory run:

    python -m http.server 8080

Open the local address printed by Python, then navigate to a language directory. Feedback is submitted within the page after the backend becomes available. Beta CTAs download the Android APK.

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

## Direct feedback

assets/js/feedback.js provides a localized internal dialog, POSTing JSON to https://feedback.wootrex.cz/feedback in production and local previews. No credentials or email client are used. The feedback API is deployed with a verified HTTPS Custom Domain and D1 storage. Backend sources are separate in wootrex-feedback-api. Privacy drafts describe the upcoming API/D1 flow and existing Beta 1 email behavior; confirm retention/deletion before release.

## Beta CTA click measurement

assets/js/beta-cta.js routes the beta CTAs by device and additionally measures clicks anonymously. Buttons tagged with data-cta (hero, nav, platform_section) fire a non-blocking sendBeacon/fetch keepalive POST with a text/plain body to https://click.wootrex.cz/e/beta-click, a Cloudflare Worker endpoint hosted in wootrex-admin-online. The beacon never calls preventDefault, so the APK download and TestFlight page open immediately even if tracking fails.

Only four whitelisted fields leave the browser: platform_target (android|ios, derived from the exact destination URL), language (cs|en|de|sk|pl), source_cta and device_type (derived from the user agent). No cookies, no IP storage, no user agent transmission, no identifiers and no fingerprinting. A click means interest, not a confirmed install; the GitHub release download_count stays the separate install proxy. The privacy page documents this processing.

Tests (Node.js, no dependencies): node --test tools/test


## Czech fitness portal

The root and /cs/ now introduce the app alongside a Czech content magazine. /cs/aplikace/ contains the current distribution section, sourced from the established localized landing template during generation. #beta and #ios-beta remain valid on the Czech home page. /cs/stazeni/ preserves the full original landing and contact/feedback flow. EN/DE/SK/PL landing pages, all privacy policies, update.json and the beta measurement script retain their established behavior.

Continue generating with `python tools/build_locales.py`. It calls tools/build_fitness_portal.py after the localized landing generation. Portal content templates live in tools/fitness_portal/pages/; shared presentation and optimized media are in assets/fitness/. Do not edit the generated portal pages directly. The portal builder adapts routes, metadata, analytics, language selection and current beta details to the publication origin.

The six original sample articles are visibly marked as editorial concepts and use noindex,follow; they are omitted from sitemap.xml. The three sourced strength-training articles and catalog plan pages are published and indexable. The main pages are indexable. Recipe status and the screenshot montage are disclosed on their pages. The generated robots.txt allows the site and excludes the source tools directory.

The illustrative dumbbell photograph was created using ImageGen for this project and optimized as WebP for publication; it is identified as an illustration. Original app screenshots and logo are reused without changing their contents.


### Training library and published articles

`tools/fitness_portal/training_plans.json` is a reviewed snapshot of the app catalog. Its source metadata records the app commit and check date; website generation never requires the app checkout or private app configuration. Preserve exercise order, per-exercise set overrides, rep ranges and cardio intervals when updating it. The website provides descriptions and instructions for finding the templates in the app; it does not import plans automatically.

The three published article bodies are in `tools/fitness_portal/articles/`; titles, publication date and linked research references are in `training_articles.json`. `tools/training_content.py` adds these articles, related reading, the filterable plan library and individual plan pages to the existing templates. Article citations identify study populations and practical limits. Do not turn study outcomes into promises of individual results or describe the text as independently clinically reviewed.

Run `python tools/build_locales.py`, then `node --test tools/test`. Published articles include Article structured data, canonical URLs and sitemap entries. CSS and portal JavaScript URLs are content-versioned so updated filtering reaches returning visitors.
