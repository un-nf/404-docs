---
title: About Us
description: Learn about 404's mission to restore digital privacy through open-source anti-fingerprinting technology. Meet the team fighting surveillance capitalism one fingerprint at a time.
hide:
---

# About Us

## Who We Are

404 is a local TLS-terminating proxy built to address cross-session tracking through active fingerprint spoofing. It's currently maintained by a solo developer with a background in systems engineering, computational modeling, and education.

The project was founded in 2024 after recognizing that existing privacy tools (e.g. VPNs, private browsing modes, ad blockers) no longer address passive fingerprinting techniques that operate across multiple layers of the network stack. 404 is an attempt to give individuals and organizations practical control over how their devices appear on the web.

---

## Our Ethos

<div class="grid cards" markdown>

-   :material-shield-lock:{ .lg .middle } __Privacy as Default Infrastructure__

    ---

    Your device shouldn't broadcast dozens of unique identifiers every time you visit a website. Persistent tracking should not be the invisible default.

-   :material-home-circle:{ .lg .middle } __Local-First, Always__

    ---

    404 runs entirely on your machine. No cloud backends. No telemetry. Your data never touches our servers because **we don't have servers**.

-   :fontawesome-brands-github:{ .lg .middle } __Transparency Through Open Source__

    ---

    Every line of code is public.

-   :material-account-school:{ .lg .middle } __Accessible Privacy Tools__

    ---

    Anti-fingerprinting is technically demanding. A major goal of 404 is making privacy accessible to those who need it most.

</div>

---

## Why We Exist

Cross-session tracking has become foundational infrastructure for the modern web. It operates without meaningful consent, is difficult to detect, and is increasingly centralized through a small number of ad-tech and fraud-prevention vendors. Nearly all internet users are now subject to continuous, non-consensual measurement; infrastructure that lends itself to population-scale profiling.

The acute impact falls on communities operating under heightened scrutiny. Journalists, immigration attorneys, human rights organizations, and researchers rely on the open web to investigate sensitive topics, communicate with peers, or gather information on behalf of vulnerable populations. In these contexts, persistent client fingerprinting enables the correlation of browser activity across sessions, sites, and networks—exposing intent, professional focus, and organizational relationships. This creates tangible risk: legal pressure, political targeting, data breaches, and chilling effects on inquiry and advocacy.

Existing defensive tools no longer address this problem:

- **VPNs** hide your IP, but fingerprinting doesn't need it.
- **Incognito mode** clears cookies, but your device signature remains identical.
- **Ad blockers** stop requests, but [servers still collect device telemetry](https://unit42.paloaltonetworks.com/cname-cloaking/).
- **Privacy Browsers** work but trade convenience and break many modern sites.

404 addresses this gap by giving individuals and organizations practical control over how their devices appear on the internet. Rather than attempting to block trackers, 404 intercepts and modifies traffic to present believable but false device profiles, reducing linkability across sessions while remaining compatible with the modern web.

---

## The Problem

### Passive Fingerprinting

Modern tracking techniques collect hundreds of semi-unique data points to build device profiles that persist across:

- Cookie deletion
- Private browsing sessions  
- VPN connections
- Different browsers on the same device
- Network changes

Commercial fingerprinting services achieve 99.5%+ accuracy in identifying returning users. This type of metadata surveillance enables adversaries to map associations, track presence, monitor organizational behavior, and correlate activity without breaking encryption.

### Population-Scale Monitoring

Tracking operates on multiple layers that most privacy tools are not designed to control. If left unaddressed, passive fingerprinting will continue to normalize population-scale monitoring as an invisible default, further entrenching power imbalances between centralized tracking infrastructures and the communities they observe.

### The Illusion of Consent

"Cookie consent" banners are theater. By the time you see them, your fingerprint has already been logged, correlated, and sold. GDPR and CCPA are steps forward, but enforcement is weak and technical evasion is complex.

---

## Development Status

404 is in active development. Current priorities:

- **More profiles** (Safari, mobile browsers, Linux configs)  
- **Improved consistency** (reducing edge-case leaks)
- **Better UX** (reducing manual configuration)
- **External security audit** (for components that introduce the most technical risk)
- **Community contributions** (documentation, testing, profile tuning)

404 is not built for mass adoption, yet. It is infrastructure for individuals and organizations that need practical control over fingerprinting.

---

## Contributing

404 is open source. Contributions are welcome in the form of:

- **Testing** to identify fingerprint leaks and edge cases
- **Development** for code, profiles, and eBPF components
- **Research** documenting new tracking techniques and mitigations
- **Documentation** improving onboarding and technical clarity

[Contribute on GitHub](https://github.com/un-nf/404/blob/main/CONTRIBUTING.md){.md-button .md-button--primary}
[Join the Discussion](https://github.com/un-nf/404/discussions){.md-button}

---

## Contact

- **GitHub Issues**: Bug reports and feature requests  
- **GitHub Discussions**: General questions and implementation discussion
- **Email**: See [contact page](contact.md)
