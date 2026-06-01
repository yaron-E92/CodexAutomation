---
name: issue-to-pr-automation
description: Use this skill when the user wants Codex to take a GitHub issue or literal issue description through planning, implementation, PR creation, CI repair, verification, and ready-to-merge notification.
---

# Issue-to-PR Automation

This skill turns one GitHub issue or one literal issue description into a pull request.

## Hard rules

- Never merge to main automatically.
- Process only one issue per run unless explicitly told otherwise.
- Keep changes small, surgical, and issue-scoped.
- Do not perform unrelated refactors.
- Planning and verification must be read-only.
- Implementation and repair may edit the workspace.
- CI repair loops must be bounded.
- If the workflow fails after the configured attempts, stop and report clearly.
- If the PR passes CI and verification, report that it is ready to merge.

## Preferred implementation

Prefer the user-level scripts in:

~~~powershell
$env:USERPROFILE\codex-tools
~~~

Main queue command:

~~~powershell
pwsh -File "$env:USERPROFILE\codex-tools\codex-process-next-ready-issue.ps1" -Username "OWNER" -Repo "REPO" -Base main -LocalCheck "dotnet test"
~~~

Direct issue command:

~~~powershell
pwsh -File "$env:USERPROFILE\codex-tools\codex-issue-to-pr.ps1" -Issue 123 -Username "OWNER" -Repo "REPO" -Base main -LocalCheck "dotnet test"
~~~

For non-.NET repositories, replace `dotnet test` with the repository's documented verification command.

## Workflow

1. Identify the target:
   - A GitHub issue number, or
   - A literal issue description, or
   - The oldest issue labeled `codex:ready`.

2. Planning phase:
   - Read global and repository AGENTS.md files.
   - Inspect relevant files.
   - Do not edit files.
   - Produce a short implementation plan.

3. Implementation phase:
   - Create a branch.
   - Make minimal code changes.
   - Add or update tests when behavior changes.
   - Run the local verification command.

4. Local repair phase:
   - If local checks fail, fix only the failure.
   - Re-run local checks.
   - Stop after the configured maximum repair attempts.

5. PR phase:
   - Commit.
   - Push.
   - Create a pull request.

6. CI phase:
   - Watch required GitHub checks.
   - If CI fails, inspect failure information.
   - Fix minimally.
   - Commit, push, and watch CI again.

7. Verification phase:
   - Review final diff against issue and plan.
   - Do not edit files during verification.
   - Return PASS or FAIL.
   - If FAIL, fix only verifier gaps.

8. Completion:
   - If CI passes and verifier passes, report:
     - PR URL
     - Verification command used
     - "Ready to merge"