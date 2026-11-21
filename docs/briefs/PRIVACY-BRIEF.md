# Privacy policy accuracy brief (vireault-site, 21 Nov 2026)

Repo Dixonchoi22/vireault-site. Work on the existing branch `feat/privacy-policy-accuracy` (this file is its first commit; delete this brief file in your last commit). Edit ONLY `public/privacy.html` (keep the site's existing style, header/footer, nav). Open ONE pull request into `main` titled "Privacy policy: describe what the app actually does". **Do NOT merge it** — it changes the owner's public policy and waits for his approval. Don't touch other open PRs (PR #6 is someone else's).

Plan first: post a short outline of the new sections, then edit.

## Facts to state (from the Vireault Android app source, repo Dixonchoi22/Vireault main; make NO claims beyond these)
- Unlock secret: PIN, pattern or passphrase. It is used on the device to derive the encryption key and is never sent anywhere. We (the developer) can't see, reset or recover it.
- Recovery: optional user-held 12-word recovery phrase that lets the user set a new unlock secret. Only the user holds it; we can't recover it or reset a vault by email. If the user skipped it and forgets the unlock secret, the vault can't be opened (unless they have their own separate encrypted backup and its recovery material).
- Encryption: keys derived with Argon2id; files encrypted with AES-256-GCM, on the device.
- Camera: only used when the user takes a photo/video inside the app; captures go straight into the encrypted vault, not the phone gallery. Nothing leaves the device.
- Microphone: only to record sound for videos the user records in the app. Nothing leaves the device.
- Biometrics (fingerprint/face via Android BiometricPrompt): optional unlock; biometric data is handled by Android and never reaches the app or us.
- The app's own code has no INTERNET permission, no analytics, no ads, no crash-reporting SDK, no accounts.
- Purchases (Pro subscription / lifetime) go through Google Play Billing; payment and purchase data are handled by Google under Google's privacy policy (link https://policies.google.com/privacy). We don't receive card details.
- Data deletion: data lives only on the device; uninstalling or deleting a vault removes it.
- Contact: one line, e.g. "Questions about this policy: use the developer contact email on Vireault's Google Play listing." Do NOT invent an email address.
- Update the "last updated" date to 21 November 2026.
Remove or fix anything currently on the page that contradicts the above (e.g. "PIN or pattern" only — add passphrase). Plain, short English.
