---
title: Frequently Asked Questions
description: Frequently asked questions about 404—anonymity, data privacy, how the proxy works, and localhost configuration explained.
hide:
    - navigation
---

# FAQ

## Does 404 make me anonymous online? 

!!! Fail "No. Our goal is *not* to offer nation-state level evasion."

    If you require anonymity and/or plausible deniability from your online activity, there are tools like Tor that are better suited for your needs. 

404 aims to offer protection from *commercial grade* fingerprinting tools used by ad-tech companies like Google who collect and sell your data to third parties. Paired with a VPN, 404 offers fingerprint protection from most commercial grade fingerprinting tools (dataDome, FingerprintJS, etc.)

## How does 404 work?

!!! Example "404 pretends to be you as well as the server." 
    
    In essence, your machine thinks it is talking to a website (google.com) and the website thinks it is talking to you (Firefox on Windows), but in reality both your machine and the server are talking to your locally hosted instance of 404.

    YOU --> 404 --> `google.com`

    `google.com` --> 404 --> YOU

    This means that no website you visit sees your real fingerprint, only the one dictated by whatever 404 profile you're running.

## Does 404 ever see my data and/or logs?

!!! Danger "No. The local app has clear access to the contents of your web traffic, but those logs never leave your machine."

    404 hosts no infrastructure, nor do we plan to. In order to collect your data, we would need to host servers and allow you to connect to them. 

    **No information ever leaves your machine and all mutation happens locally. Always.**

## Does 404 change my IP address?

!!! Fail "No."

    In order to change your IP address, 404 would have to *route* your traffic. This goes against our core principles of local first mutation. You can, however (and should), follow the VPN integration steps to ensure that your persona location matches that of your VPN's advertised country. 

## What is `localhost`?

??? info "Localhost is the *local* interface that 404 listens on. Every machine comes with a pre-programmed *private* address, `127.0.0.1`, that allows local services to perform necessary tasks."

    When you send a packet to `localhost`/`127.0.0.1`/`lo`, you are sending the packet back to its host machine. Applications pair this with a `port` (4040 in our case) to allow a computer to operate on data locally. 

    By default 404 listens on `localhost:4040` but this can be changed to any desired port. There is also functionality to change the listening interface (e.g. `0.0.0.0` for *all* interfaces), but this is *not suggested* as this opens your proxy up to all devices on your `LAN`