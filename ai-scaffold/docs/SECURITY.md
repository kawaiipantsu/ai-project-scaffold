# Security Policy

This document defines the security requirements and secure coding practices for this project.

These rules apply to all developers, contributors, AI coding agents, automated tools, applications, services, APIs, infrastructure, and deployment configurations associated with the project.

Security must be considered during implementation, not added as an afterthought.

---

## 1. User Requirements Take Priority

Always consider the user's initial prompt, requirements, environment, and deployment architecture before making security-related implementation decisions.

Do not blindly enable, disable, or modify infrastructure-level security features without understanding how the application will be deployed.

For example, HTTPS/TLS may be:

* Handled directly by the application.
* Terminated by a reverse proxy.
* Terminated by a load balancer.
* Terminated by an ingress controller.
* Managed by a CDN or cloud provider.
* Managed elsewhere in the user's infrastructure.

Do not duplicate or conflict with security controls already handled upstream.

However, never weaken application-level security simply because upstream security may exist.

---

# Secure Coding

## 2. General Secure Coding

Always follow secure coding best practices.

At minimum:

* Validate untrusted input.
* Sanitize input where appropriate.
* Encode output for its destination/context.
* Use parameterized queries or safe ORM/database APIs.
* Prevent SQL, command, template, and other injection attacks.
* Prevent path traversal.
* Prevent unsafe file access.
* Prevent insecure deserialization.
* Avoid arbitrary code execution.
* Use safe APIs instead of executing shell commands when possible.
* Apply authentication where required.
* Apply authorization independently of authentication.
* Enforce authorization server-side.
* Follow least-privilege principles.
* Use secure defaults.
* Fail securely.
* Do not expose unnecessary implementation details in errors.
* Keep security-sensitive logic simple and auditable.
* Use established cryptographic libraries instead of implementing cryptography manually.

Never trust data merely because it originated from the frontend.

All security-critical validation and authorization must be enforced by the trusted backend.

---

# Credentials & Sensitive Information

## 3. Never Expose Secrets

Never expose, leak, log, return, display, commit, embed, or otherwise disclose sensitive information.

This includes, but is not limited to:

* Usernames
* Passwords
* Database credentials
* API keys
* Access tokens
* Refresh tokens
* Session tokens
* Authentication cookies
* Private keys
* Encryption keys
* Signing keys
* SSH keys
* Certificates containing private keys
* OAuth client secrets
* Webhook secrets
* Service-account credentials
* Connection strings containing credentials
* Internal authentication information
* Recovery codes
* Secret configuration values
* Internal infrastructure information that creates unnecessary security exposure

Never place real credentials or secrets in:

* Source code
* Git history
* Documentation
* Examples
* Tests
* Fixtures
* Frontend bundles
* URLs
* Error messages
* Debug output
* Screenshots
* Logs
* Generated files

Follow the repository's credential documentation, including `CREDS_PREDEFINED.md` and `CREDS_DB.md`.

---

## 4. Environment Variables Are Not Automatically Safe

Environment variables may be appropriate for secrets, but their use does not automatically make a system secure.

Ensure secrets are not:

* Printed during startup.
* Included in debug dumps.
* Returned by diagnostic endpoints.
* Exposed through frontend environment variables.
* Included in client-side JavaScript bundles.
* Written into generated configuration files unintentionally.
* Exposed by CI/CD logs.

Only expose configuration to clients when it is explicitly intended to be public.

---

## 5. Logging

Never log sensitive values.

Logs should avoid containing:

* Passwords
* Tokens
* API keys
* Authorization headers
* Session cookies
* Private keys
* Database credentials
* Complete connection strings
* Sensitive personal information
* Secret request parameters

Redact sensitive fields where logging is necessary.

Production error responses should not expose stack traces, filesystem paths, database internals, environment variables, or internal service information.

---

# HTTPS, TLS & mTLS

## 6. HTTPS

Use HTTPS whenever it is applicable and available.

Plain HTTP should not be used for sensitive production traffic.

HTTPS may be handled upstream by infrastructure such as a:

* Reverse proxy
* Load balancer
* CDN
* API gateway
* Kubernetes ingress
* Cloud platform

Respect the deployment architecture specified by the user.

If TLS terminates upstream, configure the application appropriately for that architecture rather than unnecessarily implementing a second conflicting TLS layer.

Applications behind trusted proxies must correctly handle forwarded protocol information only from explicitly trusted proxies.

---

## 7. TLS

Use modern, maintained TLS implementations and secure defaults.

For new systems:

* Prefer TLS 1.3.
* Support TLS 1.2 when compatibility requires it.
* Do not enable obsolete SSL/TLS protocols.
* Do not weaken cipher configuration solely to support obsolete clients.
* Use certificates with appropriate validation.
* Verify certificate chains and hostnames when acting as a client.
* Never disable certificate verification as a permanent workaround.

Avoid SSLv2, SSLv3, TLS 1.0, and TLS 1.1.

When configuring cipher suites manually, use modern authenticated encryption and follow current platform/library recommendations.

Prefer secure algorithms such as:

* AES-GCM
* ChaCha20-Poly1305

Prefer ephemeral key exchange providing forward secrecy where TLS 1.2 configuration requires explicit cipher selection.

Do not enable known-obsolete cryptographic algorithms or cipher suites such as:

* NULL encryption
* EXPORT ciphers
* RC4
* DES
* 3DES
* Anonymous cipher suites

Whenever possible, prefer the secure defaults supplied by a current, maintained TLS library rather than maintaining a custom cipher list.

---

## 8. mTLS

Use mutual TLS (mTLS) when required by the user's architecture or when strong service-to-service authentication is appropriate.

When using mTLS:

* Validate client certificates.
* Validate server certificates.
* Verify certificate chains.
* Verify identities appropriately.
* Protect private keys.
* Establish certificate rotation procedures.
* Reject invalid, expired, or unauthorized certificates.
* Do not disable verification for convenience.

Do not introduce mTLS unnecessarily when authentication and transport security are already appropriately handled by the intended infrastructure.

---

# Web Security

## 9. CORS

Web applications and APIs must configure Cross-Origin Resource Sharing (CORS) deliberately.

Do not blindly allow every origin.

Prefer an explicit allowlist of trusted origins.

Avoid configurations equivalent to:

`Access-Control-Allow-Origin: *`

when endpoints expose authenticated, private, privileged, or sensitive functionality.

Never dynamically reflect arbitrary origins without validating them against an approved allowlist.

Only allow:

* Required origins
* Required HTTP methods
* Required headers
* Credentials when actually necessary

Remember that CORS is a browser security mechanism and **not an authorization system**.

Backend authentication and authorization must still be enforced.

---

## 10. Content Security Policy

Web applications should use a restrictive Content Security Policy (CSP) whenever applicable.

Start from a restrictive policy and explicitly allow required resources.

Avoid unnecessarily broad directives.

In particular, avoid allowing:

* Arbitrary script origins
* Arbitrary frame origins
* `unsafe-eval`
* `unsafe-inline`

unless there is a documented and unavoidable requirement.

Prefer nonces or hashes for scripts when appropriate.

Consider appropriate directives such as:

* `default-src`
* `script-src`
* `style-src`
* `img-src`
* `font-src`
* `connect-src`
* `frame-src`
* `frame-ancestors`
* `object-src`
* `base-uri`
* `form-action`

A typical security-oriented starting point should restrict unspecified resources rather than permit everything.

CSP should be adapted to the actual application rather than copied blindly.

---

## 11. Security Headers

Web applications should configure appropriate security headers.

Depending on the application and deployment architecture, consider:

* `Content-Security-Policy`
* `Strict-Transport-Security`
* `X-Content-Type-Options`
* `Referrer-Policy`
* `Permissions-Policy`

Clickjacking protection should be implemented using CSP `frame-ancestors` where possible.

`X-Frame-Options` may additionally be appropriate for compatibility.

HSTS should only be configured where HTTPS behavior and deployment architecture are understood.

Do not enable HSTS settings blindly for domains or subdomains that may still require HTTP.

---

# Files & Directories

## 12. Protect Sensitive Files

Sensitive files and directories must never be publicly accessible through web servers, static file handlers, object storage, application routes, or generated artifacts.

Examples include:

* `.env`
* `.env.*`
* `.git/`
* `.github/` when not intentionally exposed
* Configuration files containing secrets
* Credential files
* Private keys
* SSH keys
* TLS private keys
* Database files
* Database dumps
* Backups
* Temporary files
* Debug files
* Log files
* Source maps containing sensitive information
* Internal documentation
* Deployment configuration
* CI/CD configuration containing sensitive information
* Secret-management files
* Development-only endpoints

Web servers should explicitly restrict access to sensitive files and directories where applicable.

Do not rely solely on obscurity or unusual filenames.

---

## 13. Static File Serving

Never expose an entire project directory as a static/public directory.

Use a dedicated public/static directory containing only files intentionally intended for public access.

Prevent:

* Directory traversal
* Directory listing
* Access outside the configured public root
* Serving dotfiles unintentionally
* Serving source/configuration files unintentionally
* Symlink-based escapes where applicable

Treat uploaded files as untrusted.

---

# Authentication & Authorization

## 14. Authentication

Use established authentication mechanisms and libraries.

Do not implement custom password hashing, token formats, session cryptography, or authentication protocols unless explicitly required and appropriately reviewed.

Passwords must be stored using an appropriate password-hashing algorithm, never reversible encryption or plaintext.

Use maintained implementations of algorithms such as:

* Argon2id
* bcrypt
* scrypt

Choose parameters appropriate for the environment and current security recommendations.

---

## 15. Authorization

Authentication does not imply authorization.

Every sensitive operation must verify that the authenticated identity is authorized to perform that specific action.

Do not rely on:

* Hidden frontend controls
* Client-provided roles
* Client-provided ownership identifiers
* Disabled buttons
* Obscure URLs

Authorization must be enforced on the trusted server side.

Follow least privilege.

---

# Sessions & Cookies

## 16. Secure Sessions

Session identifiers must be unpredictable and securely generated.

For cookies containing authentication/session information, use appropriate protections such as:

* `Secure`
* `HttpOnly`
* `SameSite`

Select the `SameSite` policy according to actual application requirements.

Do not place sensitive session information directly into client-readable cookies unless the design explicitly requires it and it is appropriately protected.

Implement reasonable session expiration, invalidation, and rotation behavior.

---

# Input, Output & Injection Protection

## 17. Treat External Input as Untrusted

Treat all external input as potentially malicious.

This includes:

* HTTP requests
* Query parameters
* Form fields
* JSON
* Headers
* Cookies
* File uploads
* Webhooks
* Database content originating from users
* Third-party API responses
* Imported files
* URLs
* Command-line arguments
* Messages from queues or event systems

Validate according to the expected type, format, size, and allowed values.

---

## 18. Injection Prevention

Never construct database queries by concatenating untrusted input.

Use parameterized queries, prepared statements, or safe ORM interfaces.

Similarly, never place untrusted input directly into:

* Shell commands
* HTML
* JavaScript
* Templates
* File paths
* LDAP queries
* XML/XPath expressions
* Regular expressions with security implications

Use context-appropriate escaping, encoding, validation, and safe APIs.

---

# File Uploads

## 19. File Upload Security

When file uploads are supported:

* Restrict allowed file types.
* Restrict file sizes.
* Generate safe server-side filenames.
* Do not trust client-provided MIME types.
* Do not trust file extensions alone.
* Prevent path traversal.
* Store uploads outside executable locations when possible.
* Prevent uploaded files from becoming executable code.
* Apply authorization to private files.
* Consider malware/content scanning when appropriate for the threat model.

Never allow an uploaded filename to control an arbitrary filesystem path.

---

# Network & External Requests

## 20. Outbound Requests

Treat externally supplied URLs as untrusted.

Applications making server-side HTTP requests must consider Server-Side Request Forgery (SSRF).

Where applicable, prevent access to:

* Loopback interfaces
* Private/internal networks
* Cloud metadata endpoints
* Internal administrative services
* Unix/local sockets
* Unexpected protocols

Use explicit allowlists where the application's purpose permits them.

---

# Cryptography

## 21. Cryptographic Practices

Do not design custom cryptographic algorithms or protocols.

Use established, maintained cryptographic libraries.

Use cryptographically secure random number generators for:

* Tokens
* Session identifiers
* Password reset links
* Security codes
* Nonces
* Cryptographic keys

Do not use general-purpose pseudo-random generators for security-sensitive values.

Never hard-code cryptographic keys.

---

# Dependencies

## 22. Dependency Security

Minimize unnecessary dependencies.

Before introducing a dependency:

* Determine whether it is actually needed.
* Prefer actively maintained packages.
* Prefer established packages with clear provenance.
* Avoid abandoned or suspicious packages.
* Review relevant security implications.

Keep dependencies reasonably current, particularly when security updates are available.

Do not automatically upgrade major versions without considering compatibility and project requirements.

---

# Production Security

## 23. Debug & Development Features

Production deployments must not unintentionally expose:

* Debug mode
* Development servers
* Interactive debuggers
* Profilers
* Test endpoints
* Internal administration endpoints
* Stack traces
* Environment dumps
* Development credentials
* Mock authentication
* Test accounts with known credentials

Development conveniences must not silently become production vulnerabilities.

---

## 24. Error Handling

Return useful but non-sensitive errors.

External users should not receive unnecessary details about:

* Filesystem paths
* Database schemas
* SQL queries
* Internal hostnames
* Private IP addresses
* Environment variables
* Credentials
* Stack traces
* Internal implementation details

Record diagnostic information securely where needed without leaking secrets into logs.

---

# AI Agent Security Requirements

## 25. Instructions for AI Agents

AI agents working on this repository must actively consider security while implementing or modifying code.

Before completing security-relevant work:

1. Review this file.
2. Review the user's original requirements.
3. Inspect the existing security architecture.
4. Determine whether TLS/HTTPS is handled by the application or upstream.
5. Check authentication and authorization boundaries.
6. Check CORS configuration when applicable.
7. Check CSP and relevant HTTP security headers for web applications.
8. Ensure sensitive directories and files cannot be served publicly.
9. Check that credentials and secrets cannot reach source code, logs, frontend bundles, or responses.
10. Validate external input at appropriate trust boundaries.
11. Run available security-related tests and tooling where applicable.
12. Report any security limitation that could not safely be resolved.

Do not weaken existing security controls simply to make an implementation easier.

Do not disable certificate validation, authentication, authorization, CORS protections, CSP, input validation, or other security mechanisms merely to resolve development errors.

Fix the underlying configuration or implementation instead.

---

# Security Decision Principles

When multiple implementations are possible, prefer the option that is:

1. Secure by default.
2. Least privileged.
3. Simple to understand and audit.
4. Compatible with the user's intended architecture.
5. Based on established standards and maintained libraries.
6. Explicit about trust boundaries.
7. Resistant to accidental exposure.

Security controls must be appropriate to the actual project.

Do not blindly add controls that conflict with the user's deployment model, but never silently reduce security because the environment is uncertain.

When a security-sensitive decision cannot safely be inferred, consult the relevant project documentation or request clarification.
