# Global Codex Instructions

These instructions apply across all repositories unless a repository-level AGENTS.md overrides them.

## General working rules

- Keep changes small, surgical, and issue-scoped.
- Do not perform unrelated refactors.
- Do not change public APIs, database schemas, contracts, or user-visible behavior unless the task explicitly requires it.
- Prefer boring, readable, maintainable code over clever code.
- Preserve existing architecture, naming conventions, formatting style, and dependency choices.
- Do not invent requirements.
- If something is unclear, state the assumption or ask.
- Never merge to main automatically.
- Treat CI and tests as gates, not decorations.

## Planning rules

When asked to plan:

- Do not edit files.
- Inspect relevant code before producing a plan.
- Produce a concrete, implementation-ready plan.
- Include:
  1. Summary of requested change
  2. Relevant files or areas to inspect/change
  3. Acceptance criteria
  4. Risks and edge cases
  5. Verification commands, if known
  6. A short implementation sequence

## Implementation rules

When asked to implement:

- Follow the approved plan when one exists.
- Make the smallest useful change.
- Add or update tests when behavior changes.
- Keep commits reviewable.
- Do not perform opportunistic cleanup.
- Do not rewrite large areas unless the task explicitly requires it.
- Prefer repository-specific instructions over assumptions.

## Debugging rules

When fixing failures:

- Fix only the cause of the failure.
- Do not widen scope.
- Prefer understanding the failure over guessing.
- If multiple fixes are possible, choose the least invasive one.
- Re-run the relevant failing check when possible.

## Verification rules

When asked to verify:

- Do not edit files unless explicitly asked to fix gaps.
- Compare implementation against issue, plan, and acceptance criteria.
- Return PASS or FAIL.
- If FAIL, list concrete gaps and the minimal required fix.

## Git and PR rules

- Use descriptive branch names.
- Do not force-push unless explicitly asked.
- Do not squash, rebase, or rewrite history unless explicitly asked.
- PR descriptions should include what changed, why, how it was verified, and known risks.
- Never mark work as ready if tests or CI are failing.

## Automation rules

For issue-to-PR automation:

- Process only one issue per run unless explicitly asked otherwise.
- Planning and verification should be read-only.
- Implementation and repair may write to the workspace.
- CI repair loops should be bounded.
- If the task fails after the configured number of attempts, stop and report clearly.
