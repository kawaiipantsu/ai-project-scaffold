# README Generation Instructions

> **AI AGENT:** This file is a template/instruction file. Replace its contents with a polished, project-specific `README.md` based on the actual project.

Create a visually appealing, useful, and easy-to-read README for this project.

The README should focus primarily on:

* **Features**
* **Installation**
* **Usage**
* **About**

Always follow the user's original prompt, requirements, and preferences first.

If the user provides specific instructions for the README, those instructions take priority over the recommendations in this file.

---

## README Style

The finished README should feel like a polished open-source project page rather than automatically generated documentation.

Use:

* Clear headings
* Short explanations
* Good visual hierarchy
* Tables where they improve readability
* Code blocks for commands and examples
* Screenshots
* A graphical project banner
* Badges when useful
* Icons or emoji sparingly when they improve navigation
* Links to relevant project documentation

Avoid unnecessary walls of text.

The README should quickly communicate:

1. What the project is.
2. Why someone would use it.
3. What it looks like.
4. What its important features are.
5. How to install it.
6. How to use it.

---

# Graphical Banner

The README should **always have a graphical banner at the top**.

Prefer a project-specific banner that visually represents the project or tool.

For example:

```markdown
<p align="center">
  <img src=".github/images/banner.png" alt="Project Name" />
</p>
```

The banner should be stored locally in the repository.

Do not hotlink externally hosted banner images.

If a new banner or other external graphical asset is required, follow:

`docs/ASSETS.md`

Any sourced asset must be properly licensed, downloaded, stored, and tracked according to the project's asset rules.

---

# Project Introduction

Immediately after the banner, clearly identify the project.

A typical structure may include:

```markdown
# Project Name

Short, memorable description of what the project does.

Optional badges.

A slightly longer explanation of the project's purpose and primary use case.
```

The introduction should be concise.

A reader should understand the project's purpose within a few seconds.

Do not invent capabilities that the project does not have.

---

# Features

Include a prominent **Features** section.

Highlight the project's most important capabilities.

Prefer concise explanations over simply listing technical components.

For example:

```markdown
## ✨ Features

| | |
|---|---|
| 🚀 **Feature** | Short explanation of why this feature is useful. |
| 🔒 **Feature** | Short explanation of another important capability. |
| ⚡ **Feature** | Short explanation of another important capability. |
```

The exact presentation is flexible.

Use bullets, tables, subsections, or another format when it better fits the project.

Focus on features that matter to users.

---

# Screenshots

The README should include **real screenshots of the project or tool whenever the project has something meaningful to show**.

Examples include:

* Web interfaces
* Desktop interfaces
* Terminal output
* CLI usage
* Dashboards
* Reports
* Visualizations
* Configuration interfaces
* Important workflows

Prefer multiple useful screenshots over a single decorative image when they help explain the project.

Store README-specific images under:

`.github/images/`

For example:

```markdown
## 🖥️ Screenshots

### Dashboard

<p align="center">
  <img src=".github/images/dashboard.png" alt="Project dashboard" />
</p>

### CLI

<p align="center">
  <img src=".github/images/cli.png" alt="Project CLI" />
</p>
```

Screenshots must represent the actual project.

Do not fabricate screenshots that falsely represent functionality that does not exist.

---

# Installation

Include a clear **Installation** section.

Installation instructions should match the actual project and supported environments.

Where applicable, document:

* Prerequisites
* Packages
* Binary installation
* Source builds
* Debian/Ubuntu packages
* Docker/container installation
* Platform-specific requirements
* Required permissions
* Initial configuration

Prefer copy/paste-friendly commands.

For example:

```markdown
## 📦 Installation

### From source

\`\`\`bash
git clone <repository>
cd <project>
make build
\`\`\`
```

Only include installation methods that actually exist.

Do not invent package managers, releases, containers, scripts, or installation methods.

---

# Usage

Include a practical **Usage** section.

Show users how to get started after installation.

Prefer real commands and examples.

For example:

```markdown
## 🚀 Usage

Start the application:

\`\`\`bash
./project
\`\`\`

Run a command:

\`\`\`bash
project command --option value
\`\`\`
```

Include additional examples when they help demonstrate important functionality.

Keep the first example simple enough for a new user to follow.

---

# About

Include an **About** section describing the project in slightly more detail.

It may explain:

* Why the project exists
* What problem it solves
* Who it is intended for
* Important design goals
* Project philosophy
* Current development status

Keep detailed technical architecture in `docs/ARCHITECTURE.md` rather than duplicating it in the README.

---

# Additional Sections

Additional sections may be included when they are genuinely useful.

Examples include:

* Requirements
* Quick Start
* Configuration
* Architecture
* Development
* API
* Examples
* Roadmap
* Security
* Contributing
* Documentation
* License
* Acknowledgements

Do not add sections merely to make the README longer.

The README should prioritize useful information over completeness for its own sake.

---

# Reference Layout

For inspiration on presentation, visual hierarchy, screenshots, feature presentation, installation instructions, and usage examples, refer to:

`https://github.com/kawaiipantsu/synapseids`

Use it as **layout inspiration only**.

Do not blindly copy its text or project-specific content.

Adapt the structure to the current project.

The current project's:

* Purpose
* Features
* Technology
* Installation process
* Screenshots
* Commands
* Architecture
* Development status

must always reflect the actual repository.

---

# Project Documentation

Before generating or significantly rewriting the README, review the relevant files under `docs/`, especially:

* `docs/PROJECT.md`
* `docs/PROJECT_RULES.md`
* `docs/ARCHITECTURE.md`
* `docs/STRUCTURE.md`
* `docs/TECHNOLOGY.md`
* `docs/SECURITY.md`
* `docs/ASSETS.md`

Use these documents to understand the project instead of guessing.

Inspect the actual source code and repository structure when necessary.

---

# Asset Rules

All images and graphical assets used by the README must follow `docs/ASSETS.md`.

For README-specific graphics, prefer:

`.github/images/`

Externally sourced assets must first be downloaded and tracked according to `docs/ASSETS.md` before being copied to their final location.

Never assume that an image found on the internet is free to use.

Never hotlink external images when the asset can reasonably be stored in the repository.

---

# Accuracy

The finished README must describe the **actual state of the project**.

Never claim that something exists when it has not been implemented.

Do not invent:

* Features
* Screenshots
* Installation methods
* Packages
* Releases
* APIs
* Commands
* Supported platforms
* Performance numbers
* Security guarantees
* Compatibility claims

If functionality is planned but not implemented, clearly identify it as planned or omit it.

---

# User Instructions Take Priority

**The user's instructions always take priority over the preferred README structure described here.**

If the user requests:

* A different layout
* Specific sections
* No screenshots
* No banner
* Different wording
* A minimal README
* A highly technical README
* A particular visual style
* Specific installation instructions
* Specific ordering

follow the user's request.

This file provides the **default README strategy**, not permission to override the user.

---

# Final Goal

The finished `README.md` should make someone visiting the repository immediately understand:

**What is this?**

**What can it do?**

**What does it look like?**

**How do I install it?**

**How do I use it?**

It should be visually polished, technically accurate, and tailored to the actual project.
