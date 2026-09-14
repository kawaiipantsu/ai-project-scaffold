# Technology

This document describes the technologies and development tools generally available and preferred for projects using this scaffold.

These are **defaults and available options, not mandatory technology choices**.

The user's initial prompt and project-specific requirements always take priority.

If the user specifies a language, framework, database, web server, architecture, version, or other technology, follow the user's requirements instead.

---

# General Principles

AI agents have discretion to select the technologies best suited to the project.

Prefer:

* Simple solutions
* Mature technologies
* Actively maintained software
* Stable releases
* Minimal unnecessary dependencies
* Technologies appropriate to the workload
* Existing project technologies over introducing competing stacks

Do not use every available technology simply because it is listed here.

Use only what provides value to the project.

---

# Software Versions

Always prefer the **latest stable and supported versions** of software, frameworks, libraries, dependencies, and development tools available for the target environment.

Version numbers in this file represent minimums, families, or examples and should not unnecessarily pin a project to an old release.

Before starting a new project, determine the currently appropriate stable version when version choice matters.

Avoid:

* End-of-life releases
* Unsupported dependencies
* Deprecated APIs
* Obsolete frameworks

unless required by the user or compatibility requirements.

---

# Preferred Web Stack

For traditional web applications, the preferred basic stack is:

```text id="5d7pxa"
Apache 2.4+
    ↓
.htaccess / Apache configuration
    ↓
PHP 8+
    ↓
Application / API
    ↓
Database / Redis / Services

HTML5
CSS3
JavaScript
    ↓
Browser
```

This stack is preferred when it provides a simple and appropriate solution.

It is not mandatory.

---

## Backend

For conventional web applications, prefer:

* Apache 2.4+
* PHP 8+
* `.htaccess` where appropriate

PHP may be used for:

* Application backends
* REST/API endpoints
* Authentication
* Database access
* Server-rendered pages
* Administrative interfaces
* Background scripts
* CLI tooling

Prefer clean API endpoints when frontend/backend separation provides value.

Do not force PHP into workloads better suited to another available technology.

---

## Frontend

The basic preferred frontend stack is:

* HTML5
* CSS3
* JavaScript

Prefer native browser capabilities when they provide a simple solution.

Frameworks and libraries may be introduced when they provide meaningful value.

Do not automatically introduce a large frontend framework for a project that can be implemented cleanly with HTML, CSS, and JavaScript.

---

## Canvas & WebGL

Browser graphics may use:

* Canvas
* WebGL

Use them when appropriate for:

* Visualization
* Interactive graphics
* Rendering
* Games
* Image manipulation
* High-performance browser graphics
* Custom interfaces

Do not introduce Canvas or WebGL when ordinary HTML/CSS provides a simpler solution.

---

# Node.js

Node.js is available and may be preferred for workloads such as:

* WebSocket servers
* Real-time communication
* APIs
* Event-driven services
* Streaming
* Background workers
* Development/build tooling

Node.js may run alongside an Apache/PHP application when that architecture makes sense.

For example:

```text id="31exua"
Browser
   ↓
Apache / PHP API
   ↓
Application

Browser
   ↓
WebSocket
   ↓
Node.js
```

Choose PHP, Node.js, or another backend based on the actual requirements.

---

# Available Technologies

The development environment may provide or support the following technologies.

## Web

```text id="b4w39i"
Apache 2.4+
.htaccess
PHP 8+
PHP-CLI
HTML5
CSS3
JavaScript
Canvas
WebGL
Node.js
```

## Systems & Compiled Development

```text id="3x20q8"
Rust
Go / Golang
C
C++
Make
Makefile
```

These are suitable for:

* Services
* Daemons
* CLI applications
* Performance-sensitive components
* Networking software
* Workers
* Native utilities
* System integrations

---

## Python

Available:

```text id="u86yy1"
Python 3
Python 2
```

Prefer **Python 3** for all new development.

Python 2 should only be used for legacy compatibility when explicitly required.

Python may be useful for:

* Automation
* Scripts
* Data processing
* Machine learning
* Computer vision
* Maintenance tools
* Build utilities
* Background processing

---

## GPU / Accelerators

Available technologies may include:

```text id="mgwd6p"
CUDA
Coral TPU
OpenCV
```

Use these when projects require:

* GPU computation
* Machine learning inference
* Computer vision
* Image/video processing
* Hardware acceleration
* Edge inference

Do not assume accelerator hardware exists on every deployment target.

Applications should handle hardware availability appropriately when portability is required.

---

# Databases

Available database technologies include:

```text id="4quqbp"
MySQL
MariaDB
Qdrant
```

## MySQL / MariaDB

Prefer MySQL/MariaDB for traditional relational data when appropriate.

Use proper:

* Schemas
* Migrations
* Indexes
* Transactions
* Parameterized queries
* Connection management

Database files and migrations should follow `STRUCTURE.md`.

Credentials must follow `CREDS_DB.md` and `SECURITY.md`.

---

## Qdrant

Qdrant is available when vector storage/search is required.

Suitable uses include:

* Embeddings
* Semantic search
* Similarity search
* Retrieval systems
* AI/RAG applications

Do not introduce a vector database unless the project actually requires vector search.

---

# Redis

Redis is available and preferred where shared fast state provides value.

Possible uses include:

* Shared sessions
* Caching
* Rate limiting
* Short-lived state
* Coordination
* Distributed counters

Redis is particularly useful when applications must scale across multiple backend instances.

Follow the architecture guidance in `ARCHITECTURE.md`.

---

# Queues

Beanstalkd is available for lightweight queue-based background processing.

Suitable uses include:

* Background jobs
* Worker queues
* Deferred processing
* Batch operations
* Asynchronous tasks
* Work distribution

Other queue technologies may be selected when project requirements justify them.

Do not introduce queue infrastructure when synchronous processing is sufficient.

---

# AI & Automation

Available AI/automation systems may include:

```text id="f0w3p7"
n8n
Ollama API
LM Studio API
ACE-Step 1.5 API
```

These may be used where appropriate for:

* Local AI inference
* LLM integration
* Automation workflows
* AI-assisted processing
* Audio/music generation
* Agent workflows
* Model-backed services

Do not assume a particular model or endpoint is configured without inspecting the target environment or user requirements.

---

# Scripts & CLI Tools

Shell scripts, PHP-CLI, Python, Node.js, Go, Rust, or other suitable tools may be used for automation and maintenance tasks.

Choose the simplest appropriate implementation.

For example, do not create a compiled service when a small shell script or cron task safely solves the problem.

Likewise, do not build a large shell script when a structured application would be significantly safer and easier to maintain.

---

# Background Services

Depending on the project, background processing may use:

* cron / `cron.d`
* systemd services
* PHP-CLI workers
* Node.js workers
* Python workers
* Go services
* Rust services
* Beanstalkd queues
* Redis-backed processing

Follow `ARCHITECTURE.md` when choosing between scheduled scripts, workers, queues, and persistent services.

---

# Debian Build Environment

A Debian build environment is available.

Projects may use:

* Makefiles
* Debian packaging
* `.deb` packages
* Standard Debian build tooling
* Service definitions
* Package installation scripts

Where appropriate, projects should be capable of producing reproducible build or installation artifacts.

Generated packages and build artifacts should follow `.gitignore` and `STRUCTURE.md`.

---

# Additional Software

AI agents may install additional:

* Software
* Packages
* Compilers
* Development tools
* Frameworks
* Libraries
* Build dependencies

when they are reasonably required to complete the project.

Before adding something new:

1. Check whether an existing available tool already solves the problem.
2. Prefer maintained and reputable software.
3. Prefer stable releases.
4. Avoid unnecessary dependencies.
5. Consider security and licensing.
6. Document important permanent dependencies.

Project dependencies should be reflected in the appropriate package/build files and documentation.

---

# System Access

The development environment may provide passwordless `sudo` access.

This may be used when necessary to:

* Install required development packages.
* Configure required local services.
* Prepare the build environment.
* Install system dependencies.
* Perform project-required setup.

Do not use elevated privileges unnecessarily.

Do not make unrelated system changes.

Do not disable security controls merely to make development easier.

Do not assume the final production environment will provide passwordless `sudo` or equivalent privileges.

---

# Technology Selection

AI agents have discretion to select appropriate technologies when the user has not specified them.

A useful decision order is:

```text id="qpsg9m"
User Requirements
       ↓
Existing Project Technology
       ↓
Simplest Appropriate Solution
       ↓
Preferred Technologies in this File
       ↓
Additional Technology if Required
```

Do not rewrite an existing project into the preferred stack merely because this file lists it.

---

# User Requirements Override This File

The user's initial prompt and subsequent explicit requirements always take priority.

For example, if this file prefers:

```text id="93tjvv"
Apache + PHP + MariaDB
```

but the user requests:

```text id="5f7dpw"
Go + PostgreSQL
```

use Go and PostgreSQL.

Similarly, if the user requests a specific framework or technology version, accommodate that requirement unless doing so is impossible or creates a serious issue that should first be brought to the user's attention.

---

# AI Agent Rules

AI agents should:

1. Read the user's initial prompt first.
2. Inspect the existing project technology before introducing new technology.
3. Prefer current stable software versions.
4. Prefer simple solutions.
5. Use the technologies in this file when they are appropriate.
6. Install additional dependencies when genuinely needed.
7. Avoid unnecessary frameworks and services.
8. Document significant technology decisions.
9. Follow `ARCHITECTURE.md` for architectural decisions.
10. Follow `SECURITY.md` for security requirements.
11. Follow `STRUCTURE.md` for repository organization.
12. Never assume the development environment exactly matches production.

---

# Final Principle

Use the right tool for the job.

The technologies listed here describe the preferred and available toolbox, not a mandatory stack.

Start with the user's requirements, choose the simplest appropriate solution, use modern stable versions, and introduce additional technology only when it provides a clear benefit.
