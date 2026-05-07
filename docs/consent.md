---
title: 404 Consent & Warning
description: Important warnings for both the desktop application and the CLI application. Covers local CA trust, TLS termination, data handling, and where the product legal documents live.
hide:
  - navigation
---

# Quick consent & warning

This page applies to both the managed desktop product path and the open source CLI application path.

*By running this software you understand that:*

- This proxy generates a local CA and key-pair for TLS interception.

- This proxy **terminates TLS**, usernames and passwords that pass through this proxy may be temporarily stored/visible in ***local only*** logs. Do not share logs. 

- This software changes local trust and routing behavior. Review the warnings and documentation before using it on a machine you care about.

*...and agree that:*

- You will not use your primary accounts.

- You will not share your CA certificate with anyone.

- If you find a security issue report it to support@404privacy.com

[Join the Discord for support!](https://discord.gg/X9QrVm6dqS){target="_blank"}

**Main Discussion:** GitHub discussions

> *Alternative community options coming soon!*

---

## Product path vs. self-hosted path

The legal surface is not identical across the whole stack.

### Desktop app

The desktop application is the proprietary managed product path.

Read the current public legal documents here:

- [Privacy Policy](https://404privacy.com/privacy/){target="_blank"}
- [Terms of Service](https://404privacy.com/terms/){target="_blank"}
- [EULA](https://404privacy.com/eula/){target="_blank"}

### CLI application

STATIC and the CLI application path remain open source.

Those components are documented here as repository and operator documentation and remain governed by their open source licensing terms.