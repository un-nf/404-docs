# Documentation Plan Notes

This file captures the pieces that should be revisited deliberately rather than guessed at while restructuring the site.

## Open questions and follow-up

1. Add current desktop UI screenshots once the onboarding, dashboard, CA, and account views are frozen enough to document visually without creating maintenance debt.

2. Confirm how much pricing and trial detail should be mirrored inside 404-docs versus linked directly to `404privacy.com/pricing/`.

3. Add a version-compatibility matrix for desktop app builds versus runtime/distro contract versions once that compatibility policy is explicitly maintained as release-facing documentation.

4. Document a public manual signature-verification walkthrough for `/distro/manifest.json` once the desired user-facing public-key distribution story is finalized for operators who want to verify the published distro without reading the release workflows.

5. Decide whether the docs site should mirror the full legal text from `404privacy.com` or continue to link to the canonical hosted Privacy Policy, Terms of Service, and EULA pages.

6. Validate and then document the cleanest manual operator bootstrap path for the WSL distro without the desktop app, especially around first-write creation of `/opt/404/win-user`, runtime TOML authorship, and expectations for `/etc/wsl.conf` boot behavior across Windows builds.