---
name: security-hardening
description: Find where untrusted data or untrusted actors reach something that matters in a JS/TS backend, React web app, or React Native app, and put the right control there. Use when adding authentication or authorization, handling user input, storing or logging sensitive data, integrating an external service, reviewing code for vulnerabilities, or hardening before a launch.
---

# Security hardening

Locate the points where a system extends trust, then justify or control each one. This skill is about boundaries and the assumptions crossing them, not about running a scanner and closing tickets.

The defining constraint: the question is never "is this code secure", which has no answer, but "what does this code trust, and what makes that trust justified". Every real vulnerability is a place where trust was extended without anyone deciding to extend it. Find those, and the controls become obvious.

## Classify the trust

Sort every input into one of three tiers, and know which tier you are in at all times:

- **Untrusted.** Anything that crossed a network or a user: request bodies, params, query strings, headers, cookies, uploaded files, webhook payloads, third-party API responses, and anything read back from a client. Data does not become trusted by having been stored; a value a user wrote into your database is still theirs.
- **Validated.** Untrusted data that has passed through a schema at the boundary and come out typed. Validation converts, it does not merely check. Call the Skill tool with "api-design" for how the boundary is shaped.
- **Trusted.** Values your own code produced, and configuration you control. This is the only tier that may reach logic without a guard.

Most vulnerabilities are a tier confusion: something untrusted was read as though it were trusted, usually because it arrived by a path nobody was thinking about.

## Where the holes actually are

Ordered by how often they are the real finding, not by how much attention they get.

- **Broken access control.** The most common serious flaw, and the least likely to be caught by a tool. Every request must answer who is asking and whether they may touch this specific resource. Enforce it server-side, per object, not per route: an endpoint that checks a user is logged in and then trusts an id from the request lets any user read any record. Never rely on a hidden UI control as the enforcement.
- **Injection.** Untrusted values concatenated into an interpreted string: SQL, NoSQL query objects, shell commands, file paths, template expressions. Use parameterized queries and the library's escaping, never string building. A path assembled from user input needs normalizing and confining to its intended root.
- **Secrets.** Never in source, never in a client bundle, never in a log line, never in a URL. Read them from the environment through a validated loader so a missing one fails at startup rather than at midnight. Anything that reached a client is public, whatever it is named. A secret committed once is compromised, so rotate it rather than deleting the commit.
- **Sensitive data exposure.** Decide what counts as sensitive for this domain before writing the logger. Errors and traces are the usual leak: a stack trace to the client, a request body in a log, tokens in an analytics event. Redact at the point of logging, not by remembering to be careful.
- **Cross-site concerns, web.** Injected HTML is the risk React normally removes, so treat any escape from it as a decision requiring sanitization. Cookie-based sessions need CSRF protection and correct `SameSite`, `Secure` and `HttpOnly` flags. A content security policy is worth its configuration cost on anything public.
- **Supply chain.** Every dependency runs with your privileges. Call the Skill tool with "dependency-choice", which weighs maintenance and removal cost, and add the security axis: audit for known advisories, treat install scripts as code you are running, and pin what you cannot review.
- **Server-side request forgery.** Any feature that fetches a URL supplied by a user can be pointed at internal addresses and cloud metadata endpoints. Allowlist destinations rather than blocklisting them.

## By surface

- **Backend.** Authorization per object, parameterized data access, rate limiting on anything expensive or guessable, validated environment, no secret in a log, least privilege on the database and cloud credentials.
- **Frontend, React.** Nothing secret reaches the bundle, and no authorization decision is made only in the client. Treat the UI as a convenience over the server's rules. Sanitize any raw HTML, and keep tokens out of URLs and out of storage that other scripts can read.
- **Mobile, React Native.** The bundle ships to the device and can be read, so it holds no secret. Credentials belong in the platform keychain or keystore, never in async storage. Certificate handling stays strict; disabling validation for a staging environment has a way of shipping.

## Rules

- **Server-side or it did not happen.** A control the client enforces is a hint. Duplicate it in the UI for feedback, never for protection.
- **Validate at the edge, once, into a type.** Re-checking the same value in five places means nobody knows where the boundary is.
- **Deny by default.** New routes, new fields, new permissions start closed and open deliberately.
- **Least privilege everywhere.** Tokens, database roles, cloud credentials, and CI secrets get the narrowest scope that works, and an expiry where one is possible.
- **Never invent cryptography.** Use the platform primitive or a maintained library for hashing, signing, and encryption, and use it in the mode its documentation prescribes.
- **A finding is not a fix.** Naming a risk without either closing it or recording it as an accepted, owned decision leaves the system exactly as exposed as before.

## Excuses that do not hold

| Excuse | Why it fails |
| --- | --- |
| "It is internal, nobody outside can reach it" | Internal is a network claim, not a trust claim, and it stops being true the first time something is exposed for an integration. Access control is what makes it internal |
| "The UI does not show that button to those users" | The UI is not the enforcement layer. The request can be made without the UI, and eventually will be |
| "We will add auth before launch" | Authorization designed after the data model is a retrofit through every query. It is cheaper now and it is never cheaper later |
| "The data is already in our database, so it is ours" | A value a user wrote is untrusted no matter how long it has been stored. Stored input is still input |

## When this does not apply

A local script, a prototype nobody will deploy, and a pure refactor of code whose boundaries do not move do not need this pass. Reach for it when something crosses a trust boundary: a new input, a new caller, a new integration, a new place data comes to rest.

The shape survives where the rule yields. On a prototype that may later ship, say which controls you deliberately skipped, so that decision is visible to whoever promotes it rather than being discovered later.

## Before you hand it over

Check the change for the three findings that most often survive a security pass: an endpoint that authenticates but never authorizes the specific object, a value that reaches a query or a command without going through a schema first, and something sensitive that is now in a log, an error response, or a client bundle.
