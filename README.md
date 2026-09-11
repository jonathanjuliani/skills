# jon-skills

Dynamic, vendor-neutral agent skills for JavaScript, TypeScript, React, and React Native, plus the product and delivery work around the code.

Installable as a plugin.

## What makes it different

Most skill sets bake in a stack, a framework, or a convention. The goal with these ones is to resolve the stack at runtime and work with whatever is already there.

Every technical skill consults one **precedence chain** before it touches a tool choice:

1. **Project** the skill detects what the repo already uses (lockfile, `package.json`, config files, existing layout) and defers to it.
2. **Company** if the repo carries a standardization config or skill, that wins over any personal or community default.
3. **Personal** seeded tiebreakers apply only when nothing above resolves the choice.
4. **Community** for anything still open on a greenfield project, the skill recommends the current community default with a one-line rationale, then asks before deciding.

Nothing forces a vendor.

The stack is data resolved at runtime, so the same skills work on a legacy npm/Jest service, a pnpm/Vitest monorepo, and a fresh Expo app without special-casing.

## Guardrails

A rule that a model can talk itself out of is not a rule. Every skill here carries the guardrails that earn their place in it, and no more:

- **When this does not apply** (all of them): the conditions under which the skill's discipline yields. A skill with no escape hatch gets applied to a one-line change, feels absurd, and stops being invoked.
- **Excuses that do not hold**: the specific sentence the agent would tell itself to skip this, and the rebuttal. Only where a real excuse exists.
- **Before you hand it over**: the two or three things that actually go wrong in that skill's output, checked against the output.
- **Persistence**: only on the two skills that set a posture to hold across a session, because the rest run once and finish.

A guardrail shapes how a skill is applied. It never reduces what the agent may analyze, search, read, or consider. The authoring rules for all of this are in [`.agents/conventions.md`](.agents/conventions.md).

## Skills

### Foundation

- **resolve-conventions** (model-invoked): the precedence engine. Detects a project's conventions and resolves anything unresolved against personal then community defaults.
- **setup-skills** (user-invoked): one-time setup. Confirm personal defaults, detect the project, write `.jon-skills/config.yaml`, and **optionally** add a verification block to the repo's `AGENTS.md` or `CLAUDE.md`.
- **agent-instructions** (model-invoked): write or repair a repo's `AGENTS.md` or `CLAUDE.md` so its rules actually bind, on the budget of being read every turn.

### Engineering

- **project-shape** (model-invoked): detect single-repo, monorepo, or modular, and recommend folder and structure best practices per surface (backend, frontend, mobile).
- **ts-standards** (model-invoked): JS/TS conventions reference (naming, types, error handling, module boundaries, validation at boundaries). Principles, not vendors.
- **create** (model-invoked): scaffold a new component, module, package, service, or screen to the resolved conventions and shape. Walks a YAGNI ladder first, since the cheapest unit of code is the one nobody writes.
- **refactor** (model-invoked): behavior-preserving refactor toward the project's conventions, tests green throughout, and no fence removed before it is understood.
- **api-design** (model-invoked): choose REST, tRPC, or GraphQL by consumer, with typed, validated contracts.
- **security-hardening** (model-invoked): find where the system extends trust (untrusted input, access control, secrets, supply chain) and put the right control there.
- **state-management** (model-invoked): separate server state from client state and pick the right tool for each.
- **forms** (model-invoked): forms people can finish. Labels that persist, validation that fires at the right moment, errors that never destroy typed input, and submit that happens once.
- **frontend-craft** (model-invoked): compose React and React Native components well and treat accessibility as part of the build, reaching for the platform before a dependency. Takes its direction from `design-brief`.
- **testing-strategy** (model-invoked): choose seams and test kinds, concentrate effort on critical paths, and run the red-green loop.
- **verify-before-done** (model-invoked): set the observable criterion before starting, then prove it with fresh command output before claiming anything is done, fixed, or passing.
- **dependency-choice** (model-invoked): decide whether to add a dependency and which, judged on current community adoption, fit, and exposure.
- **perf-audit** (model-invoked): measure, fix the dominant cost, re-measure; guidance per surface.
- **observability** (model-invoked): instrument for the questions production will ask, and alert on symptoms a user can feel.
- **ship-flow** (model-invoked): move a change to production in small steps, with CI as a gate, flags, staged rollout, and an undo path.
- **migration** (model-invoked): retire an old dependency, API, or pattern with expand, migrate, contract, and treat deleting the old thing as the actual finish line.
- **release-flow** (model-invoked): versioning, changelog, and publishing, matching the project's existing process.

### Design

Design decides what a surface should be and whether it is good; engineering builds it.

- **design-brief** (model-invoked): establish the surface kind, the audience and what they are doing, the references, the dials, and the constraints that override taste. One sentence that the rest of the work is checked against.
- **information-architecture** (model-invoked): content, hierarchy, navigation, screen and URL structure, naming and flows, decided before anything is styled.
- **design-inspiration** (model-invoked): take a reference apart and reuse the reasoning rather than the pixels, including extracting a token set from a live page and knowing a convention from a signature.
- **design-tokens** (model-invoked): name decisions by role rather than by value, define both themes together, and adopt a token system in a codebase that hardcodes values today.
- **design-review** (model-invoked): scored usability critique ranked by user impact, so a finding is a row a team can prioritise instead of an opinion.

They run in that order on a new surface: a read, then the structure, then the direction and its tokens, then the build in `engineering/`, then the score. On an existing product most of it is already answered and the job is to inherit rather than decide.

`design-inspiration` accumulates what it learns in a personal store at `~/.jon-skills/design/references/`, one file per reference, recording what was taken, what was rejected, and the audience it came from. Personal rather than in the repo, because an installed plugin is read-only and the point is to accumulate across projects. It is the design counterpart to the personal tier of the precedence chain, and it is meant to outgrow the conventions shipped here.

Accessibility splits three ways rather than being one pass: a linter catches the static mistakes, `axe` in CI catches the computed ones, and only what neither can see reaches a human review. `frontend-craft` carries that split, and `design-review` refuses to spend attention on anything the first two tiers should have gated.

### Process

- **align-first** (model-invoked): restate the ask, name the assumptions you would otherwise make silently, surface only the branches whose answers change the work, then continue under stated defaults rather than blocking.
- **investigate-product** (user-invoked): investigate the product and user problem before any solution is designed. Output is a short problem brief.
- **plan-delivery** (user-invoked): sequence a set of asks into phases by value versus effort, with a thin first slice and clear cut lines.
- **diagram** (model-invoked): choose the right diagram for what is being explained and render it.
- **retro** (user-invoked): turn a finished delivery into durable, owned changes that feed the next plan.

Some things are deliberately left out:

- a `bug-hunting` and a `quality` review skill, because Claude Code ships `/code-review` and `/simplify`. On another harness you may want an equivalent; this can change later
- an `item estimation` skill lives inside the `plan-delivery` one

## Optional companions

This pack is self-contained: nothing here requires another plugin to work. A few skills are better with company, and where that is true they name the companion rather than assuming it is installed.

| Want | Where it lives |
| --- | --- |
| A relentless interview until every branch is resolved | `grill-me` and `grill-with-docs` in [mattpocock/skills](https://github.com/mattpocock/skills). `align-first` here is the one-pass version you run every time; that is the heavy one for when it matters |
| A deeper test-driven discipline | `obra/superpowers` and `mattpocock/skills` both ship one. `testing-strategy` here carries the loop well enough to work alone |
| Extracting a token set from a live site | [arvindrk/extract-design-system](https://github.com/arvindrk/extract-design-system), which `design-inspiration` points at rather than reimplementing |
| Building and stress-testing a domain model | `domain-modeling` in [mattpocock/skills](https://github.com/mattpocock/skills). `agent-instructions` here covers what a `CONTEXT.md` should contain |

Claude Code's own `/code-review`, `/simplify`, `/run` and `dataviz` are referenced in a few places and ship with that harness. On Codex, Cursor or Gemini you will want an equivalent, and the skills that mention them say so rather than depending on them.

## Install

The skills are plain `SKILL.md` files, so most agents can read them. Four harnesses have a first-class path; the rest go through the generic installer.

### Any agent, one command

The [open skills CLI](https://github.com/vercel-labs/skills) installs into dozens of agents and handles this repo's layout, since it walks a skill directory up to three levels and supports `skills/<category>/<name>/SKILL.md`:

```bash
npx skills add jonathanjuliani/skills            # pick what you want
npx skills add jonathanjuliani/skills --list     # browse first
```

### Claude Code

```bash
/plugin marketplace add jonathanjuliani/skills
```

```bash
/plugin install jon@skills
```

### Codex

Reads `.codex-plugin/plugin.json`, which points at `skills/`. Skills are invoked with `@`, so `/setup-skills` here is `@setup-skills` there.

```bash
codex plugin marketplace add jonathanjuliani/skills
```

```bash
codex plugin add jon@skills
```

### Cursor

Reads `.cursor-plugin/plugin.json`. Cursor splits short always-on policies (`.cursor/rules/*.mdc`) from full workflows (`.cursor/skills/<name>/SKILL.md`); these are workflows, so they belong in the skills layer, not pasted into rules.

If you sync the files by hand rather than installing the plugin, note that Cursor documents a flat `.cursor/skills/<name>/` layout while this repo groups skills into buckets. Copy the leaf directories, not `skills/` itself. Whether Cursor walks the bucket level is untested here.

### Gemini CLI

Reads `gemini-extension.json`, which loads `GEMINI.md` as context.

```bash
gemini extensions install https://github.com/jonathanjuliani/skills
```

### Then, once per repo

```bash
/setup-skills
```

Confirms your personal defaults, detects the project, writes `.jon-skills/config.yaml`, and offers to add a verification rule to the repo's `AGENTS.md` or `CLAUDE.md`.

> Local development: point the marketplace at your clone, which is also what you want until the first push lands.
>
> ```bash
> /plugin marketplace add ~/development/jon/skills
> ```

### What is verified where

Only Claude Code has been measured. `evals/RESULTS.md` records what was tested and what was not, including the finding that a model-invoked skill was never reached for on its own across eleven runs. Two things carry over from that:

- **Cross-skill chaining** (`Call the Skill tool with "..."`) is Claude Code phrasing. Whether another harness acts on it is untested, so on Codex, Cursor and Gemini treat a skill as self-contained until measured.
- **Nothing in `design/`, and no frontend skill, has an eval.** Seven skills now cover that territory on reasoning alone. `design-review` is the only one whose output is structured enough to score objectively, so it is the one to measure first.
- **User-invoked skills** (`setup-skills`, `investigate-product`, `plan-delivery`, `retro`) rely on `disable-model-invocation`, a Claude Code key, plus `policy.allow_implicit_invocation: false` for OpenAI-style hosts. A harness honouring neither may reach for them on its own, which matters most for `investigate-product`, since it is forbidden from proposing a solution and would derail a coding task.

## Prior art

These are the skill sets this one learned from. Each is worth reaching for directly when you want something narrower, more opinionated, or more complete than what is here: this pack is deliberately small and vendor-neutral, and that is a trade, not a claim to be better.

### Methodology, end to end

| Repo | What it is | Reach for it when |
| --- | --- | --- |
| [obra/superpowers](https://github.com/obra/superpowers) | A full development methodology as composable skills: brainstorm, plan, worktree, subagent-driven execution, TDD, review | You want the process to own the whole loop rather than assembling it yourself. Its `verification-before-completion` is the direct ancestor of `verify-before-done` here |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 25 production engineering skills mapped to a lifecycle, with slash commands, personas and reference checklists | You want breadth and concrete checklists. Most of what `security-hardening`, `observability` and `ship-flow` cover here is deeper there |
| [mattpocock/skills](https://github.com/mattpocock/skills) | A senior TypeScript engineer's daily workflow, built around grilling the user until the ask is actually understood | You want alignment before code. `grill-me` and `grill-with-docs` have no equivalent here and are not duplicated on purpose |
| [anthropics/skills](https://github.com/anthropics/skills) | Anthropic's own skills: document formats, artifacts, MCP builder, skill-creator | You need a document, an artifact, or to author skills. This pack does not go near those |

### Code posture

| Repo | What it is | Reach for it when |
| --- | --- | --- |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | Forces the laziest solution that works, with intensity levels and a published benchmark | You want the anti-over-engineering stance always on. The YAGNI ladder in `create` is a narrow version of its ladder |
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | Behavioral rules from Karpathy's notes on LLM coding pitfalls: surface assumptions, stay surgical, define verifiable goals | You want one short file of guardrails rather than a skill set. Its ideas are spread across `create`, `refactor` and `verify-before-done` here |

### Design and frontend

| Repo | What it is | Reach for it when |
| --- | --- | --- |
| [feature-sliced/skills](https://github.com/feature-sliced/skills) | The official Feature-Sliced Design v2.1 skill: layers, slices, public API boundaries, import rules | You want one prescriptive frontend architecture rather than the layout recommendations in `project-shape`. Note it carries no licence |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Design intelligence as searchable data: UI styles, palettes, font pairings, UX guidelines, across many stacks | You are doing real visual design work. `frontend-craft` sets a direction; this one has the reference library behind it |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | Anti-slop frontend for landing pages, portfolios and redesigns, driven by a design read and three dials | You are building marketing or portfolio surfaces. The design read and dials in `frontend-craft` come from here |

| [educlopez/ui-craft](https://github.com/educlopez/ui-craft) | A design engineering system: one skill over 34 reference files covering heuristics, inspiration, motion, forms, dataviz, recipes and craft levels | You want depth on a specific surface. Its scored-critique method is the ancestor of `design-review` here, and its pattern analysis of `design-inspiration` |
| [julianoczkowski/designer-skills](https://github.com/julianoczkowski/designer-skills) | A nine-skill design pipeline: brief, information architecture, tokens, build, review, tasks, with an orchestrator | You want the whole design process driven end to end. The phase split here follows its shape |
| [arvindrk/extract-design-system](https://github.com/arvindrk/extract-design-system) | Extracts colours, type, spacing, radii and shadows from any public site into a W3C `tokens.json` and `tokens.css` | You want a real starting token set from a reference. `design-inspiration` points at this rather than reimplementing it |

### Output shape

| Repo | What it is | Reach for it when |
| --- | --- | --- |
| [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | Cuts token use hard by stripping the agent's prose | Long sessions where output volume is the cost |
| [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) | Shapes output for action: next step first, state restated, no preamble | You want answers you can act on rather than read. Pick one of this and caveman, not both |
| [blader/humanizer](https://github.com/blader/humanizer) | Removes the structural tells of AI writing, based on Wikipedia's "Signs of AI writing" | You are shipping prose: docs, posts, release notes |

### Catalogues and runtimes

| Repo | What it is | Reach for it when |
| --- | --- | --- |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | A curated list of skills, resources and tools | You are looking for something specific and want to search before building it |
| [humanlayer/skills](https://github.com/humanlayer/skills) | A small set including `improve-claude-md` and agentic control-loop builders | You want an agentic loop or a CI-driven agent. `agent-instructions` here owes its conditional-rule idea to `improve-claude-md` |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | An agent harness performance system: skills, instincts, memory, security | You want to change the harness itself, not just add skills |
| [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | An agent framework built to grow with its user | You are building a custom agent rather than extending an existing one |

Links verified 2026-09. Star counts are deliberately omitted, since they are stale the day they are written.

## Philosophy

Detect before you decide.
Recommend before you impose.
Ask before you assume.
Prove before you claim.

## Motivation and Goals

The plugin is a set of small, composable skills that defer to the project in front of them, so they stay useful across personal and company codebases instead of fighting with whatever is already there.

## Repo layout

- `skills/` the skills themselves, grouped into `foundation/`, `engineering/`, `design/` and `process/`.
- `docs/` human-facing pages, for user-invoked skills only.
- `evals/` the test harness and its findings. `RESULTS.md` records what has and has not been measured, including the parts that failed.
- `scripts/validate.py` the checks. Frontmatter parses, names match folders, guardrails present, cross-references and relative links resolve, `plugin.json` in sync, and markdown style holds (list markers, emphasis, fence languages, table pipes, whitespace, no em-dashes).
- `.githooks/pre-commit` runs those checks before a commit lands.
- `.github/workflows/validate.yml` runs them on push and pull request, plus a weekly link check.
- `.agents/conventions.md` how to write and extend a skill here.
- `AGENTS.md` instructions for an agent working on this repo. Not for consumers: the reusable part is `skills/`.
- `.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/`, `gemini-extension.json` one manifest per harness, kept in sync by the validator.
- `GEMINI.md` the context file the Gemini extension loads for consumers.

There is no Node toolchain here on purpose, and no markdown formatter either. The repo is markdown, YAML and two scripts, so there is no JavaScript to lint, and a formatter was measured against it and rejected: 384 lines changed across 24 files while every measurable axis was already uniform. The style is checked instead of rewritten, and the reasoning is in [`.agents/conventions.md`](.agents/conventions.md). The one dependency is pyyaml.

```bash
pip install pyyaml
git config core.hooksPath .githooks   # once per clone
python3 scripts/validate.py           # offline, fast
python3 scripts/validate.py --links   # also resolves external URLs
```

Skip the hook for a single commit with `git commit --no-verify`.
