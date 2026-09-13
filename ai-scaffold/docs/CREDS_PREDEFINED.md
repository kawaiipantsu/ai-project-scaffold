# Predefined Credentials & Authentication

This document defines how application credentials, initial administrator accounts, authentication secrets, recovery mechanisms, user management, RBAC, and authentication audit events should be handled.

These requirements apply to developers, contributors, AI coding agents, automated tooling, and application components that implement authentication or credential storage.

Always consider the user's original requirements first.

Security should support the user's desired level of simplicity without silently removing important protections.

---

# Core Principles

Authentication systems should be:

* Secure by default.
* Simple for legitimate administrators to operate.
* Resistant to accidental credential exposure.
* Recoverable without hidden backdoors.
* Capable of supporting role-based access control when needed.
* Auditable.
* Appropriate for the project's actual deployment environment.

Do not introduce unnecessary authentication complexity when the user's requirements are simple.

However, simplicity must not mean:

* Hard-coded passwords.
* Shared default credentials.
* Plaintext password storage.
* Unrestricted administrative access.
* Hidden authentication bypasses.
* Unprotected recovery endpoints.
* Missing authorization checks.

---

# Initial Administrator

## Generate Credentials During Initial Setup

If the application requires an initial administrator account and the user has not supplied credentials, generate a unique, cryptographically secure random password during initial setup.

Never use predictable defaults such as:

```text
admin
password
admin123
changeme
root
default
```

Do not derive the password from:

* Project name
* Hostname
* Username
* Current date
* Domain name
* Installation path
* Machine identifiers

Use a cryptographically secure random number generator.

The generated password should have sufficient entropy and should not rely solely on complexity rules.

---

## Initial Credential Delivery

When an administrator password is automatically generated, present it directly to the user during the initial setup process.

For example:

```text
Initial administrator created.

Username: admin
Password: <generated-password>

Store this password securely.
```

The actual generated password must only be shown when necessary.

Do not:

* Commit it to Git.
* Store it in documentation.
* Write it to ordinary application logs.
* Include it in analytics or telemetry.
* Expose it through an unauthenticated endpoint.
* Repeatedly display it after initialization.
* Store a plaintext copy in the database.

If setup is performed through an automated or non-interactive environment, use an appropriate secure credential delivery mechanism for that environment.

---

## No Permanent Default Password

The application must never ship with a universal administrator password.

Every installation requiring a bootstrap administrator should receive either:

1. Credentials explicitly provided by the user through an appropriate secure mechanism, or
2. A unique cryptographically generated initial password.

Never reuse generated bootstrap passwords between installations.

---

# Password Storage

## Never Store Plaintext Passwords

User passwords must never be stored in plaintext.

Passwords should normally be **hashed**, not encrypted.

Use a maintained password-hashing implementation based on an appropriate algorithm such as:

* Argon2id
* bcrypt
* scrypt

Prefer Argon2id when supported by the project's technology stack.

Parameters should be appropriate for the deployment environment and current security recommendations.

Never use general-purpose fast hashes such as these directly for password storage:

* MD5
* SHA-1
* SHA-256
* SHA-512

A fast cryptographic hash alone is not a password-hashing scheme.

---

# Credential & Secret Storage

## Sensitive Database Values

Applications may need to store sensitive values that must later be recovered in their original form.

Examples include:

* API keys
* Access tokens
* Refresh tokens
* Integration credentials
* Service credentials
* Private configuration secrets
* Third-party authentication secrets
* Private keys
* Signing material
* Other application-managed secrets

When these values must be stored in a database, they should be encrypted at rest using authenticated encryption.

Do not store recoverable secrets as plaintext database fields.

---

## Encryption

Use established, maintained cryptographic libraries.

Prefer authenticated encryption schemes supported by the selected platform, such as:

* AES-GCM
* ChaCha20-Poly1305

Do not design custom encryption algorithms or protocols.

Encrypted records should preserve the information necessary for safe decryption and key rotation, such as an appropriate key identifier/version and cryptographic metadata required by the selected implementation.

Never reuse nonces where the selected cryptographic scheme requires uniqueness.

---

# Encryption Keys

## Keep Keys Separate From Encrypted Data

The key used to encrypt database credentials must not simply be stored alongside those credentials in the same database.

Where practical, encryption keys should come from an external trusted source such as:

* Operating-system protected configuration
* A secret manager
* A key management service
* A hardware-backed key store
* A securely provided runtime secret

The exact mechanism should accommodate the user's environment and deployment requirements.

For small or self-hosted deployments, keep the solution practical while still ensuring that possession of a database backup alone does not automatically reveal every stored secret.

Follow `CREDS_DB.md` and `SECURITY.md` for additional project requirements.

---

## Key Rotation

Design encrypted credential storage so encryption keys can be rotated when necessary.

Where practical, encrypted records should identify which key/version was used so values can be migrated to newer keys.

Do not permanently couple all encrypted data to a single undocumented key.

---

# Password Changes

Authenticated users should be able to change their own passwords when user accounts are supported.

Administrative password resets should require appropriate authorization.

Password changes and administrative resets should invalidate or rotate authentication sessions where appropriate.

Never return an existing password to a user.

Because passwords are hashed, the application should not be capable of recovering the original password.

---

# Administrative Recovery

## Lockout Recovery Must Exist

Projects with application-managed administrator accounts should provide a documented recovery mechanism so legitimate operators can regain administrative access if all administrator credentials are lost.

The recovery mechanism must **not** be a hidden backdoor.

It must require trusted administrative access to the deployment environment.

---

## Administrative Password Reset

Where appropriate, provide an explicit administrative recovery command or maintenance procedure.

For example, a project might provide:

```text
application admin reset-password <username>
```

or:

```text
application admin set-password <username>
```

The exact interface depends on the project.

The recovery mechanism should require privileged local or administrative access and must not be exposed as an unauthenticated public API.

If a password is not explicitly provided, prefer securely prompting for it or generating a cryptographically secure random replacement.

Do not place passwords directly on command lines when avoidable, because command-line arguments may be visible through:

* Shell history
* Process listings
* Monitoring tools
* Administrative logs

Prefer an interactive prompt, protected input source, or other mechanism appropriate for the environment.

---

## Forced Administrative Reset

A trusted operator should have a documented way to forcefully reset an account password when normal authentication cannot be used.

This exists for legitimate recovery scenarios such as:

* Lost administrator credentials.
* Administrator lockout.
* Authentication-provider failure.
* Account recovery after configuration problems.
* Disaster recovery.

A forced reset must:

* Require trusted administrative access.
* Generate/store a new password hash correctly.
* Never expose the previous password.
* Invalidate existing sessions where appropriate.
* Create an audit event.
* Avoid bypassing unrelated authorization controls.
* Avoid creating a permanent master credential.

Do not implement universal passwords, secret bypass parameters, hidden accounts, undocumented endpoints, or hard-coded recovery keys.

---

# Recovery Documentation

The recovery procedure should be documented under project contributor/operator documentation where appropriate.

For example:

```text
contrib/
└── recovery/
    └── README.md
```

or another location appropriate to the project structure.

The documentation should explain:

* How to identify the administrator account.
* How to invoke the recovery command.
* What permissions are required.
* How to reset the password securely.
* What sessions or tokens will be invalidated.
* Where the recovery action is audited.

Do not place actual credentials in recovery documentation.

---

# User Management

## Keep It Appropriate to the Project

User management should accommodate the user's requirements.

A small internal application may only need:

* Administrator
* User

A larger application may require:

* Multiple administrators
* Operators
* Read-only users
* Service accounts
* Custom roles
* Fine-grained permissions

Do not build an unnecessarily complicated identity-management platform when the user only needs basic authentication.

At the same time, avoid architecture that makes future authorization impossible.

---

# RBAC

## Role-Based Access Control

When the application has functionality with different privilege levels, use role-based access control (RBAC) or an equivalent authorization model.

Authorization should be enforced by the trusted backend.

Do not rely on frontend visibility to enforce permissions.

Hiding a button does not prevent a user from calling the underlying API.

---

## Roles

Roles should represent meaningful sets of permissions.

Example roles may include:

```text
admin
operator
user
viewer
```

These names are examples only.

Use roles appropriate to the actual project.

Do not introduce roles merely because they appear in this document.

---

## Permissions

Where the application requires finer control, roles should map to explicit permissions.

Examples might include:

```text
users.read
users.create
users.update
users.delete

settings.read
settings.update

audit.read

credentials.read
credentials.update
```

The exact permissions depend on the project.

Prefer explicit authorization checks over assumptions based solely on UI state.

---

## Least Privilege

Users, services, and administrators should receive only the permissions required for their intended purpose.

Administrative access should not be granted by default.

New accounts should receive a safe default role appropriate to the user's requirements.

Never trust a role or permission value supplied by the client without verifying it against trusted server-side state.

---

# Sensitive Credential Access

Access to stored secrets should be tightly controlled.

A user who can edit an integration does not automatically need permission to retrieve its existing plaintext secret.

Where practical, interfaces should display sensitive values as masked:

```text
••••••••••••••••
```

or:

```text
sk_••••••••••••abcd
```

Prefer allowing users to replace a secret rather than repeatedly revealing the existing value.

If revealing a stored credential is genuinely required, enforce appropriate authorization and audit the action.

---

# Authentication Audit Logging

## Audit Important Events

Applications with user authentication should maintain audit records for security-relevant identity events.

Examples include:

* Successful login
* Failed login
* Logout
* Password change
* Password reset
* Forced administrative password reset
* User creation
* User deletion
* User enable/disable actions
* Role changes
* Permission changes
* Administrative account changes
* Credential changes
* Token creation
* Token revocation
* Relevant authentication configuration changes

The exact set should reflect the application's functionality.

---

## Audit Record Contents

Where appropriate and legally/operationally suitable, audit records may contain:

* Timestamp
* Event type
* Acting user/account identifier
* Target user/account identifier
* Result
* Relevant source information
* Request or correlation identifier
* Relevant non-sensitive metadata

Audit logs must never contain:

* Passwords
* Password hashes
* API keys
* Access tokens
* Refresh tokens
* Session secrets
* Private keys
* Encryption keys
* Authentication cookies
* Full Authorization headers

Do not accidentally turn an audit log into a credential database.

---

## Failed Authentication

Failed authentication attempts should be auditable.

Record enough information to investigate abuse without recording the attempted password or other submitted secrets.

Repeated failures may justify protections such as:

* Rate limiting
* Temporary throttling
* Progressive delays
* Account protections
* Administrative alerts

Choose controls appropriate to the user's requirements and threat model.

Avoid creating trivial denial-of-service opportunities through overly aggressive permanent account lockouts.

---

# Audit Log Protection

Audit logs should be protected against unauthorized access and modification.

Access to security audit information should require appropriate authorization.

Where practical:

* Make security events append-oriented.
* Restrict deletion.
* Restrict modification.
* Record administrative actions.
* Establish suitable retention.
* Protect logs from exposing sensitive information.

If RBAC is used, audit-log access should normally have an explicit permission such as:

```text
audit.read
```

---

# Sessions & Tokens

Authentication tokens and sessions must be generated using cryptographically secure randomness.

Tokens should:

* Have sufficient entropy.
* Have appropriate expiration.
* Be revocable where required.
* Be invalidated when relevant account security changes occur.
* Never be stored in plaintext when a non-recoverable representation is sufficient.

For web sessions, follow the cookie and session requirements in `SECURITY.md`.

---

# API Keys

If the application provides API keys:

* Generate them using a cryptographically secure random number generator.
* Give them sufficient entropy.
* Show the complete key only when necessary.
* Prefer showing newly generated keys once.
* Allow keys to be revoked.
* Allow keys to be rotated.
* Associate keys with an owner.
* Associate keys with appropriate permissions/scopes where needed.
* Record creation and revocation in the audit log.

If the original API key does not need to be recovered later, prefer storing a secure hash/verifier rather than reversible encryption.

---

# Secret Exposure

If a credential or secret is accidentally exposed:

1. Treat it as compromised.
2. Revoke or rotate it.
3. Remove the exposed value from active configuration.
4. Investigate where it was exposed.
5. Review relevant audit information.
6. Address the cause of the exposure.
7. Handle repository history appropriately if the secret entered Git history.

Simply deleting a secret from the latest Git commit does not make an exposed credential safe again.

---

# AI Agent Requirements

AI agents implementing authentication or user-management functionality must:

1. Read the user's original requirements.
2. Read `SECURITY.md`.
3. Read `CREDS_DB.md`.
4. Inspect existing authentication and authorization mechanisms.
5. Prefer existing project mechanisms over creating competing systems.
6. Never generate hard-coded universal credentials.
7. Generate bootstrap administrator passwords securely when required.
8. Present generated credentials only through an appropriate initial setup path.
9. Hash passwords using an established password-hashing algorithm.
10. Encrypt recoverable database secrets using authenticated encryption.
11. Keep encryption keys separate from encrypted database values.
12. Implement authorization server-side.
13. Support RBAC when the application's requirements need multiple privilege levels.
14. Audit important authentication and user-management events.
15. Never place credentials or secrets into logs.
16. Provide a secure administrative recovery mechanism when application-managed administrators exist.
17. Never implement hidden authentication bypasses or backdoor accounts.
18. Keep the solution proportional to the user's requirements.

---

# User Requirements Take Priority

The user may request a deliberately simple authentication model.

For example:

```text
One administrator only.
```

Do not respond by unnecessarily building a complex enterprise identity system.

Implement the simplest secure solution that satisfies the user's requirements.

However, never interpret simplicity as permission to use:

* Plaintext passwords
* Default passwords
* Hard-coded credentials
* Authentication bypasses
* Unprotected administrative endpoints
* Client-side-only authorization
* Plaintext secret storage
* Missing security auditing where authentication security requires it

Design the underlying authorization model cleanly enough that RBAC can be introduced or expanded later when reasonably practical.

---

# Final Principle

Credentials must be treated as sensitive throughout their entire lifecycle:

```text
Generation
    ↓
Delivery
    ↓
Storage
    ↓
Use
    ↓
Authorization
    ↓
Audit
    ↓
Rotation
    ↓
Revocation
    ↓
Recovery
```

The application should remain recoverable by its legitimate operator without creating hidden backdoors.

Passwords should be securely hashed.

Recoverable secrets should be encrypted when stored.

Encryption keys should be separated from encrypted data.

Administrative privileges should be explicit.

Security-sensitive actions should be auditable.

And no credential, password, key, token, or secret should ever be exposed merely for convenience.
