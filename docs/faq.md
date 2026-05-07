---
title: Frequently Asked Questions
description: Frequently asked questions about 404—anonymity, data privacy, how the proxy works, and localhost configuration explained.
hide:
    - navigation
---

# FAQ

## Does 404 make me anonymous online? 

!!! Danger "No. Our goal is *not* to offer nation-state level evasion."

    If you require anonymity and/or plausible deniability from your online activity, there are tools that are better suited for your needs. 

404 aims to offer protection from *commercial grade* fingerprinting tools used by ad-tech companies like Google who collect and sell your data to third parties. Paired with a VPN, 404 offers fingerprint protection from most commercial grade fingerprinting tools (dataDome, FingerprintJS, etc.)

## Is 404 a desktop app or an open source repository?

Both, but the division matters.

- The **desktop app** is the managed product path.
- The **runtime stack** remains the open source self-hosted path.

This documentation site now covers both on purpose, with separate setup paths so those workflows do not get mixed together.

## How does 404 work?

!!! Example "404 pretends to be you as well as the server." 
    
In essence, your machine thinks it is talking to a website (google.com) and the website thinks it is talking to you (Firefox on Windows), but in reality both your machine and the server are talking to your locally hosted instance of 404.

YOU → 404 → `google.com`

`google.com` → 404 → YOU

This means that no website you visit sees your real fingerprint, only the one dictated by whatever 404 profile you're running.

## Does 404 ever see my data and/or logs?

!!! Danger "No, *BUT* the local app has clear access to the contents of your web traffic. Those logs never leave your machine."

404 hosts no infrastructure, nor do we plan to. In order to collect your data, we would need to host servers and allow you to connect to them. 

**No information ever leaves your machine and all mutation happens locally. Always.**

## Does the desktop app upload my traffic anywhere?

No. The desktop app manages a local runtime.

The product infrastructure handles things like account state, access control, and release delivery. It is not a cloud proxy path for your browsing traffic.

## Does 404 change my IP address?

!!! Failure "No."

In order to change your IP address, 404 would have to *route* your traffic through someone else's network. That is not the product model.

404 changes the fingerprint your machine presents. It does not replace a VPN.

## What is `localhost`?

!!! info "Localhost is the *local* interface that 404 listens on. Every machine comes with a pre-programmed *private* address, `127.0.0.1`, that allows local services to perform necessary tasks."

When you send a packet to `localhost`/`127.0.0.1`/`lo`, you are sending the packet back to its host machine. Applications pair this with a `port` to allow a computer to operate on data locally. 

The common ports now depend on how you launch the runtime:

- repo sample config: `127.0.0.1:4040`
- standalone binary with no config file: `127.0.0.1:8443`

There is also functionality to change the listening interface, but binding to `0.0.0.0` should be treated as an infrastructure decision, not a casual default, because it exposes the listener beyond strict local-only use.

## Does Windows still run STATIC as a native binary?

By default, no.

The current desktop product path on Windows uses a managed WSL2 runtime. The desktop app provisions and controls that Linux environment for you.

If you are operating the open source path manually, you can still work directly with STATIC and the distro build system yourself.

## Do I need an account?

For the **desktop app product path**, treat the account and licensing flow as part of the current distribution model.

For the **self-hosted open source path**, you can still clone, build, and run the runtime stack directly.