# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

## Project
This is a fullstack simulation of an internal Employee Operations Assistant (WorkflowOps Lab) designed specifically to test, evaluate, and visualize AI failure modes (mock API timeouts, missing RAG data, unauthorized requests) via a reliability dashboard.

## Stack
- **Frontend**: Next.js, TypeScript, Tailwind CSS
- **Backend**: Python 3.11+, FastAPI, `pytest`
- **Orchestration**: Anthropic Python SDK
- **Embeddings**: Local open-source via `sentence-transformers` (`BAAI/bge-m3`)
- **Data/Storage**: Local JSON files for evals & state (No database engine committed yet)
*(Note: Postgres/pgvector, Auth, and Observability tools are excluded until the exact infrastructure is initialized and committed.)*

## Architecture boundaries & Decision Tree
The agent executes the stateful loop defined in ARCHITECTURE.md. It is a router, not a blind generator — never call a tool whose preconditions aren't met by accumulated state. See ARCHITECTURE.md for the full tree and failure rules.

## Coding standards
- **Traceability Rule**: Never accept a change I can't read, manually trace, and explain out loud. If the diff is too large to manually trace a single example through, the task was too large — split it.
- **Fail Loudly**: When interacting with the mock enterprise systems, explicit failures are features. Never catch an exception and return a silent empty state or generic fallback unless explicitly commanded.
- **Strict UI States**: All frontend components must account for streaming states, loading states, and partial JSON chunks.

## What not to touch
- **The Eval Directory (`/data/eval_cases` or `/evals`)**: These files are strictly **off-limits** for modifications during feature work. If a code change or prompt update causes an eval case (like a hallucination trap) to fail, you must fix the code or the prompt. You are strictly forbidden from editing the test case's expected output or scoring rubric to force a passing grade.

## Running tests
- Tests: TODO (Command goes here once the evaluation scoring harness is built. Eventually, this will run the synthetic cases across policy Q&A, live data lookups, and escalations.)

## Secrets
- **Zero-Exposure Rule**: API keys, tokens, and DB strings live exclusively in `.env.local` or `.env`. You must never hardcode a literal credential string in the codebase. If you write `sk-ant-`, `sk-proj-`, or `sk-svc-` in any file other than an ignored `.env` file, you have failed the most critical check. `.env*` must be in `.gitignore` and you should never create an env file outside it.

## Decisions
- When making a non-trivial architectural choice (e.g. how the agent decides between the mock PTO API and the Handbook RAG, or how we format the JSON trace logs), the reasoning, tradeoffs, and failure modes must be explicitly recorded in `DECISIONS.md`. Keep the markdown formatting extremely clean so the raw text can be seamlessly ported over into project tracking workspaces like Notion later.
