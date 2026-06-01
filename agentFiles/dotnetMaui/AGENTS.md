# Repository Instructions

## Project type

This repository is a .NET / MAUI project.

## Main areas

* MAUI presentation layer: UI, pages, views, view models, bindings, app startup, platform-specific UI code.
* Shared/application logic: non-UI services, models, helpers, validation, and business-adjacent behavior.
* Tests: unit/integration tests where present.

## Build and verification

Verification is handled by the global Codex automation tools.

For MAUI-related issues, use the `area:maui` profile/label.

For non-MAUI .NET issues, use the `area:backend` profile/label only if the change does not require building the MAUI project.

If a non-GUI `.slnf` solution filter exists, prefer it for non-MAUI .NET verification.

## Target selection rules

* For UI, XAML, pages, views, view models, bindings, navigation, or platform presentation behavior, treat the issue as `area:maui`.
* For non-UI logic, services, validation, models, or tests, treat the issue as `area:backend`.
* Do not touch MAUI UI files for backend-only issues unless explicitly required.
* Do not touch backend/domain/application logic for UI-only issues unless explicitly required.

## Repository-specific constraints

* Keep changes small and localized.
* Prefer editing existing files over creating new abstractions.
* Do not introduce new frameworks unless explicitly requested.
* Do not change persistence, models, migrations, scoring, task state logic, or public APIs unless the issue explicitly requires it.
* Do not perform broad formatting changes.
* Do not perform unrelated cleanup.

## MAUI-specific rules

* Preserve existing binding patterns.
* Be careful with XAML names, binding contexts, routes, and platform-specific files.
* Do not rename views, view models, routes, bindings, commands, or properties unless the issue explicitly requires it.
* If a change affects UI behavior, keep it limited to the relevant page/component/view model.
