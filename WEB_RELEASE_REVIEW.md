# Web release review —27 October2026

Reuses PR7 deletion routes and PR8 privacy completion. No duplicate endpoint,
request form or backend. This release changes only static website content/assets.

## Verified before deployment
-53 Node DOM/network/content tests PASS; all HTTP mutations are mocked with
 synthetic credentials. No real feedback email, login or deletion was sent.
-2 Python tests PASS, including the full locale/portal generator twice in an
 isolated copy and matching output/sitemap/manual request routes.
-All5 deletion and5 privacy pages checked in actual320px browser viewport:
 no horizontal overflow after German heading fix. Czech request and feedback
 dialog also inspected at390px. Automatic credential form hidden/disabled by default.
-Local links/assets resolve; root deletion entry links/canonical to Czech route.
 Sitemap includes all5 request routes. Versioned policy CSS avoids old CSS cache.
-CNAME/update.json and existing Beta138 download/TestFlight destinations unchanged.
-GitHub Pages settings: main/root branch publishing, existing wootrex.cz domain,
 Enforce HTTPS already enabled. main not protected; PR8 has no required check runs.
 No Pages/DNS/security settings were modified.

## Public behavior
Prominent mailto request to the established wootrex@seznam.cz contact works without
JavaScript or installed app. Users send their own email; no password/code/photo
is requested by this manual route. It explicitly asks for account and associated
online data removal and explains ownership verification, phone-only data, exports,
feedback/email requests, store subscriptions and provider retention limitations.
No assertion that submitting email automatically deletes anything. No instruction
to uninstall merely to request account removal. Automatic backend config remains
false with an empty publishable key; no production account operation can start.

Policies now describe current optional Supabase accounts, local workout/photo scope,
actual feedback fields, Cloudflare processing and inactive production purchases.
No guessed legal identity, guaranteed processing deadline or unsupported immediate
provider-log/backup erasure. The same source updates all5 policies and bilingual root.

## Remaining operational gates
Owner must monitor/verify the support inbox, authenticate requests safely and
actually fulfill account/associated-data deletion, including relevant processors.
Exact legal/operator and retention details remain for owner confirmation before
store submission. Receiving/processing real mail was NOT tested. Automatic
managed Supabase deletion remains disabled pending independent staging acceptance.
These are not claims of Google approval. Google permits a customer-service email
request path: https://support.google.com/googleplay/android-developer/answer/13327111

## Deployment strategy
Merge reviewed PR8 into the PR7 branch first, then PR7 into main, so only the final
combined content reaches Pages. Do not run or alter mobile PR50, keys, binaries,
Supabase production, payments or beta release manifest. Verify Pages run and actual
HTTPS URLs afterward; if Pages is quota-blocked, do not rerun blindly or claim live.
