# Architecture Guidelines

This document defines the default architectural principles for this project.

It is intended to be broadly reusable across different applications and services.

The exact implementation should always follow the user's requirements, the project's technology choices, and the actual deployment environment.

Prefer simple architecture first, while keeping reasonable paths available for scaling later.

---

# General Principles

The architecture should aim to be:

* Simple to understand.
* Easy to operate.
* Easy to scale when needed.
* Secure by default.
* Modular enough to replace or expand individual components.
* Observable and debuggable.
* Resistant to unnecessary coupling.
* Appropriate for the user's actual workload.

Do not build unnecessary distributed systems for small workloads.

Do not block future scaling by tightly coupling everything together either.

Prefer the simplest architecture that leaves room to grow.

---

# Application Boundaries

Keep core backend logic separate from ingress and egress concerns.

Where practical, separate:

* Request handling
* Business logic
* Data access
* Authentication
* Background processing
* External integrations
* Infrastructure concerns

Ingress components should primarily be responsible for receiving requests, validating them, applying appropriate security controls, and passing them into the application.

Egress components should handle communication with external systems in a controlled and explicit manner.

Core backend logic should not depend directly on web-facing transport details unless the application is intentionally very small.

---

# API-First Backend Access

When the project has a backend and separate clients, prefer exposing backend functionality through defined API endpoints.

Examples of clients may include:

* Web interfaces
* Mobile applications
* CLI tools
* Administrative interfaces
* External integrations
* Internal services

Avoid direct database access from frontend or untrusted client components.

Prefer:

```text
Client
   ↓
API
   ↓
Authorization
   ↓
Business Logic
   ↓
Data Layer
   ↓
Database
```

The API does not need to be publicly exposed if it is only used internally.

Use an interface appropriate to the application, such as:

* HTTP/HTTPS
* REST
* RPC
* gRPC
* Unix sockets
* Internal message queues

Do not introduce network APIs where a local function call is sufficient.

---

# Ingress & Egress

Ingress and egress should be explicit.

Typical ingress components may include:

* Reverse proxies
* Load balancers
* API gateways
* Web servers
* CLI entry points
* Message consumers

Typical egress may include:

* Third-party APIs
* SMTP
* Webhooks
* External databases
* Object storage
* Queue systems
* Other services

Do not let arbitrary application components make uncontrolled outbound requests.

Where practical, centralize or clearly structure external integrations.

---

# Internal Network Communication

Internal communication should be optimized for the deployment environment.

For communication that remains entirely within a trusted local host or tightly controlled private network, additional encryption may not always be necessary.

Examples may include:

* Unix sockets
* Loopback communication
* Local Redis connections
* Local database connections
* Private service networks

Do not add unnecessary encryption layers solely for appearance when they provide no meaningful security benefit and create operational or performance cost.

However:

* Never assume a network is trusted without understanding the deployment.
* Protect sensitive cross-host communication when appropriate.
* Use TLS or mTLS where the threat model requires it.
* Follow `SECURITY.md` for transport-security requirements.

Always respect the user's infrastructure and deployment requirements.

---

# Scalability

Design for reasonable scalability without prematurely distributing the system.

Prefer stateless application processes where practical.

State that must survive process restarts or support multiple application instances should normally be moved into shared systems such as:

* Databases
* Redis
* Object storage
* Queues

This allows multiple application instances to operate behind a load balancer when needed.

---

# Sessions

For applications requiring server-side sessions, prefer Redis or another appropriate shared session store when horizontal scaling is expected.

Redis is useful for:

* Session storage
* Short-lived state
* Rate-limiting counters
* Distributed locks where carefully designed
* Caching
* Lightweight coordination

Do not store important permanent application data only in Redis unless the design explicitly requires it and persistence is properly configured.

For very small single-instance applications, simpler session mechanisms may be acceptable.

Do not introduce Redis when it provides no actual benefit.

---

# Queues & Asynchronous Work

Use queues when work should be processed outside the normal request lifecycle.

Queues are appropriate for tasks such as:

* Email delivery
* Report generation
* Imports
* Exports
* Image or media processing
* Notifications
* Long-running jobs
* Data synchronization
* External API processing
* Batch work
* Retryable operations

A common pattern is:

```text
Application
    ↓
Queue
    ↓
Worker
    ↓
Database / External Service
```

Queues make it easier to:

* Offload expensive work.
* Process jobs concurrently.
* Scale worker capacity independently.
* Retry failed work.
* Schedule deferred processing.
* Protect frontend/API latency.

Do not use a queue for work that is fast, synchronous, and simpler to perform directly.

---

# Workers

Background workers should be independently scalable when workload requires it.

Workers should:

* Handle failures gracefully.
* Log failures.
* Avoid losing jobs silently.
* Support retry where appropriate.
* Avoid processing the same job incorrectly multiple times.
* Be safe against duplicate delivery where practical.

Prefer idempotent job handlers for operations that may be retried.

Do not assume a queue guarantees exactly-once processing unless the selected technology actually provides that guarantee.

---

# Scheduled & Background Processing

Choose the simplest appropriate background-processing mechanism.

## cron.d

For small deployments and simple recurring tasks, operating-system cron jobs may be sufficient.

Examples:

```text
/etc/cron.d/project
```

Cron is appropriate for:

* Cleanup tasks
* Regular synchronization
* Periodic reports
* Maintenance
* Database housekeeping
* Simple scheduled jobs

Keep cron jobs observable and ensure failures are logged.

---

## System Services

For long-running or more important background processes, use system services.

Examples may include:

* systemd services
* worker daemons
* queue consumers
* schedulers
* long-running import/export processors

Use services when:

* A process should always be running.
* Automatic restart is required.
* Health/status monitoring is useful.
* Workload needs to scale independently.
* Queue consumption is continuous.

---

## Larger Scale Scheduling

When workload or deployment complexity grows, consider dedicated scheduling or queue systems.

Examples may include:

* Redis-backed job systems
* RabbitMQ
* NATS
* Kafka
* Cloud queue services
* Container orchestration scheduled jobs

Only introduce these systems when project requirements justify their operational complexity.

---

# Database

The database should remain behind the application layer.

Do not expose databases directly to untrusted clients.

Database access should normally flow through controlled application code.

Use:

* Parameterized queries
* Transactions where needed
* Connection pooling
* Migrations
* Appropriate indexes
* Clear ownership of schema changes

Database migrations and schema files should be stored under:

```text
database/
├── migrations/
└── schemas/
```

Follow `CREDS_DB.md` for credential handling.

---

# Caching

Use caching when it provides measurable value.

Possible cache layers include:

* In-process caches
* Redis
* Reverse-proxy caches
* CDN caches

Do not cache sensitive data carelessly.

Always define:

* Cache lifetime
* Invalidation strategy
* Ownership
* Whether stale data is acceptable

Do not introduce caching simply because Redis is already available.

---

# Error Handling

Always implement error handling.

Applications should:

* Handle expected failures explicitly.
* Avoid silent failures.
* Return useful but safe errors.
* Log enough information for diagnosis.
* Avoid leaking secrets or internal implementation details.
* Distinguish retryable from permanent failures where useful.
* Fail safely.

Do not ignore returned errors.

Do not use empty catch blocks unless there is an explicitly documented reason.

User-facing errors should be understandable.

Internal logs may contain more diagnostic information, but must still follow `SECURITY.md`.

---

# Timeouts & Retries

External requests and long-running operations should have reasonable timeouts.

Do not allow network calls to wait indefinitely.

Retries should only be used where appropriate.

Use bounded retries and preferably backoff for transient failures.

Be careful when retrying operations that may not be idempotent.

---

# Logging

Use structured and useful logging where appropriate.

Logs should help answer:

* What happened?
* When did it happen?
* Which component failed?
* Which request/job was involved?
* Was the operation successful?

Never log credentials, passwords, tokens, private keys, or other secrets.

See `SECURITY.md`.

---

# Health Checks

Services that run continuously should expose or implement basic health checks where appropriate.

Typical checks may include:

* Process is alive.
* Database is reachable.
* Redis is reachable.
* Queue system is reachable.
* Critical dependencies are healthy.

Avoid making health checks unnecessarily expensive.

Separate liveness and readiness concepts where the deployment platform benefits from them.

---

# Graceful Shutdown

Long-running services should shut down cleanly.

Where applicable:

* Stop accepting new work.
* Finish or safely release active work.
* Close database connections.
* Close queue connections.
* Flush important logs.
* Respect termination signals.

This is especially important for containerized or orchestrated deployments.

---

# CI/CD

Use basic CI/CD where it provides value.

A reasonable baseline may include:

* Build verification
* Tests
* Linting
* Formatting checks
* Static analysis
* Security scanning

CI should catch common mistakes before changes reach `main`.

Do not create overly complicated pipelines for small projects.

Follow `GIT_RULES.md` for repository and GitHub workflow requirements.

---

# Deployment

Deployment architecture should match project scale.

Small deployments may use:

```text
Reverse Proxy
     ↓
Application
     ↓
Database
```

Larger deployments may evolve toward:

```text
Load Balancer
      ↓
Application Instances
      ↓
Redis / Queue
      ↓
Workers
      ↓
Database
```

Do not introduce distributed infrastructure unless workload or reliability requirements justify it.

---

# Reverse Proxy / Edge

Where appropriate, place internet-facing applications behind a reverse proxy, ingress controller, load balancer, or similar edge component.

It may handle:

* TLS termination
* HTTP routing
* Request limits
* Compression
* Static content
* Security headers
* Access logging
* Basic rate limiting

The backend application should not assume it is directly exposed to the internet when the intended architecture uses an upstream ingress layer.

---

# Security Boundaries

Keep internet-facing components separate from sensitive internal services where practical.

Avoid exposing:

* Databases
* Redis
* Queue systems
* Internal admin services
* Worker control interfaces
* Internal metrics
* Debug endpoints

to untrusted networks.

Use network-level controls in addition to application-level authentication where appropriate.

Follow `SECURITY.md`.

---

# Configuration

Configuration should be externalized from application logic.

Use mechanisms appropriate to the environment, such as:

* Configuration files
* Environment variables
* Command-line options
* Secret managers

Do not hard-code environment-specific values into source code.

Sensitive configuration must follow the credential and security policies.

---

# Observability

For larger or operationally important systems, consider:

* Metrics
* Health checks
* Audit logs
* Structured logging
* Tracing

Do not add heavy observability infrastructure unless the project needs it.

Start simple and expand when operational requirements justify it.

---

# Architecture Evolution

The architecture should be allowed to grow with the project.

Prefer a progression such as:

```text
Simple Application
       ↓
Shared Database
       ↓
Redis / Shared Sessions
       ↓
Background Queue
       ↓
Separate Workers
       ↓
Multiple Application Instances
       ↓
Dedicated Services
```

Do not start at the bottom of this list unless requirements demand it.

---

# AI Agent Rules

AI agents should:

1. Read the user's original requirements.
2. Prefer the simplest architecture that satisfies them.
3. Keep core backend logic separate from ingress/egress concerns where practical.
4. Prefer APIs for backend access when multiple clients or services need access.
5. Keep databases and internal services away from direct public exposure.
6. Use Redis for shared sessions when horizontal scaling requires it.
7. Use queues for long-running, retryable, asynchronous, or independently scalable work.
8. Use cron for simple scheduled jobs.
9. Use system services or workers for continuous background processing.
10. Add infrastructure only when it solves a real requirement.
11. Always implement proper error handling.
12. Use timeouts for external communication.
13. Avoid silent failures.
14. Add reasonable CI validation when appropriate.
15. Follow `SECURITY.md`, `TECHNOLOGY.md`, and `STRUCTURE.md`.
16. Do not over-engineer small projects.

---

# Final Principle

Start simple.

Keep clear boundaries.

Expose backend functionality through controlled interfaces.

Keep databases and sensitive services internal.

Use shared state such as Redis only when needed.

Use queues when work benefits from asynchronous or independent scaling.

Use cron or system services according to operational needs.

Add CI, error handling, logging, and security from the beginning.

Scale the architecture when actual requirements justify it, not simply because the technology exists.
