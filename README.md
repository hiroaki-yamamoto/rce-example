# Example code that have RCE Vulnerability

## Important Note
**Don't use this code for production. This code contains Remote Code Execution
Vulnerability.**

## What This?
This is an example code to show what remote code execution is.

## So, What Remote Code Execution?
Remote Code Execution (RCE) is known as a vulnerability. It enables attacker to
log into your service and do **everything** by executing code remotely.
And again, **EVERYTHING**. Once this vulnerability is found, attacker can download
AWS secret key files, swiping user information data from the db, steal
crypto-currencies, and shut down your great service.

## Why I write this dangerous code
The most web services are secure as you know, but in recent days, there's very
few people who can consider the security of querystring. Especially, many services
in Japan don't validate querystring. So, I want to warn this problem...

## How to prevent
If you are not an engineer, you should hire an engineer who has knowledge of
cyber-security, and pay for the cost of the security.

If you are engineer, follow [CWE-20], and validate everything that might be
input from the user. In addition to this, following [CVE] might be an good idea.

[CWE-20]: https://cwe.mitre.org/data/definitions/20.html
[CVE]: https://cve.mitre.org/
