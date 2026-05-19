# Security Policy

This repo ships default security guardrails into future repos. A vulnerability
here can propagate into every project created from the template.

## Reporting

Report template security issues privately to `chinu.ramraika@gmail.com`.

## In scope

- Unsafe defaults in generated workflow files or hooks
- Missing deny-list or secret-ignore patterns in the shipped scaffold
- Generated files that encourage insecure deployment or secret handling

## Scope note

This policy covers the template itself. Repos created from this template should
carry their own `SECURITY.md` tailored to their runtime and data profile.

