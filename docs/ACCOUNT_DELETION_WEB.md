# Account deletion request page — draft, not published

/cs/odstraneni-uctu/ provides a discoverable email request to the existing published privacy contact wootrex@seznam.cz, independently of an installed app. Operators must confirm mailbox ownership, audit the live cloud inventory, remove only that account's data, and confirm outcome/any necessary retention. Do not delete solely on a submitted email address, do not ask for passwords by email, and define a monitored response/processing policy before publication.

The separate automatic form is OFF by default. It sends a password only to Supabase Auth over HTTPS, stores no access/refresh token, and saves only a random recovery receipt plus its temporary owner marker in tab-scoped sessionStorage. No analytics or feedback script runs on this page. The Edge endpoint derives the owner from a verified current session, never from form-supplied user IDs.

Before enabling: deploy and accept the app PR's delete-account/deletion-status functions and approved server inventory on staging; verify CORS and quotas/rate limits; set only public Supabase URL/publishableKey in assets/js/account-deletion-config.js and enabled:true; test dedicated A/B accounts, lost response, invalid password and account mismatch. Never put service-role secrets in this repository. Keep automatic form disabled if the backend is not verified. Publish this page/policy and enter its actual public URL in Google Play Data Safety before app release.

Privacy updates cover existing accounts, local/cloud scope, maps, feedback and planned Free/Pro without claiming functional payments. Verify controller legal identity, hosting/retention, processing time, all translations and actual SDK/network behavior before store submission. Root privacy.html points to the canonical current Czech policy. Existing APK/TestFlight links and site design are unchanged.

Local validation:16 Node checks passed (7 deletion/page/flow checks plus9 existing beta/manifest checks). These use synthetic requests; no real account or message was deleted/sent. No main merge or production deployment by this change.
