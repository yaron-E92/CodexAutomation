# Repository Instructions

## Project type

This repository contains multiple application areas:

* .NET backend / application logic
* React + TypeScript + Vite web presentation layer
* .NET MAUI presentation layer
* Tests and shared tooling

## Area labels / Codex profiles

Use one or more area labels to select the target area:

* `area:backend`: .NET backend, application logic, domain-adjacent logic, services, APIs, persistence, tests.
* `area:web`: React + TypeScript + Vite web UI.
* `area:maui`: .NET MAUI UI/client.

Labels are flags and may be combined.

Examples:

* Backend-only issue: `area:backend`
* Web-only issue: `area:web`
* MAUI-only issue: `area:maui`
* Backend + web issue: `area:backend` and `area:web`
* Backend + MAUI issue: `area:backend` and `area:maui`

Do not use a separate `area:fullstack` label. Full-stack means a combination of area labels.

## Build and verification

Verification is handled by the global Codex automation tools.

The global verifier chooses what to run based on the selected profiles.

Important MAUI rule:

* Backend/.NET verification must avoid accidentally building MAUI projects.
* If a non-GUI `.slnf` solution filter exists, it should be preferred for backend verification.
* MAUI verification should target MAUI `.csproj` files directly.

## Target selection rules

Codex should determine the affected area from the issue title, body, labels, changed files, and this file.

* Backend-only issues must not modify Web or MAUI code unless explicitly required.
* Web-only issues must not modify Backend or MAUI code unless explicitly required.
* MAUI-only issues must not modify Backend or Web code unless explicitly required.
* Cross-area issues must touch only the minimum necessary layers.
* If the issue is ambiguous, prefer the smallest safe scope and call out the assumption.

## Backend rules

* Preserve existing architecture and layering.
* Do not move business logic into presentation layers.
* Do not change persistence, migrations, public API contracts, schemas, scoring, or task state logic unless explicitly required.
* Add or update tests when backend behavior changes.
* Prefer existing services, patterns, and abstractions over new ones.

## Web rules

* Preserve existing component structure and UI patterns.
* Prefer small component-level changes.
* Do not introduce new state-management libraries or UI frameworks unless explicitly requested.
* Do not change backend contracts from the web layer unless the issue explicitly requires a cross-layer change.
* Avoid broad formatting changes.

## MAUI rules

* Preserve existing XAML, binding, navigation, and view-model patterns.
* Do not rename views, view models, routes, bindings, commands, or properties unless explicitly required.
* Prefer localized page/view-model changes.
* Be careful with platform-specific behavior.

## General constraints

* Keep changes small, surgical, and issue-scoped.
* Prefer editing existing files over creating new abstractions.
* Do not perform unrelated refactors.
* Do not create TODO-only implementations or empty stubs.
* Do not perform opportunistic cleanup.
* If a larger refactor seems necessary, stop and explain why before proceeding.
