# WOOTREX website

Official Czech landing page, with Czech and English privacy policy. Plain static HTML, CSS and JavaScript; no build step, backend, external dependencies, analytics, cookies or trackers.

## Files

- index.html — landing page
- privacy.html — Czech / English privacy policy, updated 7 October 2026
- assets/css/style.css — responsive design and reduced-motion support
- assets/js/main.js — accessible mobile menu and reveal animations
- assets/images/wootrex-symbol.png — public WX brand asset
- assets/images/favicon.png — public app icon used as favicon
- README.md — setup, deployment and asset provenance

## Local preview

From this directory run:

    python -m http.server 8080 --bind 127.0.0.1

Open http://127.0.0.1:8080/. Both HTML files also work when opened directly.

## Hosting

Publish this directory to any static host. Keep the assets directory beside both HTML pages. No routing rewrites are needed. Connect the registered WOOTREX domain in the host's settings and enable HTTPS.

Before public launch, set og:image to an absolute HTTPS URL for the deployed brand image on both pages. Add og:url and a canonical URL once the final domain is known; no domain was guessed. Review the privacy policy against the released application's behavior and the selected hosting provider's handling of access logs. Update this page before introducing new online data processing.

## Branding provenance

Only these public branding assets were copied from the Flutter project:

| Website file | Original source |
| --- | --- |
| assets/images/wootrex-symbol.png | C:\Projekty\gym_log\assets\branding\wootrex_symbol.png |
| assets/images/favicon.png | C:\Projekty\gym_log\assets\branding\wootrex_app_icon.png |

The progress artwork is an HTML/CSS/SVG illustration, explicitly labeled as neither an application screen nor real data. It can later be replaced by approved public screenshots.

All beta links open mailto:wootrex@seznam.cz?subject=WOOTREX%20Beta. There are no APK downloads.

## Verification checklist

Check desktop and mobile layouts, navigation toggle and Escape handling, keyboard focus, all section links, both privacy language anchors, and reduced-motion behavior. E-mail links require an e-mail client. Without JavaScript all content remains visible; the main sections can still be reached by scrolling.

No commit or push is part of this implementation.

## Splash logo update

The header, hero, privacy header, Open Graph image and favicon now use assets/images/wootrex-splash-logo.png, copied unchanged from C:\Projekty\gym_log\assets\images\wootrex_splash_logo_transparent.png (1254 x 1254, transparent). This is the exact asset referenced by WootrexIntro.logoAsset in lib/widgets/wootrex_intro.dart. The older intro logo is 1024 x 1024; the current startup asset provides higher resolution and matches the app. Header display sizes are 48px desktop / 40px mobile; hero sizes are 300px desktop / 220px mobile, with sufficient source pixels for retina displays. The original website logo and favicon files remain available but are no longer referenced.
