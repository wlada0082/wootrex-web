# Privacy completion on web PR7

Base: existing draft PR7 b4316335a57e51aaae076ba52ebf9c497da66bb3. Its five localized delete-account.html pages, exact-origin automatic form, disabled public config, CSP and manual support path are reused unchanged. No second deletion form/config is retained. Companion backend remains app PR41; app PR42 adds native initiation and optional receipt recovery.

This PR adds actual Supabase-account disclosures, local/cloud separation and explicitly unfinished Free/Pro/payment descriptions in all five policies plus the bilingual root. tools/account_privacy_content.json is the maintained multilingual source; the locale builder calls the tested postprocessor so regeneration preserves the new content. Existing download/TestFlight links and site design are unchanged.

Before publication confirm operator legal identity, hosting/processors, provider logs/backups and receipt retention, and a monitored ownership-verified email request process. Do not delete solely on an unverified email and never request a password by email. Use existing wootrex@seznam.cz contact. Account deletion is not subscription cancellation or remote phone-data erasure.

The existing automatic form stays OFF with no public key. Enable only after real staging Auth/Deno/CORS/concurrency acceptance and reviewed server activation. Never publish service-role keys. App release requires the actual public deletion URL, not merely a draft PR.

Available checks:14 Node policy/beta/content tests,1 Python idempotence/regeneration test. PR7's15 existing DOM/network checks are documented parent evidence; they are not re-claimed as a new run. No production publication, email dispatch, real login or deletion occurred. CI account limits remain a separate release gate; no repeated blocked workflow was requested.
