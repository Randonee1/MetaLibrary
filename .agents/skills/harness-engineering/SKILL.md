---
name: harness-engineering
description: Design and improve agent-first engineering harnesses for Codex or other coding agents. Use when the user asks how to make agents more effective in a repository, create or revise AGENTS.md and repo-local documentation, add agent-legible tooling, design feedback loops for testing/review/observability, enforce architecture with mechanical checks, improve autonomous PR workflows, or reduce drift in agent-generated codebases.
---

# Harness Engineering

## Overview

Harness engineering means designing the repository, tools, documents, checks, and feedback loops that let coding agents do reliable work with limited human attention. Treat humans as intent-setters and reviewers of judgment; make the repository itself the agent's source of truth.

This skill distills practices from OpenAI's "Harness engineering: leveraging Codex in an agent-first world" article, published February 11, 2026.

For broader article context, section-by-section notes, examples, and checklists, read `references/harness-engineering.md`.

## Operating Model

Optimize for agent legibility before raw code output.

- Make the repository the system of record. Move decisions, product rules, architecture, schemas, quality bars, and plans into versioned repo-local files.
- Keep `AGENTS.md` short. Use it as a map to deeper docs, not as a monolithic instruction manual.
- Prefer progressive disclosure. Give the agent stable entry points and clear pointers to the next source of truth.
- Let agents use normal developer tools directly: CLI tools, local scripts, test runners, browser automation, logs, metrics, traces, and GitHub commands.
- When an agent fails, ask what capability, context, constraint, or feedback loop is missing. Encode the fix into the harness rather than only retrying the prompt.

## Repository Map

When designing or revising an agent-first repo, create a small, navigable knowledge base:

```text
AGENTS.md
ARCHITECTURE.md
docs/
  design-docs/
    index.md
    core-beliefs.md
  exec-plans/
    active/
    completed/
    tech-debt-tracker.md
  generated/
    db-schema.md
  product-specs/
    index.md
  references/
    <tool-or-framework>-llms.txt
  DESIGN.md
  FRONTEND.md
  PLANS.md
  PRODUCT_SENSE.md
  QUALITY.md
  RELIABILITY.md
  SECURITY.md
```

Adapt the exact names to the repo. Preserve the pattern: short map, indexed docs, executable plans, generated references, and explicit quality domains.

## Workflow

Use this sequence when asked to improve an agent harness:

1. Inventory current agent visibility.
   - Read `AGENTS.md`, docs, scripts, CI, tests, app boot instructions, observability setup, and review workflow.
   - Identify knowledge that exists only in chat, humans' heads, external docs, or unlinked files.

2. Define the scarce resource.
   - Assume human time and attention are constrained.
   - Decide which manual activity should become agent-readable or agent-executable next: context gathering, bug reproduction, UI validation, log inspection, PR review, build recovery, or cleanup.

3. Add legibility before autonomy.
   - Make the app bootable in isolated worktrees when possible.
   - Expose UI state through browser automation, DOM snapshots, screenshots, and navigation scripts.
   - Expose observability through local logs, metrics, traces, and query examples.
   - Add scripts that let the agent reproduce, validate, and summarize outcomes without copy-paste from humans.

4. Encode architecture as constraints.
   - Define allowed layers, dependency directions, cross-cutting boundaries, naming rules, schema conventions, logging requirements, and file-size limits.
   - Prefer custom linters, structural tests, type checks, and CI jobs over prose-only rules.
   - Write lint failures with remediation hints that give agents immediate next steps.

5. Build review and repair loops.
   - Instruct agents to self-review locally, request targeted reviews, respond to feedback, run validation, and iterate until checks pass.
   - Add workflows for recovering from build failures, flakes, and review comments.
   - Escalate to humans only for product judgment, ambiguous tradeoffs, security-sensitive choices, or destructive actions.

6. Add continuous garbage collection.
   - Convert recurring review comments and cleanup preferences into docs, lints, tests, or background cleanup tasks.
   - Track technical debt in repo-local files.
   - Prefer small recurring refactors over occasional large cleanup bursts.

## Design Principles

- Prefer maps over manuals. A concise index plus maintained deep docs beats one giant instruction file.
- Prefer enforceable invariants over taste debates. Capture human taste as checks or narrowly scoped standards.
- Prefer boring, inspectable technologies when agent comprehension matters.
- Prefer explicit boundaries: domain layers, provider interfaces, data validation at boundaries, typed SDKs, and known dependency directions.
- Prefer local, reproducible feedback. Agents should be able to launch, inspect, test, and repair the app in the environment where they work.
- Prefer repository-local memory. If Codex cannot discover it in context or through tools, it effectively does not exist.

## Output Patterns

When producing recommendations, make them concrete:

- Name the missing harness capability.
- State the repo artifact to add or edit.
- Explain how an agent will use it.
- Add the mechanical check or feedback loop that keeps it fresh.
- Include a validation command or acceptance criterion.

Example:

```text
Capability: Agent-readable architecture boundaries
Artifact: docs/ARCHITECTURE.md plus scripts/check-layer-boundaries.ts
Agent use: Read ARCHITECTURE.md before touching domain modules; run the checker before PR creation.
Freshness: CI fails on illegal imports and prints the allowed dependency directions.
Validation: npm run check:architecture
```

## Pitfalls

- Do not expand `AGENTS.md` into a long policy dump. Link to maintained docs instead.
- Do not rely on external memory for critical decisions. Put it in the repo.
- Do not ask agents to "try harder" when the environment is underspecified. Improve the harness.
- Do not grant autonomy before observability, reproducibility, and review loops exist.
- Do not treat generated code volume as success. Track product behavior, reliability, maintainability, and cleanup load.
- Do not let stale docs accumulate without checks, ownership, or recurring doc-gardening.
